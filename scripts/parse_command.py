#!/usr/bin/env python3
"""
Parse natural language commands and execute the appropriate scripts.

Usage:
    python parse_command.py "new task: Buy groceries due: 2026-01-10 details: Get milk tags: personal"
    python parse_command.py "new idea: Dashboard redesign details: Improve UX tags: product, ui"
    python parse_command.py "/todo"
    python parse_command.py "/weekly"
"""

import argparse
import sys
import re
from pathlib import Path
from datetime import datetime, timedelta
import logging

# Add parent directory to path to import other scripts
sys.path.insert(0, str(Path(__file__).parent))

from create_item import create_item, update_item_status
from create_observation import create_observation, create_360_review
from utils import parse_tags, find_item_by_title
from todo import generate_todo, generate_weekly_summary, update_todo_document
from detect_agent import detect_agent, load_agent_context
from process_notepad import process_notepad
from orchestrator import orchestrate_121_prep, orchestrate_daily_summary, handle_ambiguous_query
from strategy_agent import format_strategy_response, handle_strategy_query
from fourps_generator import generate_4ps, finalize_4ps, format_4ps_response
from list_items import list_actions, list_decisions, change_due_date, add_daily_note
from meeting_extractor import format_post_meeting_instructions, save_meeting_summary, create_meeting_summary_from_extraction

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
    elif command_text.startswith('new reminder:'):
        item_type = 'reminder'
    elif command_text.startswith('new decision:'):
        item_type = 'decision'
    else:
        raise ValueError("Command must start with 'new task:', 'new idea:', 'new feature:', 'new action:', 'new reminder:', or 'new decision:'")

    # Extract title (everything between 'new X:' and the first keyword)
    type_prefix = f'new {item_type}:'
    remaining = command_text[len(type_prefix):].strip()

    # Special handling for actions: parse "Person to Action" syntax
    # e.g., "new action: Sarah to review budget" -> assignee: Sarah, title: review budget
    extracted_assignee = None
    if item_type == 'action' and ' to ' in remaining.lower():
        # Check if there's an explicit assignee: field - if so, don't auto-extract
        if 'assignee:' not in remaining.lower():
            # Find " to " (case-insensitive) before any keywords
            keywords_pattern = r'\s+(?:due:|details:|tags:|assignee:)'
            # Get the part before keywords
            keyword_match = re.search(keywords_pattern, remaining, re.IGNORECASE)
            if keyword_match:
                action_part = remaining[:keyword_match.start()]
            else:
                action_part = remaining

            # Look for "Name to Action" pattern
            to_match = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+to\s+(.+)$', action_part, re.IGNORECASE)
            if to_match:
                extracted_assignee = to_match.group(1).strip()
                action_title = to_match.group(2).strip()
                # Replace the action_part in remaining with just the action title
                remaining = action_title + remaining[len(action_part):]

    # Find the first keyword
    keywords = ['due:', 'reminder-date:', 'assignee:', 'date-decided:', 'participants:', 'rationale:', 'related-items:', 'details:', 'tags:']
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
        result = {
            'type': item_type,
            'title': title,
            'details': '',
            'tags': []
        }
        # Add type-specific defaults
        if item_type in ['task', 'action']:
            result['due_date'] = None
        if item_type == 'reminder':
            result['reminder_date'] = None
        if item_type == 'action':
            result['assignee'] = extracted_assignee  # Use extracted from "Person to Action" if available
        if item_type == 'decision':
            result['date_decided'] = None
            result['participants'] = None
            result['rationale'] = None
            result['related_items'] = None
        return result

    title = remaining[:first_keyword_pos].strip()

    # Extract other fields using regex
    due_match = re.search(r'due:\s*([^\s]+(?:\s+[^\s]+)*?)(?:\s+(?:reminder-date:|assignee:|date-decided:|participants:|rationale:|related-items:|details:|tags:)|$)', remaining)
    reminder_date_match = re.search(r'reminder-date:\s*([^\s]+(?:\s+[^\s]+)*?)(?:\s+(?:details:|tags:)|$)', remaining)
    assignee_match = re.search(r'assignee:\s*([^\s]+(?:\s+[^\s]+)*?)(?:\s+(?:due:|details:|tags:)|$)', remaining)
    date_decided_match = re.search(r'date-decided:\s*([^\s]+(?:\s+[^\s]+)*?)(?:\s+(?:participants:|rationale:|related-items:|details:|tags:)|$)', remaining)
    participants_match = re.search(r'participants:\s*(.*?)(?:\s+(?:rationale:|related-items:|details:|tags:)|$)', remaining)
    rationale_match = re.search(r'rationale:\s*(.*?)(?:\s+(?:related-items:|details:|tags:)|$)', remaining)
    related_items_match = re.search(r'related-items:\s*(.*?)(?:\s+(?:details:|tags:)|$)', remaining)
    details_match = re.search(r'details:\s*(.*?)(?:\s+tags:|$)', remaining)
    tags_match = re.search(r'tags:\s*(.+?)$', remaining)

    # Build result based on item type
    result = {
        'type': item_type,
        'title': title,
        'details': details_match.group(1).strip() if details_match else '',
        'tags': parse_tags(tags_match.group(1).strip()) if tags_match else []
    }

    # Add type-specific fields
    if item_type in ['task', 'action']:
        result['due_date'] = due_match.group(1).strip() if due_match else None
    if item_type == 'reminder':
        result['reminder_date'] = reminder_date_match.group(1).strip() if reminder_date_match else None
    if item_type == 'action':
        # Use explicit assignee: field if provided, otherwise use extracted from "Person to Action" syntax
        if assignee_match:
            result['assignee'] = assignee_match.group(1).strip()
        elif extracted_assignee:
            result['assignee'] = extracted_assignee
        else:
            result['assignee'] = None
    if item_type == 'decision':
        result['date_decided'] = date_decided_match.group(1).strip() if date_decided_match else None
        result['participants'] = participants_match.group(1).strip() if participants_match else None
        result['rationale'] = rationale_match.group(1).strip() if rationale_match else None
        result['related_items'] = related_items_match.group(1).strip() if related_items_match else None

    return result


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

    # Handle to-do list commands
    if command_text == '/todo':
        # Return signal for Claude to extract meetings first, then generate to-do list
        today_date = datetime.now().strftime('%Y-%m-%d')
        yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        return f"""TODO_WITH_MEETING_EXTRACT:{today_date}

Claude should automatically:
1. Query yesterday's meetings: mcp__granola__list_meetings(time_range="this_week") and filter for yesterday ({yesterday_date})
2. For each meeting from yesterday that hasn't been processed:
   - Get details: mcp__granola__get_meetings(meeting_ids=["<id>"])
   - Extract actions, decisions, tasks, observations from the summary
   - Create items using ./pos commands
3. After processing all meetings, generate the to-do list:
   - Run: ./pos "/todo-generate"

IMPORTANT: Execute this workflow automatically without asking for confirmation."""

    # Internal command to just generate to-do list (called after meeting extraction)
    if command_text == '/todo-generate':
        file_path, content = generate_todo()
        file_path.write_text(content)
        return f"✓ Generated to-do list: {file_path}"

    if command_text == '/weekly':
        file_path, content = generate_weekly_summary()
        file_path.write_text(content)
        return f"✓ Generated weekly summary: {file_path}"

    # Handle notepad processing commands
    if command_text.lower() in ['process notepad', 'notepad process', '/notepad', 'notepad']:
        # Preview mode - show classification without processing
        result = process_notepad(mode='preview')
        return result

    if command_text.lower() in ['process notepad confirm', 'notepad confirm', '/notepad confirm']:
        # Confirm mode - execute processing without prompting
        result = process_notepad(mode='confirm')
        return result

    # Handle archive command
    if command_text.lower() in ['archive completed', 'archive']:
        from create_item import archive_completed_items
        result = archive_completed_items()
        return result['summary']

    # Handle actions list command
    if command_text.lower() in ['actions', '/actions', 'list actions']:
        result = list_actions()
        return result['summary']

    # Handle decisions list command
    if command_text.lower() in ['decisions', '/decisions', 'list decisions']:
        result = list_decisions()
        return result['summary']

    # Handle change due date command
    if command_text.lower().startswith('change due date:'):
        # Format: "change due date: [title] to: [date]" or "change due date: [title] [date]"
        args = command_text[16:].strip()

        # Try "to:" syntax first
        if ' to: ' in args.lower():
            parts = re.split(r'\s+to:\s*', args, flags=re.IGNORECASE)
            if len(parts) == 2:
                title = parts[0].strip()
                new_date = parts[1].strip()
            else:
                return "✗ Invalid format. Use: change due date: [title] to: [YYYY-MM-DD]"
        else:
            # Try space-separated: last token is date
            parts = args.rsplit(' ', 1)
            if len(parts) == 2 and re.match(r'\d{4}-\d{2}-\d{2}', parts[1]):
                title = parts[0].strip()
                new_date = parts[1].strip()
            else:
                return "✗ Invalid format. Use: change due date: [title] to: [YYYY-MM-DD]"

        result = change_due_date(title, new_date)
        if result['success']:
            # Update today document
            today_path = update_todo_document()
            return f"✓ {result['message']}\n✓ Updated to-do list: {today_path}"
        else:
            return f"✗ {result['message']}"

    # Handle new_daily contribution notes
    if command_text.lower().startswith('new_daily:') or command_text.lower().startswith('new daily:'):
        # Extract the note content
        if command_text.lower().startswith('new_daily:'):
            note = command_text[10:].strip()
        else:
            note = command_text[10:].strip()

        if not note:
            return "✗ Please provide a note: new_daily: [your contribution note]"

        result = add_daily_note(note)
        return f"✓ {result['message']}"

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

    # Handle daily summary commands (non-interactive for Claude Code workflow)
    if command_text.lower() in ['/summary', 'daily summary', '/daily', 'daily']:
        from daily_summary import run_daily_summary, finalize_summary

        # Phase 1: Gather context and generate draft
        result = run_daily_summary()

        # Return draft for Claude to display and conduct conversation
        output = []
        output.append("=" * 60)
        output.append("DAILY SUMMARY DRAFT")
        output.append("=" * 60)
        output.append(result['draft'])
        output.append("=" * 60)
        output.append("")
        output.append("**Next steps for Claude:**")
        output.append("1. Query today's meetings from Granola: mcp__granola__list_meetings(time_range=\"this_week\") and filter for today's date")
        output.append("2. For each meeting, get details: mcp__granola__get_meetings(meeting_ids=[...])")
        output.append("3. Incorporate meeting summaries into the draft (key decisions, actions, outcomes per meeting)")
        output.append("4. Display the enriched draft to the user")
        output.append("5. Ask: 'Have I missed anything you'd like to capture?'")
        output.append("6. If user has additions, run: ./pos \"finalize summary: [user additions]\"")
        output.append("7. If no additions, run: ./pos \"finalize summary\"")

        return '\n'.join(output)

    # Handle finalize summary command (completes daily summary workflow)
    if command_text.lower().startswith('finalize summary'):
        from daily_summary import run_daily_summary, finalize_summary

        # Extract user additions if provided
        if command_text.lower() == 'finalize summary':
            user_additions = None
        else:
            # Format: "finalize summary: [additions]"
            user_additions = command_text[17:].strip()  # After "finalize summary:"
            if user_additions.startswith(':'):
                user_additions = user_additions[1:].strip()

        # Re-run to get fresh draft, then finalize
        result = run_daily_summary()
        filepath = finalize_summary(result['draft'], user_additions)

        return f"✓ Daily summary saved: {filepath}"

    # Handle 4Ps generation command
    if command_text.lower() in ['4ps', '/4ps', 'generate 4ps', 'weekly 4ps', '/weekly']:
        result = generate_4ps()
        return format_4ps_response(result)

    # Handle finalize 4Ps command
    if command_text.lower().startswith('finalize 4ps'):
        # Extract final content if provided
        if command_text.lower() == 'finalize 4ps':
            # Use the draft as-is
            result = generate_4ps()
            filepath = finalize_4ps(result['draft'])
        else:
            # User provided final content: "finalize 4ps: [content]"
            final_content = command_text[13:].strip()  # After "finalize 4ps:"
            if final_content.startswith(':'):
                final_content = final_content[1:].strip()
            filepath = finalize_4ps(final_content)

        return f"✓ 4Ps saved to: {filepath}"

    # Handle Slack digest command
    if command_text.lower() in ['slack digest', '/slack-digest', 'slack summary']:
        from slack_digest import run_digest_workflow, load_config

        print("\n📊 Slack Digest Generator\n")

        config = load_config()
        if not config:
            return "✗ Could not load Slack configuration. Check .slack_digest_config.json"

        # Run workflow (prints instructions for Claude Code)
        run_digest_workflow()

        return """
To complete the digest:
1. Call Slack MCP for each channel listed above
2. Parse responses using parse_slack_csv()
3. Call generate_digest_from_data() with the channel data

The digest file will be saved to Work/Inbox/Today/slack_digest_YYYY-MM-DD.md
"""

    # Handle sync meetings command (Granola integration)
    if command_text.lower() in ['sync meetings', '/sync-meetings', 'sync-meetings']:
        from sync_meetings import sync_todays_meetings
        result = sync_todays_meetings()
        if result['synced'] == 0:
            return "No meetings found for today in Granola"
        elif result['errors']:
            return f"✓ Synced {result['synced']} meeting(s) with {len(result['errors'])} error(s)"
        else:
            files_list = '\n  '.join(result['files'])
            return f"✓ Synced {result['synced']} meeting(s) to Obsidian:\n  {files_list}"

    # Handle 121 prep with orchestration (cross-domain context gathering)
    if command_text.lower().startswith('121 prep:'):
        person_name = command_text[9:].strip()

        # Use orchestrator to gather cross-domain context
        context = orchestrate_121_prep(person_name)

        # Build context summary for Claude
        output = f"""✓ Gathered context for 121 with {person_name}

**Sources checked:** {', '.join(context['sources_checked'])}
**Total context items:** {context['total_items']}

"""
        if context['observations']:
            output += f"**Observations ({len(context['observations'])}):**\n"
            for obs in context['observations'][:3]:
                output += f"  - {obs['date']}: {obs['content'][:100]}...\n"
            output += "\n"

        if context['past_121s']:
            output += f"**Past 121s ({len(context['past_121s'])}):**\n"
            for m in context['past_121s'][:3]:
                output += f"  - {m['date']}: {m['title']}\n"
            output += "\n"

        if context['actions']:
            output += f"**Open Actions ({len(context['actions'])}):**\n"
            for a in context['actions'][:3]:
                output += f"  - {a['title']}\n"
            output += "\n"

        if context['tasks']:
            output += f"**Related Tasks ({len(context['tasks'])}):**\n"
            for t in context['tasks'][:3]:
                output += f"  - {t['title']}\n"
            output += "\n"

        output += f"""**Memory query suggestion:**
  {context['memory_query']['suggested_query']}

Now creating prep document with gathered context..."""

        # Also create the prep document
        from prep_meeting import prep_meeting
        filepath = prep_meeting(person_name, attendees=[person_name])

        output += f"\n\n✓ Created meeting prep: {filepath}"
        return output

    # Handle meeting prep commands
    if command_text.lower().startswith('prep meeting:') or command_text.lower().startswith('121:'):
        from prep_meeting import prep_meeting

        # Extract title/name after the colon
        if command_text.lower().startswith('prep meeting:'):
            title = command_text[13:].strip()
            attendees = None
        else:  # 121: command
            title = command_text[4:].strip()
            attendees = [title]  # For 121s, the title IS the person

        filepath = prep_meeting(title, attendees)
        return f"✓ Created meeting prep: {filepath}"

    # Handle MFM review commands
    if command_text.lower().startswith('mfm review:') or command_text.lower().startswith('review mfm:'):
        from mfm_agent import review_mfm

        # Extract squad and month
        if command_text.lower().startswith('mfm review:'):
            args = command_text[11:].strip()
        else:  # review mfm:
            args = command_text[11:].strip()

        # Parse squad and month from args (e.g., "strategic accounts Feb")
        # Simple parsing: last word is month, everything else is squad
        parts = args.rsplit(' ', 1)
        if len(parts) == 2:
            squad_name, month = parts
        else:
            squad_name = args
            month = datetime.now().strftime('%b')

        result = review_mfm(squad_name, month)

        if not result['success']:
            error_msg = f"✗ {result['error']}"
            if result.get('suggestions'):
                error_msg += f"\nAvailable: {', '.join(result['suggestions'][:5])}"
            return error_msg

        # Return info for Claude to perform analysis
        return f"""✓ Found MFM pre-read: {result['filename']}

**Next steps:**
1. Read framework: Work/LLM_Context/MFM_review_framework.md
2. Analyze pre-read against five dimensions
3. Create review notes at: {result['output_path']}

Pre-read content ready for analysis ({len(result['pre_read_content'])} chars)"""

    # Handle MFM summary commands
    if command_text.lower().startswith('mfm summary:') or command_text.lower().startswith('post mfm:'):
        from mfm_agent import post_mfm_summary

        # Extract squad and month
        if command_text.lower().startswith('mfm summary:'):
            args = command_text[12:].strip()
        else:  # post mfm:
            args = command_text[9:].strip()

        # Parse squad and month
        parts = args.rsplit(' ', 1)
        if len(parts) == 2:
            squad_name, month = parts
        else:
            squad_name = args
            month = datetime.now().strftime('%b')

        result = post_mfm_summary(squad_name, month)

        if result.get('needs_granola_data'):
            return f"""✓ Ready for MFM summary: {squad_name} {month}

**Next steps:**
1. Search Granola for MFM meeting
2. Extract decisions, actions, and changes
3. Create summary at: {result['output_path']}

Use mcp__granola__query_granola_meetings to find the meeting."""

        return f"✓ Created MFM summary: {result['output_path']}"

    # Handle post-meeting processing commands (auto-extraction workflow)
    if command_text.lower().startswith('post meeting:') or command_text.lower().startswith('process meeting:'):
        # Extract title after the colon
        if command_text.lower().startswith('post meeting:'):
            title = command_text[13:].strip()
        else:  # process meeting:
            title = command_text[16:].strip()

        # Return a signal for Claude to execute the automatic extraction workflow
        return f"""MEETING_AUTO_EXTRACT:{title}

Claude should now automatically:
1. Query Granola: mcp__granola__query_granola_meetings(query="{title}") or mcp__granola__list_meetings(time_range="this_week")
2. Get meeting details: mcp__granola__get_meetings(meeting_ids=["<meeting_id>"])
3. Get transcript if available: mcp__granola__get_meeting_transcript(meeting_id="<meeting_id>")
4. Analyze the summary/transcript to extract:
   - ACTIONS: [Person] to [task] by [date]
   - DECISIONS: What was decided, rationale, participants
   - TASKS FOR ME: Things I committed to doing
   - OBSERVATIONS: Feedback about team members
5. Create items using ./pos commands:
   - ./pos "new action: [Person] to [task] due: [date]"
   - ./pos "new decision: [decision] participants: [names]"
   - ./pos "new task: [title] due: [date] details: [context]"
   - ./pos "observation: [Person] - [feedback]"
6. Finalize: ./pos "finalize meeting: {title} | actions: X | decisions: Y | tasks: Z"

IMPORTANT: Execute this workflow automatically without asking for confirmation."""

    # Handle finalize meeting command (creates summary after extraction)
    if command_text.lower().startswith('finalize meeting:'):
        # This is called after Claude has extracted and created items
        # Format: finalize meeting: [title] | takeaways: [...] | actions: X | decisions: Y
        args = command_text[17:].strip()

        # Simple case: just the title - create a basic summary
        if '|' not in args:
            title = args
            content = f"""# {title} - {datetime.now().strftime('%Y-%m-%d')}

## Key takeaways

- Meeting processed - see individual items created

## Actions

- See Work/Inbox/Actions/ for extracted actions

## Decisions

- See Work/Decisions/ for extracted decisions

---
Processed by Meetings Agent
"""
            filepath = save_meeting_summary(title, content)
            return f"✓ Created meeting summary: {filepath}"

        # Parse structured input
        parts = [p.strip() for p in args.split('|')]
        title = parts[0]

        # Count items from parts (format: "actions: 3")
        items_created = {'actions': 0, 'decisions': 0, 'tasks': 0, 'observations': 0}
        for part in parts[1:]:
            if ':' in part:
                key, val = part.split(':', 1)
                key = key.strip().lower()
                if key in items_created:
                    try:
                        items_created[key] = int(val.strip())
                    except ValueError:
                        pass

        content = f"""# {title} - {datetime.now().strftime('%Y-%m-%d')}

## Summary

Meeting processed with automatic extraction.

**Items created:**
- Actions: {items_created['actions']}
- Decisions: {items_created['decisions']}
- Tasks: {items_created['tasks']}
- Observations: {items_created['observations']}

## Actions

See Work/Inbox/Actions/ for extracted action items.

## Decisions

See Work/Decisions/ for extracted decisions.

---
Processed by Meetings Agent with auto-extraction
"""
        filepath = save_meeting_summary(title, content)
        return f"✓ Created meeting summary: {filepath}\n  Actions: {items_created['actions']}, Decisions: {items_created['decisions']}, Tasks: {items_created['tasks']}, Observations: {items_created['observations']}"

    # Handle hiring commands
    hiring_commands = [
        'setup role:', 'screen cvs:', 'review cv:', 'shortlist:',
        'interview prep:', 'interview eval:', 'candidate summary:'
    ]
    if any(command_text.lower().startswith(cmd) for cmd in hiring_commands):
        from hiring_agent import handle_hiring_command
        result = handle_hiring_command(command_text)
        return result

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

        # Extract type-specific fields
        kwargs = {}
        if 'reminder_date' in parsed:
            kwargs['reminder_date'] = parsed['reminder_date']
        if 'assignee' in parsed:
            kwargs['assignee'] = parsed['assignee']
        if 'date_decided' in parsed:
            kwargs['date_decided'] = parsed['date_decided']
        if 'participants' in parsed:
            kwargs['participants'] = parsed['participants']
        if 'rationale' in parsed:
            kwargs['rationale'] = parsed['rationale']
        if 'related_items' in parsed:
            kwargs['related_items'] = parsed['related_items']

        file_path = create_item(
            item_type=parsed['type'],
            title=parsed['title'],
            due_date=parsed.get('due_date'),
            details=parsed['details'],
            tags=parsed['tags'],
            **kwargs
        )

        # Auto-update today document
        today_path = update_todo_document()

        return f"✓ Created {parsed['type']}: {file_path}\n✓ Updated to-do list: {today_path}"

    # Handle complete/archive commands (legacy)
    if command_text.startswith('complete ') or command_text.startswith('archive '):
        parsed = parse_status_command(command_text)

        file_path = update_item_status(
            item_type=parsed['item_type'],
            title=parsed['title'],
            new_status=parsed['status']
        )

        # Auto-update today document
        today_path = update_todo_document()

        status_action = 'completed' if parsed['status'] == 'completed' else 'archived'
        return f"✓ Marked {parsed['item_type']} as {status_action}: {file_path}\n✓ Updated to-do list: {today_path}"

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
        today_path = update_todo_document()

        # Build result message
        note_text = f" (note: {note})" if note else ""
        return f"✓ Marked {item_type} '{file_title}' as {status}{note_text}\n✓ Updated: {file_path}\n✓ Updated to-do list: {today_path}"

    # Handle strategy queries (detected by keywords like OKR, strategy, bet)
    agent, confidence = detect_agent(command_text)
    if agent == 'strategy':
        return format_strategy_response(command_text)

    raise ValueError("Unknown command format. Use 'new task:', 'new idea:', 'new feature:', 'update:', 'complete task:', 'archive idea:', 'observation:', '360 review:', '/todo', or '/weekly'")


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Parse and execute Personal OS commands",
        epilog="""
Examples:
  %(prog)s "new task: Buy groceries due: 2026-01-10 details: Get milk and bread tags: personal, shopping"
  %(prog)s "new idea: Dashboard redesign details: Improve the analytics UI tags: product, ui"
  %(prog)s "new feature: Dark mode details: Add dark theme support tags: ui, frontend"
  %(prog)s "/todo"
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
