#!/usr/bin/env python3
"""
Create tasks, ideas, or features in the Obsidian Inbox.

Usage:
    python create_item.py task "Task Title" --due "2026-01-10" --details "Description" --tags "tag1, tag2"
    python create_item.py idea "Idea Title" --details "Description" --tags "tag1, tag2"
    python create_item.py feature "Feature Title" --details "Description" --tags "tag1, tag2"
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    sanitize_filename,
    parse_tags,
    format_tags_yaml,
    validate_date,
    get_inbox_path
)


def create_frontmatter(item_type, due_date=None, tags=None, status='active', status_note=None):
    """
    Generate YAML frontmatter for the file.

    Args:
        item_type: Type of item ('task', 'idea', or 'feature')
        due_date: Due date string (YYYY-MM-DD) or None
        tags: List of tag strings or None
        status: Status of item ('active', 'in-progress', 'blocked', 'waiting', 'on-hold', 'completed', or 'archived')
        status_note: Optional note about the status

    Returns:
        Formatted frontmatter string
    """
    tags_formatted = format_tags_yaml(tags) if tags else "[]"
    status_note_line = f"\nstatus-note: {status_note}" if status_note else ""

    # For tasks and actions with due dates
    if item_type in ['task', 'action'] and due_date:
        frontmatter = f"""---
type: {item_type}
status: {status}{status_note_line}
due-date: {due_date}
tags: {tags_formatted}
---"""
    # For tasks/actions without due dates, ideas, and features
    else:
        frontmatter = f"""---
type: {item_type}
status: {status}{status_note_line}
tags: {tags_formatted}
due-date: null
---"""

    return frontmatter


def create_content(item_type, title, details):
    """
    Generate the main content for the file.

    Args:
        item_type: Type of item ('task', 'idea', or 'feature')
        title: Title of the item
        details: Detailed description

    Returns:
        Formatted content string
    """
    item_label = item_type.capitalize()

    content = f"""
# {item_label}: {title}

## Details

{details}
"""

    return content


def create_item(item_type, title, due_date=None, details="", tags=None):
    """
    Create a new task, idea, feature, or action file.

    Args:
        item_type: Type of item ('task', 'idea', 'feature', or 'action')
        title: Title of the item
        due_date: Due date (YYYY-MM-DD) for tasks and actions, optional
        details: Detailed description
        tags: List of tag strings

    Returns:
        Path to the created file
    """
    # Validate inputs
    if item_type not in ['task', 'idea', 'feature', 'action']:
        raise ValueError(f"Invalid item type: {item_type}. Must be 'task', 'idea', 'feature', or 'action'.")

    if item_type in ['task', 'action'] and due_date and not validate_date(due_date):
        raise ValueError(f"Invalid date format: {due_date}. Must be YYYY-MM-DD.")

    # Get the appropriate folder
    inbox_path = get_inbox_path(item_type)

    # Create the filename
    safe_title = sanitize_filename(title)
    filename = f"{item_type}_{safe_title}.md"
    file_path = inbox_path / filename

    # Check if file already exists
    if file_path.exists():
        raise FileExistsError(f"File already exists: {file_path}")

    # Generate frontmatter and content
    frontmatter = create_frontmatter(item_type, due_date, tags)
    content = create_content(item_type, title, details)

    # Combine and write to file
    full_content = frontmatter + content

    file_path.write_text(full_content)

    return file_path


def update_item_status(item_type, title, new_status, status_note=None):
    """
    Update the status of an existing task, idea, feature, or action.

    Args:
        item_type: Type of item ('task', 'idea', 'feature', or 'action')
        title: Title of the item (used to find the file)
        new_status: New status ('active', 'in-progress', 'blocked', 'waiting', 'on-hold', 'completed', 'archived')
        status_note: Optional note about the status change

    Returns:
        Path to the updated file

    Raises:
        FileNotFoundError: If the item doesn't exist
        ValueError: If invalid item type or status
    """
    # Validate inputs
    if item_type not in ['task', 'idea', 'feature', 'action']:
        raise ValueError(f"Invalid item type: {item_type}. Must be 'task', 'idea', 'feature', or 'action'.")

    valid_statuses = ['active', 'in-progress', 'blocked', 'waiting', 'on-hold', 'completed', 'archived']
    if new_status not in valid_statuses:
        raise ValueError(f"Invalid status: {new_status}. Must be one of: {', '.join(valid_statuses)}.")

    # Get the appropriate folder
    inbox_path = get_inbox_path(item_type)

    # Create the expected filename
    safe_title = sanitize_filename(title)
    filename = f"{item_type}_{safe_title}.md"
    file_path = inbox_path / filename

    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"Item not found: {file_path}")

    # Read the current content
    content = file_path.read_text()

    # Update the status field in frontmatter
    import re

    # Check if status field exists
    if re.search(r'^status:', content, re.MULTILINE):
        # Update existing status field
        updated_content = re.sub(
            r'^status:\s*[\w-]+$',
            f'status: {new_status}',
            content,
            count=1,
            flags=re.MULTILINE
        )
    else:
        # Add status field after type field
        updated_content = re.sub(
            r'^(type:\s*\w+)$',
            f'\\1\nstatus: {new_status}',
            content,
            count=1,
            flags=re.MULTILINE
        )

    # Handle status-note field
    if status_note:
        # Check if status-note already exists
        if re.search(r'^status-note:', updated_content, re.MULTILINE):
            # Update existing note
            updated_content = re.sub(
                r'^status-note:.*$',
                f'status-note: {status_note}',
                updated_content,
                count=1,
                flags=re.MULTILINE
            )
        else:
            # Add new note after status line
            updated_content = re.sub(
                r'^(status: [\w-]+)$',
                f'\\1\nstatus-note: {status_note}',
                updated_content,
                count=1,
                flags=re.MULTILINE
            )
    else:
        # Remove status-note if it exists and no new note provided
        updated_content = re.sub(
            r'^status-note:.*\n',
            '',
            updated_content,
            count=1,
            flags=re.MULTILINE
        )

    # Write back the updated content
    file_path.write_text(updated_content)

    return file_path


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Create tasks, ideas, or features in the Obsidian Inbox"
    )

    parser.add_argument(
        'type',
        choices=['task', 'idea', 'feature'],
        help='Type of item to create'
    )

    parser.add_argument(
        'title',
        help='Title of the item'
    )

    parser.add_argument(
        '--due',
        help='Due date for tasks (YYYY-MM-DD format)',
        default=None
    )

    parser.add_argument(
        '--details',
        help='Detailed description',
        default=""
    )

    parser.add_argument(
        '--tags',
        help='Comma-separated tags',
        default=""
    )

    args = parser.parse_args()

    # Parse tags
    tags = parse_tags(args.tags) if args.tags else []

    try:
        # Create the item
        file_path = create_item(
            item_type=args.type,
            title=args.title,
            due_date=args.due,
            details=args.details,
            tags=tags
        )

        print(f"✓ Created {args.type}: {file_path}")
        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
