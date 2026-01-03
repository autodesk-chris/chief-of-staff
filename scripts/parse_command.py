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

# Add parent directory to path to import other scripts
sys.path.insert(0, str(Path(__file__).parent))

from create_item import create_item
from create_observation import create_observation
from utils import parse_tags
from summary import generate_today_summary, generate_weekly_summary


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


def execute_command(command_text):
    """
    Execute a command based on the input text.

    Args:
        command_text: The full command string

    Returns:
        Success message string
    """
    command_text = command_text.strip()

    # Handle summary commands
    if command_text == '/today':
        file_path, content = generate_today_summary()
        file_path.write_text(content)
        return f"✓ Generated today summary: {file_path}"

    if command_text == '/weekly':
        file_path, content = generate_weekly_summary()
        file_path.write_text(content)
        return f"✓ Generated weekly summary: {file_path}"

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

        return f"✓ Created {parsed['type']}: {file_path}"

    raise ValueError("Unknown command format. Use 'new task:', 'new idea:', 'new feature:', 'observation:', '/today', or '/weekly'")


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
