#!/usr/bin/env python3
"""
Generate daily and weekly summaries of tasks, ideas, and features.

Usage:
    python summary.py today
    python summary.py weekly
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta
import re

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils import get_vault_path


def parse_frontmatter(content):
    """
    Parse YAML frontmatter from a markdown file.

    Args:
        content: Full file content as string

    Returns:
        Dictionary of frontmatter fields
    """
    frontmatter = {}

    # Extract frontmatter block
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return frontmatter

    fm_content = match.group(1)

    # Parse each line
    for line in fm_content.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Handle special values
            if value.lower() == 'null':
                value = None
            elif value.startswith('[') and value.endswith(']'):
                # Parse tags array
                tags_str = value[1:-1]
                if tags_str:
                    value = [tag.strip() for tag in tags_str.split(',')]
                else:
                    value = []

            frontmatter[key] = value

    return frontmatter


def get_file_title(content):
    """
    Extract the title from markdown content.

    Args:
        content: Full file content as string

    Returns:
        Title string or empty string
    """
    # Look for the first # heading after frontmatter
    lines = content.split('\n')
    in_frontmatter = False

    for line in lines:
        if line.strip() == '---':
            in_frontmatter = not in_frontmatter
            continue

        if not in_frontmatter and line.startswith('#'):
            # Extract title text
            title = line.lstrip('#').strip()
            return title

    return ""


def get_items_from_folder(folder_path):
    """
    Get all items from a folder with their metadata.

    Args:
        folder_path: Path to the folder to scan

    Returns:
        List of dictionaries with item data
    """
    items = []

    if not folder_path.exists():
        return items

    for file_path in folder_path.glob('*.md'):
        # Skip summary files
        if file_path.name.startswith('today_') or file_path.name.startswith('weekly_'):
            continue

        content = file_path.read_text()
        frontmatter = parse_frontmatter(content)
        title = get_file_title(content)

        # Get file creation/modification time
        created_time = datetime.fromtimestamp(file_path.stat().st_birthtime)
        modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)

        items.append({
            'file_path': file_path,
            'file_name': file_path.name,
            'title': title,
            'frontmatter': frontmatter,
            'created': created_time,
            'modified': modified_time
        })

    return items


def generate_today_summary():
    """
    Generate today's summary.

    Returns:
        Tuple of (file_path, content)
    """
    vault_path = get_vault_path()
    inbox_path = vault_path / "Inbox"
    today = datetime.now().date()

    # Get all items
    tasks = get_items_from_folder(inbox_path / "Tasks")
    ideas = get_items_from_folder(inbox_path / "Ideas")
    features = get_items_from_folder(inbox_path / "Features")

    # Filter tasks due today (include completed/archived with status tracking)
    tasks_due_today_active = []
    tasks_due_today_completed = []
    for task in tasks:
        status = task['frontmatter'].get('status', 'active')
        due_date_str = task['frontmatter'].get('due-date')
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                if due_date == today:
                    if status in ['completed', 'archived']:
                        tasks_due_today_completed.append(task)
                    else:
                        tasks_due_today_active.append(task)
            except ValueError:
                pass

    # Filter tasks due this week (next 7 days, excluding today, only active)
    tasks_due_this_week = []
    week_end = today + timedelta(days=7)
    for task in tasks:
        status = task['frontmatter'].get('status', 'active')
        if status in ['completed', 'archived']:
            continue

        due_date_str = task['frontmatter'].get('due-date')
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                if today < due_date <= week_end:
                    tasks_due_this_week.append(task)
            except ValueError:
                pass

    # Sort tasks by due date
    tasks_due_this_week.sort(key=lambda x: x['frontmatter'].get('due-date', ''))

    # Filter ideas by status (active and completed separately)
    ideas_active = [idea for idea in ideas if idea['frontmatter'].get('status', 'active') not in ['completed', 'archived']]
    ideas_completed = [idea for idea in ideas if idea['frontmatter'].get('status', 'active') in ['completed', 'archived']]

    # Filter features by status (active and completed separately)
    features_active = [feature for feature in features if feature['frontmatter'].get('status', 'active') not in ['completed', 'archived']]
    features_completed = [feature for feature in features if feature['frontmatter'].get('status', 'active') in ['completed', 'archived']]

    # Generate summary content
    content = f"""# Daily Summary - {today.strftime('%B %d, %Y')}

## Tasks Due Today

