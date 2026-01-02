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


def create_frontmatter(item_type, due_date=None, tags=None):
    """
    Generate YAML frontmatter for the file.

    Args:
        item_type: Type of item ('task', 'idea', or 'feature')
        due_date: Due date string (YYYY-MM-DD) or None
        tags: List of tag strings or None

    Returns:
        Formatted frontmatter string
    """
    tags_formatted = format_tags_yaml(tags) if tags else "[]"

    # For tasks with due dates
    if item_type == 'task' and due_date:
        frontmatter = f"""---
type: {item_type}
due-date: {due_date}
tags: {tags_formatted}
---"""
    # For tasks without due dates, ideas, and features
    else:
        frontmatter = f"""---
type: {item_type}
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
    Create a new task, idea, or feature file.

    Args:
        item_type: Type of item ('task', 'idea', or 'feature')
        title: Title of the item
        due_date: Due date (YYYY-MM-DD) for tasks, optional
        details: Detailed description
        tags: List of tag strings

    Returns:
        Path to the created file
    """
    # Validate inputs
    if item_type not in ['task', 'idea', 'feature']:
        raise ValueError(f"Invalid item type: {item_type}. Must be 'task', 'idea', or 'feature'.")

    if item_type == 'task' and due_date and not validate_date(due_date):
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
