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


def get_previous_working_day(today):
    """
    Get the previous working day date.

    Args:
        today: datetime.date object for today

    Returns:
        datetime.date object for previous working day
    """
    # If today is Monday (weekday 0), return Friday
    if today.weekday() == 0:
        return today - timedelta(days=3)
    # Otherwise return yesterday
    else:
        return today - timedelta(days=1)


def read_previous_day_summary(previous_date):
    """
    Read and format the previous day's summary with comprehensive information.

    Args:
        previous_date: datetime.date object for the previous day

    Returns:
        Formatted string with previous day overview, or None if not found
    """
    vault_path = get_vault_path()
    summary_path = vault_path / "Inbox" / "Today" / f"summary_{previous_date.strftime('%Y-%m-%d')}.md"

    if not summary_path.exists():
        return None

    content = summary_path.read_text(encoding='utf-8')

    # Extract key sections with better organization
    overview_parts = []

    # Parse sections
    lines = content.split('\n')
    current_section = None
    current_header = None
    section_content = []

    # Sections to extract with their display names
    sections_to_extract = {
        '## Meetings': ('Meetings', 15),  # (display name, max items)
        '## Key Decisions': ('Key decisions', 10),
        '## Actions for Growth/Chris': ('Actions', 10),
        '## Other Work': ('Other work', 10),
        '## Tasks Completed Today': ('Completed', 10),
        '## Claude Sessions': ('Claude sessions', 5)
    }

    for line in lines:
        # Check if this is a section header we care about
        is_section_header = False
        for header, (display_name, max_items) in sections_to_extract.items():
            if line.startswith(header):
                # Save previous section if any
                if current_section and section_content:
                    overview_parts.append((current_header, current_section, section_content))
                current_header = header
                current_section = display_name
                section_content = []
                is_section_header = True
                break

        if is_section_header:
            continue

        # Check if we hit a new section we don't care about
        if line.startswith('## ') and current_section:
            # Save current section and reset
            if section_content:
                overview_parts.append((current_header, current_section, section_content))
            current_header = None
            current_section = None
            section_content = []
            continue

        # Collect content for current section
        if current_section and line.strip():
            section_content.append(line.strip())

    # Don't forget the last section
    if current_section and section_content:
        overview_parts.append((current_header, current_section, section_content))

    # Format the overview with section headings
    if not overview_parts:
        return None

    overview = []
    for header, section_name, content_lines in overview_parts:
        # Get max items for this section
        max_items = sections_to_extract.get(header, (None, 999))[1]

        # Filter and limit items
        relevant_lines = [line for line in content_lines[:max_items] if line and not line.startswith('---')]
        if relevant_lines:
            # Add section heading
            overview.append(f"**{section_name}:**")
            overview.extend(relevant_lines)
            overview.append("")  # Add blank line between sections

    return '\n'.join(overview).strip() if overview else None


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


def parse_manual_completions(today_path):
    """
    Parse existing today document to find manually crossed-off items.

    Args:
        today_path: Path to the today document

    Returns:
        List of item titles that have been manually marked as complete (strikethrough)
    """
    if not today_path.exists():
        return []

    content = today_path.read_text(encoding='utf-8')
    manually_completed = []

    # Pattern to match strikethrough items: - ~~Title~~
    import re
    pattern = r'^-\s+~~(.+?)~~\s*$'

    for line in content.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            title = match.group(1).strip()

            # Clean up the title to match source file format:
            # 1. Remove date prefix if present (e.g., "**2026-01-05**: ")
            title = re.sub(r'^\*\*\d{4}-\d{2}-\d{2}\*\*:\s*', '', title)

            # 2. Remove type prefix if present (e.g., "Task: ", "Idea: ", "Feature: ")
            title = re.sub(r'^(Task|Idea|Feature|Action):\s*', '', title)

            manually_completed.append(title)

    return manually_completed


def sync_manual_completions_to_source(manually_completed_titles):
    """
    Update source files for items that were manually crossed off in today document.

    Args:
        manually_completed_titles: List of item titles that were marked complete

    Returns:
        Number of items successfully updated
    """
    from utils import find_item_by_title
    from create_item import update_item_status

    updated_count = 0

    for title in manually_completed_titles:
        # Find the item using fuzzy matching
        matches = find_item_by_title(title)

        if not matches:
            print(f"⚠ Could not find item for manual completion: '{title}'")
            continue

        # Use the best match
        item_type, file_path, file_title, score = matches[0]

        # Check if already completed (to avoid redundant updates)
        content = file_path.read_text(encoding='utf-8')
        frontmatter = parse_frontmatter(content)
        current_status = frontmatter.get('status', 'active')

        if current_status in ['completed', 'archived']:
            # Already marked as complete, skip
            continue

        # Update to completed
        try:
            update_item_status(
                item_type=item_type,
                title=file_title,
                new_status='completed',
                status_note='Marked complete in today document'
            )
            updated_count += 1
            print(f"✓ Synced manual completion: {item_type} '{file_title}'")
        except Exception as e:
            print(f"⚠ Error updating {item_type} '{file_title}': {e}")

    return updated_count


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

    # Sync manual completions from existing today document (if it exists)
    today_folder = inbox_path / "Today"
    today_path = today_folder / f"today_{today.strftime('%Y-%m-%d')}.md"

    if today_path.exists():
        manually_completed = parse_manual_completions(today_path)
        if manually_completed:
            print(f"\n📝 Syncing {len(manually_completed)} manual completion(s) from today document...")
            updated = sync_manual_completions_to_source(manually_completed)
            if updated > 0:
                print(f"✓ Synced {updated} item(s) to source files\n")

    # Get previous working day overview
    previous_date = get_previous_working_day(today)
    previous_overview = read_previous_day_summary(previous_date)

    # Get all items
    tasks = get_items_from_folder(inbox_path / "Tasks")
    ideas = get_items_from_folder(inbox_path / "Ideas")
    features = get_items_from_folder(inbox_path / "Features")

    # Filter overdue tasks (due before today and not completed)
    overdue_tasks = []
    for task in tasks:
        status = task['frontmatter'].get('status', 'active')
        if status in ['completed', 'archived']:
            continue

        due_date_str = task['frontmatter'].get('due-date')
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                if due_date < today:
                    overdue_tasks.append(task)
            except ValueError:
                pass

    # Sort overdue tasks by due date (oldest first)
    overdue_tasks.sort(key=lambda x: x['frontmatter'].get('due-date', ''))

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

    # Generate summary content with previous day overview at the top
    content = f"""# Daily Summary - {today.strftime('%B %d, %Y')}

"""

    # Add previous day overview if available
    if previous_overview:
        day_name = "Friday" if today.weekday() == 0 else "Yesterday"
        content += f"""## {day_name}'s overview ({previous_date.strftime('%B %d')})

{previous_overview}

"""

    # Add overdue tasks section if any exist
    if overdue_tasks:
        content += """## Overdue Tasks

"""
        for task in overdue_tasks:
            due_date = task['frontmatter'].get('due-date', 'No date')
            content += f"- **{due_date}**: {task['title']}\n"
        content += "\n"

    content += """## Tasks Due Today

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

    # Add Slack actions section if slack report exists
    slack_report_path = inbox_path / "Today" / f"slack_report_{today.strftime('%Y-%m-%d')}.md"
    if slack_report_path.exists():
        slack_content = slack_report_path.read_text()
        # Extract the Tasks created section
        tasks_match = re.search(r'## Tasks created\n\n((?:- \[[ x]\] .+\n)+)', slack_content)
        if tasks_match:
            content += "\n## Slack actions\n\n"
            content += tasks_match.group(1)

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