"""

    # Show active tasks first, then completed with strikethrough
    if tasks_due_today_active or tasks_due_today_completed:
        for task in tasks_due_today_active:
            content += f"- {task['title']}\n"
        for task in tasks_due_today_completed:
            content += f"- ~~{task['title']}~~\n"
    else:
        content += "*No tasks due today*\n"

    content += "\n## Tasks Due This Week\n\n"

    if tasks_due_this_week:
        for task in tasks_due_this_week:
            due_date = task['frontmatter'].get('due-date', 'No date')
            content += f"- **{due_date}**: {task['title']}\n"
    else:
        content += "*No tasks due this week*\n"

    content += "\n## Recent Ideas\n\n"

    if ideas_active or ideas_completed:
        for idea in ideas_active:
            content += f"- {idea['title']}\n"
        for idea in ideas_completed:
            content += f"- ~~{idea['title']}~~\n"
    else:
        content += "*No active ideas*\n"

    content += "\n## Recent Features\n\n"

    if features_active or features_completed:
        for feature in features_active:
            content += f"- {feature['title']}\n"
        for feature in features_completed:
            content += f"- ~~{feature['title']}~~\n"
    else:
        content += "*No active features*\n"

    # Create file path in Today folder
    today_folder = inbox_path / "Today"
    today_folder.mkdir(exist_ok=True)  # Create folder if it doesn't exist
    file_name = f"today_{today.strftime('%Y-%m-%d')}.md"
    file_path = today_folder / file_name

    return file_path, content


def update_today_document():
    """
    Update today's document with current summary.
    This is called automatically after creating tasks/ideas/features.

    Returns:
        Path to the updated today document
    """
    file_path, content = generate_today_summary()
    file_path.write_text(content)
    return file_path


def generate_weekly_summary():
    """
    Generate weekly summary.

    Returns:
        Tuple of (file_path, content)
    """
    vault_path = get_vault_path()
    inbox_path = vault_path / "Inbox"
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)

    # Get all items
    tasks = get_items_from_folder(inbox_path / "Tasks")
    ideas = get_items_from_folder(inbox_path / "Ideas")
    features = get_items_from_folder(inbox_path / "Features")

    # Filter items from last 7 days
    tasks_this_week = [t for t in tasks if t['created'].date() > week_ago]
    ideas_this_week = [i for i in ideas if i['created'].date() > week_ago]
    features_this_week = [f for f in features if f['created'].date() > week_ago]

    # Sort tasks by due date
    tasks_this_week.sort(key=lambda x: x['frontmatter'].get('due-date', '9999-99-99'))

    # Generate summary content
    content = f"""# Weekly Summary - {week_ago.strftime('%B %d')} to {today.strftime('%B %d, %Y')}

## Tasks This Week

"""

    if tasks_this_week:
        for task in tasks_this_week:
            due_date = task['frontmatter'].get('due-date', 'No due date')
            content += f"- **{due_date}**: {task['title']}\n"
    else:
        content += "*No tasks created this week*\n"

    content += "\n## Ideas This Week\n\n"

    if ideas_this_week:
        for idea in ideas_this_week:
            content += f"- {idea['title']}\n"
    else:
        content += "*No ideas created this week*\n"

    content += "\n## Features This Week\n\n"

    if features_this_week:
        for feature in features_this_week:
            content += f"- {feature['title']}\n"
    else:
        content += "*No features created this week*\n"

    content += f"\n## Activity Summary\n\n"
    content += f"- **Total Tasks**: {len(tasks_this_week)}\n"
    content += f"- **Total Ideas**: {len(ideas_this_week)}\n"
    content += f"- **Total Features**: {len(features_this_week)}\n"
    content += f"- **Total Items**: {len(tasks_this_week) + len(ideas_this_week) + len(features_this_week)}\n"

    # Create file path
    file_name = f"weekly_summary_{today.strftime('%Y-%m-%d')}.md"
    file_path = inbox_path / file_name

    return file_path, content


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Generate daily or weekly summaries"
    )

    parser.add_argument(
        'type',
        choices=['today', 'weekly'],
        help='Type of summary to generate'
    )

    args = parser.parse_args()

    try:
        if args.type == 'today':
            file_path, content = generate_today_summary()
        else:
            file_path, content = generate_weekly_summary()

        # Write the summary file
        file_path.write_text(content)

        print(f"✓ Generated {args.type} summary: {file_path}")
        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
