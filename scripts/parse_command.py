#!/usr/bin/env python3
"""
Parse natural language commands and execute the appropriate scripts.

Usage:
    python parse_command.py "new task: Buy groceries due: 2026-01-10 details: Get milk tags: personal"
    python parse_command.py "new idea: Dashboard redesign details: Improve UX tags: product, ui"
    python parse_command.py "/today"
    python parse_command.py "/weekly"
"""

import argparse
import sys
import re
from pathlib import Path
import logging

# Add parent directory to path to import other scripts
sys.path.insert(0, str(Path(__file__).parent))

from create_item import create_item, update_item_status
from create_observation import create_observation, create_360_review
from utils import parse_tags, find_item_by_title
from summary import generate_today_summary, generate_weekly_summary, update_today_document
from detect_agent import detect_agent, load_agent_context

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('julie.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('julie')


def is_observation_command(command_text):
    """
    Check if command is an observation/feedback command.

    Args:
        command_text: The full command string

    Returns:
        Boolean indicating if this is an observation command
    """
    observation_triggers = [
        'observation:',
        'i have an observation:',
        'i have feedback:',
        'feedback:',
    ]

    command_lower = command_text.lower()
    return any(command_lower.startswith(trigger) for trigger in observation_triggers)


def parse_observation_command(command_text):
    """
    Parse an observation command.

    Args:
        command_text: The full command string

    Returns:
        Dictionary with parsed observation data
    """
    # Remove trigger phrase
    observation_triggers = [
        'observation:',
        'i have an observation:',
        'i have feedback:',
        'feedback:',
    ]

    command_lower = command_text.lower()
    remaining = command_text

    for trigger in observation_triggers:
        if command_lower.startswith(trigger):
            remaining = command_text[len(trigger):].strip()
            break

    # Find first keyword (details: or tags:)
    keywords = ['details:', 'tags:']
    first_keyword_pos = len(remaining)

    for keyword in keywords:
        pos = remaining.find(keyword)
        if pos != -1 and pos < first_keyword_pos:
            first_keyword_pos = pos

    if first_keyword_pos == len(remaining):
        # No keywords, entire remaining text is the title
        title = remaining.strip()
        return {
            'title': title,
            'details': '',
            'tags': []
        }

    title = remaining[:first_keyword_pos].strip()

    # Extract fields using regex
    details_match = re.search(r'details:\s*(.*?)(?:\s+tags:|$)', remaining)
    tags_match = re.search(r'tags:\s*(.+?)$', remaining)

    details = details_match.group(1).strip() if details_match else ''
    tags_str = tags_match.group(1).strip() if tags_match else ''
    tags = parse_tags(tags_str)

    return {
        'title': title,
        'details': details,
        'tags': tags
    }


def parse_status_command(command_text):
    """
    Parse a status update command (complete or archive).

    Args:
        command_text: The full command string

    Returns:
        Dictionary with parsed command data
    """
    # Determine command type
    if command_text.startswith('complete '):
        new_status = 'completed'
        command_prefix = 'complete '
    elif command_text.startswith('archive '):
        new_status = 'archived'
        command_prefix = 'archive '
    else:
        raise ValueError("Command must start with 'complete ' or 'archive '")

    # Extract item type and title
    remaining = command_text[len(command_prefix):].strip()

    # Expected format: "complete task: Title" or "archive idea: Title"
    item_types = ['task', 'idea', 'feature', 'action']
    item_type = None
    title = None

    for itype in item_types:
        if remaining.startswith(f'{itype}:'):
            item_type = itype
            title = remaining[len(itype) + 1:].strip()
            break

    if not item_type or not title:
        raise ValueError(f"Invalid format. Use 'complete task: Title' or 'archive idea: Title'")

    return {
        'item_type': item_type,
        'title': title,
        'status': new_status
    }


def parse_update_command(command_text):
    """
    Parse an update command with field-based syntax.

    Expected format: "update: [title] status: [status] note: [optional note]"

    Args:
        command_text: The full command string

    Returns:
        Dictionary with parsed data or None if not an update command

    Raises:
        ValueError: If status is missing or invalid
    """
    if not command_text.startswith('update:'):
        return None

    # Remove 'update:' prefix
    remaining = command_text[7:].strip()

    # Extract status if present
    status_match = re.search(r'\s+status:\s*([^\s]+)', remaining)
    if not status_match:
        # Status is required - return error that will prompt user
        raise ValueError("Status is required. Please specify: status: [active|in-progress|blocked|waiting|on-hold|completed|archived]")

    status = status_match.group(1).strip()

    # Validate status
    valid_statuses = ['active', 'in-progress', 'blocked', 'waiting', 'on-hold', 'completed', 'archived']
    if status not in valid_statuses:
        raise ValueError(f"Invalid status: {status}. Must be one of: {', '.join(valid_statuses)}")

    # Extract note if present
    note_match = re.search(r'\s+note:\s*(.+)$', remaining)
    note = note_match.group(1).strip() if note_match else None

    # Extract title (everything before 'status:')
    title_end = remaining.find(' status:')
    if title_end == -1:
        title_end = remaining.find(' note:') if note_match else len(remaining)

    title = remaining[:title_end].strip()

    if not title:
        raise ValueError("Item title is required")

    return {
        'title': title,
        'status': status,
        'note': note
    }


def parse_natural_language_status(command_text):
    """
    Parse natural language status update commands.

    Recognizes patterns like:
    - "Task X is complete"
    - "Mark idea Y as archived"
    - "X is done"
    - "Update feature Z to in progress"
    - "Block task X note: Waiting for approval"

    Args:
        command_text: The full command string

    Returns:
        Dictionary with parsed data or None if not a natural language status command
    """
    import re

    # Status keywords and their mappings
    status_keywords = {
        'complete': 'completed',
        'completed': 'completed',
        'done': 'completed',
        'finished': 'completed',
        'archive': 'archived',
        'archived': 'archived',
        'in progress': 'in-progress',
        'in-progress': 'in-progress',
        'working on': 'in-progress',
        'started': 'in-progress',
        'block': 'blocked',
        'blocked': 'blocked',
        'waiting': 'waiting',
        'wait': 'waiting',
        'on hold': 'on-hold',
        'on-hold': 'on-hold',
        'pause': 'on-hold',
        'paused': 'on-hold',
        'active': 'active',
        'resume': 'active',
        'reopen': 'active'
    }

    # Extract note if present
    note = None
    note_match = re.search(r'\s+note:\s*(.+)$', command_text, re.IGNORECASE)
    if note_match:
        note = note_match.group(1).strip()
        # Remove note from command for further parsing
        command_text = command_text[:note_match.start()].strip()

    # Pattern 1: "X is {status}" or "{status} X"
    for keyword, status_value in status_keywords.items():
        # Pattern: "X is {status}"
        pattern1 = rf'^(.+?)\s+is\s+{re.escape(keyword)}$'
        match = re.match(pattern1, command_text, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            return {
                'title': title,
                'status': status_value,
                'note': note
            }

        # Pattern: "{status} X"
        pattern2 = rf'^{re.escape(keyword)}\s+(.+)$'
        match = re.match(pattern2, command_text, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            return {
                'title': title,
                'status': status_value,
                'note': note
            }

    # Pattern 2: "mark X as {status}" or "set X to {status}" or "update X to {status}"
    action_words = ['mark', 'set', 'update', 'change']
    for action in action_words:
        for keyword, status_value in status_keywords.items():
            pattern = rf'^{action}\s+(.+?)\s+(?:as|to)\s+{re.escape(keyword)}$'
            match = re.match(pattern, command_text, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                return {
                    'title': title,
                    'status': status_value,
                    'note': note
                }

    return None


def parse_creation_command(command_text):
    """
    Parse a creation command (new task, new idea, new feature, new action).

    Args:
        command_text: The full command string

    Returns:
        Dictionary with parsed command data
    """
    # Determine command type
    if command_text.startswith('new task:'):
        item_type = 'task'
    elif command_text.startswith('new idea:'):
        item_type = 'idea'
    elif command_text.startswith('new feature:'):
        item_type = 'feature'
    elif command_text.startswith('new action:'):
        item_type = 'action'
    else:
        raise ValueError("Command must start with 'new task:', 'new idea:', 'new feature:', or 'new action:'")

    # Extract title (everything between 'new X:' and the first keyword)
    type_prefix = f'new {item_type}:'
    remaining = command_text[len(type_prefix):].strip()

    # Find the first keyword (due:, details:, or tags:)
    keywords = ['due:', 'details:', 'tags:']
    first_keyword_pos = len(remaining)
    first_keyword = None

    for keyword in keywords:
        pos = remaining.find(keyword)
        if pos != -1 and pos < first_keyword_pos:
            first_keyword_pos = pos
            first_keyword = keyword

    if first_keyword_pos == len(remaining):
        # No keywords found, entire remaining text is the title
        title = remaining.strip()
        return {
            'type': item_type,
            'title': title,
            'due_date': None,
            'details': '',
            'tags': []
        }

    title = remaining[:first_keyword_pos].strip()

    # Extract other fields using regex
    due_match = re.search(r'due:\s*([^\s]+(?:\s+[^\s]+)*?)(?:\s+(?:details:|tags:)|$)', remaining)
    details_match = re.search(r'details:\s*(.*?)(?:\s+tags:|$)', remaining)
    tags_match = re.search(r'tags:\s*(.+?)$', remaining)

    due_date = due_match.group(1).strip() if due_match else None
    details = details_match.group(1).strip() if details_match else ''
    tags_str = tags_match.group(1).strip() if tags_match else ''
    tags = parse_tags(tags_str)

    return {
        'type': item_type,
        'title': title,
        'due_date': due_date,
        'details': details,
        'tags': tags
    }


def route_to_agent(command_text):
    """
    Route command to appropriate agent.

    Phase 1.1: Just logging, not routing yet.
    Returns None to signal "continue with normal processing"
    """
    agent, confidence = detect_agent(command_text)

    # Log the detection
    logger.info(f"Agent detection: '{command_text[:50]}...' -> {agent} (confidence: {confidence})")

    # Phase 1.1: Don't route yet, just log
    # TODO: Phase 1.2 will activate routing for tasks agent

    return None  # Signal to continue with normal processing


def execute_command(command_text):
    """
    Execute a command based on the input text.

    Args:
        command_text: The full command string

    Returns:
        Success message string
    """
    command_text = command_text.strip()

    # Check if we should route to an agent
    agent_result = route_to_agent(command_text)
    if agent_result is not None:
        # Agent handled it, we're done
        return agent_result

    # Handle summary commands
    if command_text == '/today':
        file_path, content = generate_today_summary()
        file_path.write_text(content)
        return f"✓ Generated today summary: {file_path}"

    if command_text == '/weekly':
        file_path, content = generate_weekly_summary()
        file_path.write_text(content)
        return f"✓ Generated weekly summary: {file_path}"

    # Handle session logging commands
    if command_text.lower().startswith('session:') or command_text.lower().startswith('/session'):
        from session_log import log_session

        # Extract session summary
        if command_text.lower().startswith('session:'):
            summary = command_text[8:].strip()
        else:  # starts with '/session'
            summary = command_text[8:].strip()

        if not summary:
            return "✗ Please provide a session summary: session: [what you worked on]"

        log_file = log_session(summary)
        return f"✓ Session logged to: {log_file}"

    # Handle daily summary interview commands
    if command_text.lower() in ['/summary', 'daily summary', '/daily', 'daily']:
        from daily_summary_interview import conduct_interview

        result = conduct_interview()
        if result:
            return f"✓ Daily summary saved: {result}"
        else:
            return "✗ Daily summary cancelled"

    # Handle 360 review commands
    if command_text.lower().startswith('360 review:') or command_text.lower().startswith('360:'):
        # Extract team member name after the trigger
        if command_text.lower().startswith('360 review:'):
            team_member = command_text[11:].strip()
        else:  # starts with '360:'
            team_member = command_text[4:].strip()

        file_path, is_new = create_360_review(team_member)

        if is_new:
            return f"✓ Created 360 review: {file_path}"
        else:
            return f"✓ 360 review already exists: {file_path}"

    # Handle observation commands
    if is_observation_command(command_text):
        parsed = parse_observation_command(command_text)

        file_path = create_observation(
            title=parsed['title'],
            details=parsed['details'],
            tags=parsed['tags']
        )

        return f"✓ Created observation: {file_path}"

    # Handle creation commands
    if command_text.startswith('new '):
        parsed = parse_creation_command(command_text)

        file_path = create_item(
            item_type=parsed['type'],
            title=parsed['title'],
            due_date=parsed['due_date'],
            details=parsed['details'],
            tags=parsed['tags']
        )

        # Auto-update today document
        today_path = update_today_document()

        return f"✓ Created {parsed['type']}: {file_path}\n✓ Updated today summary: {today_path}"

    # Handle complete/archive commands (legacy)
    if command_text.startswith('complete ') or command_text.startswith('archive '):
        parsed = parse_status_command(command_text)

        file_path = update_item_status(
            item_type=parsed['item_type'],
            title=parsed['title'],
            new_status=parsed['status']
        )

        # Auto-update today document
        today_path = update_today_document()

        status_action = 'completed' if parsed['status'] == 'completed' else 'archived'
        return f"✓ Marked {parsed['item_type']} as {status_action}: {file_path}\n✓ Updated today summary: {today_path}"

    # Handle update command (new primary method)
    if command_text.startswith('update:'):
        parsed = parse_update_command(command_text)

        title = parsed['title']
        status = parsed['status']
        note = parsed['note']

        # Find matching items using fuzzy matching
        matches = find_item_by_title(title)

        if not matches:
            return f"✗ No items found matching: '{title}'"

        # Handle disambiguation if multiple matches
        if len(matches) > 1:
            # Check if there's a clear best match (significantly higher score)
            best_score = matches[0][3]
            second_score = matches[1][3]

            # If the best match is significantly better, use it
            if best_score - second_score >= 0.2:
                item_type, file_path, file_title, score = matches[0]
            else:
                # Present options to user
                options_text = "\nMultiple items found. Please be more specific or use the exact title:\n"
                for i, (itype, fpath, ftitle, score) in enumerate(matches[:5], 1):
                    options_text += f"  {i}. [{itype}] {ftitle} (match: {score:.0%})\n"
                return f"✗ Ambiguous match.{options_text}"
        else:
            item_type, file_path, file_title, score = matches[0]

        # Update the item status
        file_path = update_item_status(
            item_type=item_type,
            title=file_title,
            new_status=status,
            status_note=note
        )

        # Auto-update today document
        today_path = update_today_document()

        # Build result message
        note_text = f" (note: {note})" if note else ""
        return f"✓ Marked {item_type} '{file_title}' as {status}{note_text}\n✓ Updated: {file_path}\n✓ Updated today summary: {today_path}"

    raise ValueError("Unknown command format. Use 'new task:', 'new idea:', 'new feature:', 'update:', 'complete task:', 'archive idea:', 'observation:', '360 review:', '/today', or '/weekly'")


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Parse and execute Personal OS commands",
        epilog="""
Examples:
  %(prog)s "new task: Buy groceries due: 2026-01-10 details: Get milk and bread tags: personal, shopping"
  %(prog)s "new idea: Dashboard redesign details: Improve the analytics UI tags: product, ui"
  %(prog)s "new feature: Dark mode details: Add dark theme support tags: ui, frontend"
  %(prog)s "/today"
  %(prog)s "/weekly"
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'command',
        help='The command to execute (in quotes)'
    )

    args = parser.parse_args()

    try:
        result = execute_command(args.command)
        print(result)
        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
