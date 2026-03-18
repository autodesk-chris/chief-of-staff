#!/usr/bin/env python3
"""
List items from inbox folders with filtering and formatting.

Supports listing actions, decisions, and other item types with relevant metadata.
"""

import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def parse_frontmatter(content: str) -> Dict:
    """
    Parse YAML frontmatter from markdown content.

    Args:
        content: Full file content

    Returns:
        Dictionary of frontmatter fields
    """
    frontmatter = {}

    # Check for frontmatter delimiters
    if not content.startswith('---'):
        return frontmatter

    # Find end of frontmatter
    end_match = content.find('---', 3)
    if end_match == -1:
        return frontmatter

    fm_content = content[3:end_match].strip()

    # Parse each line
    for line in fm_content.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Handle null/empty values
            if value.lower() in ['null', '']:
                value = None
            # Handle arrays
            elif value.startswith('[') and value.endswith(']'):
                # Simple array parsing
                inner = value[1:-1].strip()
                if inner:
                    value = [v.strip().strip('"\'') for v in inner.split(',')]
                else:
                    value = []

            frontmatter[key] = value

    return frontmatter


def list_actions(status_filter: Optional[str] = None, assignee_filter: Optional[str] = None) -> Dict:
    """
    List all actions with their assignee and due date.

    Args:
        status_filter: Filter by status (e.g., 'active', 'completed')
        assignee_filter: Filter by assignee name (partial match)

    Returns:
        Dictionary with 'actions' list and 'summary' string
    """
    project_root = get_project_root()
    actions_folder = project_root / 'Work' / 'Inbox' / 'Actions'

    if not actions_folder.exists():
        return {'actions': [], 'summary': 'No actions folder found'}

    actions = []

    for file_path in actions_folder.glob('*.md'):
        content = file_path.read_text()
        frontmatter = parse_frontmatter(content)

        # Extract title from content
        title_match = re.search(r'^#\s*Action:\s*(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else file_path.stem

        status = frontmatter.get('status', 'active')
        assignee = frontmatter.get('assignee', 'Unassigned')
        due_date = frontmatter.get('due-date')

        # Apply filters
        if status_filter and status != status_filter:
            continue
        if assignee_filter and assignee_filter.lower() not in (assignee or '').lower():
            continue

        actions.append({
            'title': title,
            'assignee': assignee,
            'due_date': due_date,
            'status': status,
            'file': file_path.name
        })

    # Sort by due date (items with dates first, then by date)
    def sort_key(a):
        if a['due_date']:
            return (0, a['due_date'])
        return (1, '')

    actions.sort(key=sort_key)

    # Build summary
    if not actions:
        summary = "No actions found"
        if status_filter:
            summary += f" with status '{status_filter}'"
        if assignee_filter:
            summary += f" for '{assignee_filter}'"
    else:
        lines = [f"**Actions ({len(actions)})**\n"]

        for action in actions:
            due_str = f" (due: {action['due_date']})" if action['due_date'] else ""
            status_str = f" [{action['status']}]" if action['status'] != 'active' else ""
            assignee_str = f" - {action['assignee']}" if action['assignee'] else ""
            lines.append(f"- {action['title']}{assignee_str}{due_str}{status_str}")

        summary = '\n'.join(lines)

    return {'actions': actions, 'summary': summary}


def list_decisions(date_filter: Optional[str] = None) -> Dict:
    """
    List all decisions.

    Args:
        date_filter: Filter by date (YYYY-MM format for month, YYYY for year)

    Returns:
        Dictionary with 'decisions' list and 'summary' string
    """
    project_root = get_project_root()
    decisions_folder = project_root / 'Work' / 'Decisions'

    if not decisions_folder.exists():
        return {'decisions': [], 'summary': 'No decisions recorded yet'}

    decisions = []

    for file_path in decisions_folder.glob('*.md'):
        content = file_path.read_text()
        frontmatter = parse_frontmatter(content)

        # Extract title from content
        title_match = re.search(r'^#\s*Decision:\s*(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else file_path.stem

        date_decided = frontmatter.get('date-decided')
        participants = frontmatter.get('participants')
        rationale = frontmatter.get('rationale')

        # Apply date filter
        if date_filter and date_decided:
            if not date_decided.startswith(date_filter):
                continue
        elif date_filter and not date_decided:
            continue

        decisions.append({
            'title': title,
            'date_decided': date_decided,
            'participants': participants,
            'rationale': rationale,
            'file': file_path.name
        })

    # Sort by date (most recent first)
    def sort_key(d):
        if d['date_decided']:
            return d['date_decided']
        return '0000-00-00'

    decisions.sort(key=sort_key, reverse=True)

    # Build summary
    if not decisions:
        summary = "No decisions recorded"
        if date_filter:
            summary += f" for '{date_filter}'"
    else:
        lines = [f"**Decisions ({len(decisions)})**\n"]

        for decision in decisions:
            date_str = f" ({decision['date_decided']})" if decision['date_decided'] else ""
            participants_str = f" - {decision['participants']}" if decision['participants'] else ""
            lines.append(f"- {decision['title']}{date_str}{participants_str}")

        summary = '\n'.join(lines)

    return {'decisions': decisions, 'summary': summary}


def change_due_date(title: str, new_date: str) -> Dict:
    """
    Change the due date of an item.

    Args:
        title: Title or partial title to match
        new_date: New due date (YYYY-MM-DD format)

    Returns:
        Dictionary with 'success', 'file', 'old_date', 'new_date', 'message'
    """
    from utils import find_item_by_title, validate_date

    # Validate date format
    if not validate_date(new_date):
        return {
            'success': False,
            'message': f"Invalid date format: {new_date}. Use YYYY-MM-DD."
        }

    # Find matching items
    matches = find_item_by_title(title)

    if not matches:
        return {
            'success': False,
            'message': f"No items found matching: '{title}'"
        }

    # Handle multiple matches
    if len(matches) > 1:
        best_score = matches[0][3]
        second_score = matches[1][3]

        if best_score - second_score < 0.2:
            # Ambiguous - show options
            options = "\n".join([
                f"  {i}. [{m[0]}] {m[2]} (match: {m[3]:.0%})"
                for i, m in enumerate(matches[:5], 1)
            ])
            return {
                'success': False,
                'message': f"Multiple items found. Please be more specific:\n{options}"
            }

    item_type, file_path, file_title, score = matches[0]

    # Check if item type supports due dates
    if item_type not in ['task', 'action', 'reminder']:
        return {
            'success': False,
            'message': f"{item_type.capitalize()}s don't have due dates. Only tasks, actions, and reminders support due dates."
        }

    # Read current content
    file_path = Path(file_path)
    content = file_path.read_text()
    frontmatter = parse_frontmatter(content)

    old_date = frontmatter.get('due-date') or frontmatter.get('reminder-date')
    date_field = 'reminder-date' if item_type == 'reminder' else 'due-date'

    # Update the date in frontmatter
    if re.search(rf'^{date_field}:', content, re.MULTILINE):
        # Update existing field
        updated_content = re.sub(
            rf'^{date_field}:\s*.*$',
            f'{date_field}: {new_date}',
            content,
            count=1,
            flags=re.MULTILINE
        )
    else:
        # Add date field after status
        updated_content = re.sub(
            r'^(status:\s*[\w-]+)$',
            f'\\1\n{date_field}: {new_date}',
            content,
            count=1,
            flags=re.MULTILINE
        )

    # Write back
    file_path.write_text(updated_content)

    old_str = old_date if old_date else 'none'
    return {
        'success': True,
        'file': str(file_path),
        'title': file_title,
        'item_type': item_type,
        'old_date': old_date,
        'new_date': new_date,
        'message': f"Changed {item_type} '{file_title}' due date: {old_str} → {new_date}"
    }


def add_daily_note(note: str) -> Dict:
    """
    Add a contribution note for the daily summary.

    Notes are appended to the daily notes file for later inclusion in daily summary.

    Args:
        note: The note text to add

    Returns:
        Dictionary with 'success', 'file', 'message'
    """
    project_root = get_project_root()
    today = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%H:%M')

    # Store in Daily_Logs folder
    logs_folder = project_root / 'Work' / 'Daily_Logs'
    logs_folder.mkdir(parents=True, exist_ok=True)

    notes_file = logs_folder / f'daily_notes_{today}.md'

    # Create or append to file
    if notes_file.exists():
        content = notes_file.read_text()
    else:
        content = f"""---
date: {today}
type: daily-notes
---

# Daily Notes - {today}

"""

    # Append the new note with timestamp
    content += f"\n## {time_str}\n\n{note}\n"

    notes_file.write_text(content)

    return {
        'success': True,
        'file': str(notes_file),
        'message': f"Added note to daily log: {notes_file.name}"
    }


# Test function
if __name__ == '__main__':
    print("Testing list_actions:")
    result = list_actions()
    print(result['summary'])

    print("\n\nTesting list_decisions:")
    result = list_decisions()
    print(result['summary'])
