#!/usr/bin/env python3
"""
Generate daily to-do list and weekly summaries of tasks, ideas, and features.

Usage:
    python todo.py today
    python todo.py weekly
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta
import re

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils import get_vault_path


def load_team_members():
    """Load team member names from the squads overview file.

    Returns a set of lowercase first+last name strings for matching against action assignees.
    """
    squads_file = Path(__file__).parent.parent / "Work" / "LLM_Context" / "Squads" / "Squads_overview.md"
    if not squads_file.exists():
        return set()

    members = set()
    in_members_section = False
    content = squads_file.read_text()
    for line in content.splitlines():
        if line.strip() == "## Growth Organisation members":
            in_members_section = True
            continue
        if in_members_section:
            if line.startswith("## ") and "Growth Organisation" not in line:
                break
            if line.startswith("- ") and not line.startswith("- **"):
                name = line.lstrip("- ").strip()
                if name:
                    members.add(name.lower())
    return members


def is_team_member(assignee, team_members):
    """Check if an assignee matches a team member (fuzzy first-name or full-name match)."""
    if not team_members or not assignee or assignee.lower() == 'unassigned':
        return True  # Show unassigned actions
    assignee_lower = assignee.lower()
    assignee_first = assignee_lower.split()[0] if assignee_lower else ''
    for member in team_members:
        member_first = member.split()[0] if member else ''
        # Full name match or first name match (either direction)
        if assignee_lower == member or assignee_first == member_first:
            return True
    return False


def get_previous_working_day(today):
    """
    Get the most recent prior day that has a daily summary file.

    Walks back up to 7 days from yesterday and returns the first date with a
    daily_summary_YYYY-MM-DD.md or claude_sessions_YYYY-MM-DD.md file in
    Work/Daily_Logs/. Falls back to a weekday-aware default (Monday -> Friday,
    otherwise yesterday) if no log file is found in the window.

    Args:
        today: datetime.date object for today

    Returns:
        datetime.date object for previous working day
    """
    logs_dir = Path(__file__).parent.parent / "Work" / "Daily_Logs"
    candidate = today - timedelta(days=1)
    for _ in range(7):
        if logs_dir.exists():
            ds = logs_dir / f"daily_summary_{candidate.isoformat()}.md"
            cs = logs_dir / f"claude_sessions_{candidate.isoformat()}.md"
            if ds.exists() or cs.exists():
                return candidate
        candidate = candidate - timedelta(days=1)
    # Fallback: Monday -> Friday, else yesterday
    if today.weekday() == 0:
        return today - timedelta(days=3)
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
    summary_path = vault_path / "Daily_Logs" / f"daily_summary_{previous_date.strftime('%Y-%m-%d')}.md"

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

    # Pattern to match checked checkbox items: - [x] Title
    import re
    pattern = r'^-\s+\[x\]\s+(.+?)$'

    for line in content.split('\n'):
        match = re.match(pattern, line.strip(), re.IGNORECASE)
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
                status_note='Marked complete in today document',
                file_path=file_path
            )
            updated_count += 1
            print(f"✓ Synced manual completion: {item_type} '{file_title}'")
        except Exception as e:
            print(f"⚠ Error updating {item_type} '{file_title}': {e}")

    return updated_count


def parse_manual_deletions(today_path):
    """
    Parse existing today document to find external actions marked for deletion.

    Looks for checked delete markers in the format:
      - [x] 🗑 Remove <!-- file:filename.md -->

    Args:
        today_path: Path to the today document

    Returns:
        List of filenames to delete
    """
    if not today_path.exists():
        return []

    content = today_path.read_text(encoding='utf-8')
    deletions = []

    pattern = r'-\s+\[x\]\s+🗑\s+Remove\s+<!--\s+file:(.+?)\s+-->'
    for match in re.finditer(pattern, content, re.IGNORECASE):
        deletions.append(match.group(1).strip())

    return deletions


def sync_manual_deletions(filenames_to_delete):
    """
    Delete action files that were marked for removal in today document.

    Args:
        filenames_to_delete: List of filenames (e.g., 'action_Foo.md')

    Returns:
        Number of files deleted
    """
    vault_path = get_vault_path()
    actions_folder = vault_path / "Inbox" / "Actions"
    deleted = 0

    for filename in filenames_to_delete:
        file_path = actions_folder / filename
        if file_path.exists():
            file_path.unlink()
            print(f"🗑 Deleted external action: {filename}")
            deleted += 1
        else:
            print(f"⚠ Could not find file to delete: {filename}")

    return deleted


def get_item_details(content):
    """
    Extract the details section from markdown content.

    Args:
        content: Full file content as string

    Returns:
        Details string (first paragraph after ## Details), or empty string
    """
    lines = content.split('\n')
    in_details = False
    details_lines = []

    for line in lines:
        if line.strip().startswith('## Details'):
            in_details = True
            continue
        if in_details:
            # Stop at next heading or end of content
            if line.startswith('## ') or line.startswith('# '):
                break
            stripped = line.strip()
            if stripped:
                details_lines.append(stripped)

    details = ' '.join(details_lines).strip()
    # Remove due date references from details
    details = re.sub(r'\s*due:\s*\d{4}-\d{2}-\d{2}\s*', '', details).strip()
    return details


def extract_sections_from_md(md_path, section_names):
    """Read an existing todo .md and extract verbatim section bodies by name.

    Returns a dict {section_name: full_section_block_including_header_and_body}.
    Used by generate_todo() to preserve skill-curated sections (Pinned, Focus today,
    Yesterday's overview) across same-day regenerations.
    """
    if not md_path.exists():
        return {}

    result = {}
    lines = md_path.read_text().splitlines()
    current = None
    buffer = []
    for line in lines:
        if line.startswith("## "):
            if current is not None and current in section_names:
                while buffer and not buffer[-1].strip():
                    buffer.pop()
                result[current] = "\n".join(buffer) + "\n\n"
            header = line[3:].split(" (", 1)[0].strip()
            current = header
            buffer = [line]
        elif current is not None:
            buffer.append(line)
    if current is not None and current in section_names:
        while buffer and not buffer[-1].strip():
            buffer.pop()
        result[current] = "\n".join(buffer) + "\n\n"
    return {k: v for k, v in result.items() if k in section_names}


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
        if file_path.name.startswith('todo_') or file_path.name.startswith('today_') or file_path.name.startswith('weekly_'):
            continue

        content = file_path.read_text()
        frontmatter = parse_frontmatter(content)
        title = get_file_title(content)

        # Skip archived items always; skip completed items UNLESS completed today
        # (so ticking a box in the dashboard keeps the item visible-and-ticked for the rest of today)
        status = frontmatter.get('status')
        if status == 'archived':
            continue
        if status == 'completed':
            completed_date_str = frontmatter.get('completed-date', '')
            today_iso = datetime.now().date().isoformat()
            if completed_date_str != today_iso:
                continue

        # Get file creation/modification time
        created_time = datetime.fromtimestamp(file_path.stat().st_birthtime)
        modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)

        details = get_item_details(content)

        items.append({
            'file_path': file_path,
            'file_name': file_path.name,
            'title': title,
            'frontmatter': frontmatter,
            'details': details,
            'created': created_time,
            'modified': modified_time
        })

    return items


def _format_item_line(item, checkbox=" "):
    """
    Format a single item as a checkbox line with optional details.

    Args:
        item: Item dict with 'title' and 'details'
        checkbox: Checkbox content, e.g. ' ' or 'x'

    Returns:
        Formatted string (may be multi-line if details present)
    """
    line = f"- [{checkbox}] **{item['title']}**"
    details = item.get('details', '')
    if details:
        # Truncate long details to keep summary scannable
        if len(details) > 200:
            details = details[:197] + '...'
        line += f"\n  - *{details}*"
    return line


def _format_tasks_by_day(tasks):
    """
    Group tasks by due date and format with day-name subheadings.

    Args:
        tasks: List of task dicts with frontmatter containing 'due-date'

    Returns:
        Formatted string with tasks grouped under day subheadings
    """
    from collections import OrderedDict

    day_abbrevs = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    grouped = OrderedDict()

    for task in tasks:
        due_date_str = task['frontmatter'].get('due-date', '')
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            day_name = day_abbrevs[due_date.weekday()]
            key = f"{day_name} {due_date_str}"
        except (ValueError, TypeError):
            key = "No date"

        if key not in grouped:
            grouped[key] = []
        grouped[key].append(task)

    result = ""
    for day_heading, day_tasks in grouped.items():
        result += f"### {day_heading}\n"
        for task in day_tasks:
            status = task['frontmatter'].get('status', 'active')
            cb = "x" if status in ['completed', 'archived'] else " "
            result += _format_item_line(task, cb) + "\n"
        result += "\n"

    return result


def generate_todo():
    """
    Generate today's to-do list.

    Returns:
        Tuple of (file_path, content)
    """
    vault_path = get_vault_path()
    inbox_path = vault_path / "Inbox"
    today = datetime.now().date()

    # Sync manual completions from existing today document (if it exists)
    today_folder = inbox_path / "Today"
    today_path = today_folder / f"todo_{today.strftime('%Y-%m-%d')}.md"

    # Preserve skill-curated sections from any existing today.md (Pinned, Focus today,
    # Yesterday's overview). These are added by Claude during the /todo skill and would
    # otherwise be wiped by regeneration.
    preserved_sections = extract_sections_from_md(today_path, {"Pinned", "Focus today", "Yesterday's overview"})

    # Sync manual completions from the most recent prior todo on disk before generating today's.
    # Covers the common case where boxes are ticked end-of-day and /todo is next run a day or more later.
    prior_todos = sorted(
        (p for p in today_folder.glob("todo_*.md") if p.name != today_path.name),
        reverse=True,
    )
    if prior_todos:
        prior_path = prior_todos[0]
        prior_completed = parse_manual_completions(prior_path)
        if prior_completed:
            print(f"\n📝 Syncing {len(prior_completed)} manual completion(s) from {prior_path.name}...")
            updated = sync_manual_completions_to_source(prior_completed)
            if updated > 0:
                print(f"✓ Synced {updated} item(s) from {prior_path.name}\n")

        prior_deletions = parse_manual_deletions(prior_path)
        if prior_deletions:
            print(f"\n🗑 Processing {len(prior_deletions)} deletion(s) from {prior_path.name}...")
            deleted = sync_manual_deletions(prior_deletions)
            if deleted > 0:
                print(f"✓ Deleted {deleted} external action(s)\n")

    if today_path.exists():
        manually_completed = parse_manual_completions(today_path)
        if manually_completed:
            print(f"\n📝 Syncing {len(manually_completed)} manual completion(s) from today document...")
            updated = sync_manual_completions_to_source(manually_completed)
            if updated > 0:
                print(f"✓ Synced {updated} item(s) to source files\n")

        manual_deletions = parse_manual_deletions(today_path)
        if manual_deletions:
            print(f"\n🗑 Processing {len(manual_deletions)} deletion(s)...")
            deleted = sync_manual_deletions(manual_deletions)
            if deleted > 0:
                print(f"✓ Deleted {deleted} external action(s)\n")

    # Get previous working day overview
    previous_date = get_previous_working_day(today)
    previous_overview = read_previous_day_summary(previous_date)

    # Get all items
    tasks = get_items_from_folder(inbox_path / "Tasks")
    ideas = get_items_from_folder(inbox_path / "Ideas")
    features = get_items_from_folder(inbox_path / "Features")
    actions = get_items_from_folder(inbox_path / "Actions")

    # Get reminders
    reminders = get_items_from_folder(inbox_path / "Reminders")

    # Identify pinned tasks: pinned=true, not completed, and due date <= today
    pinned_tasks = []
    pinned_paths = set()
    for task in tasks:
        fm = task['frontmatter']
        if str(fm.get('pinned', '')).lower() != 'true':
            continue
        if fm.get('status', 'active') in ['completed', 'archived']:
            continue
        due_date_str = fm.get('due-date')
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                if due_date > today:
                    continue
            except ValueError:
                pass
        pinned_tasks.append(task)
        pinned_paths.add(task['file_path'])

    # Filter reminders (due today or upcoming, and overdue; include items completed today)
    reminders_today = []
    reminders_upcoming = []
    reminders_overdue = []
    week_end_rem = today + timedelta(days=7)
    for reminder in reminders:
        status = reminder['frontmatter'].get('status', 'active')
        if status in ['completed', 'archived']:
            # Keep if completed today, otherwise hide
            completed_date_str = reminder['frontmatter'].get('completed-date', '')
            try:
                completed_date = datetime.strptime(completed_date_str, '%Y-%m-%d').date()
                if completed_date != today:
                    continue
            except (ValueError, TypeError):
                continue
        # Check reminder-date or due-date
        date_str = reminder['frontmatter'].get('reminder-date') or reminder['frontmatter'].get('due-date')
        if date_str:
            try:
                rem_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                if rem_date < today:
                    reminders_overdue.append(reminder)
                elif rem_date == today:
                    reminders_today.append(reminder)
                elif rem_date <= week_end_rem:
                    reminders_upcoming.append(reminder)
            except ValueError:
                reminders_today.append(reminder)  # No valid date, show today
        else:
            reminders_today.append(reminder)  # No date, show today

    # Filter overdue tasks (due before today; include items completed today so they stay checked)
    overdue_tasks = []
    for task in tasks:
        status = task['frontmatter'].get('status', 'active')
        if status in ['completed', 'archived']:
            # Keep if completed today, otherwise hide
            completed_date_str = task['frontmatter'].get('completed-date', '')
            try:
                completed_date = datetime.strptime(completed_date_str, '%Y-%m-%d').date()
                if completed_date != today:
                    continue
            except (ValueError, TypeError):
                continue

        due_date_str = task['frontmatter'].get('due-date')
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                if due_date < today:
                    if task['file_path'] not in pinned_paths:
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
                    if task['file_path'] in pinned_paths:
                        continue
                    if status in ['completed', 'archived']:
                        tasks_due_today_completed.append(task)
                    else:
                        tasks_due_today_active.append(task)
            except ValueError:
                pass

    # Filter tasks due this week (next 7 days, excluding today; include items completed today)
    tasks_due_this_week = []
    week_end = today + timedelta(days=7)
    for task in tasks:
        status = task['frontmatter'].get('status', 'active')
        if status in ['completed', 'archived']:
            # Keep if completed today, otherwise hide
            completed_date_str = task['frontmatter'].get('completed-date', '')
            try:
                completed_date = datetime.strptime(completed_date_str, '%Y-%m-%d').date()
                if completed_date != today:
                    continue
            except (ValueError, TypeError):
                continue

        due_date_str = task['frontmatter'].get('due-date')
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                if today < due_date <= week_end:
                    if task['file_path'] not in pinned_paths:
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
    day_abbrevs = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    today_day_name = day_abbrevs[today.weekday()]
    content = f"""# Daily to-do - {today_day_name} {today.strftime('%Y-%m-%d')}

"""

    # Pinned section: prefer the skill-curated version from existing today.md if present,
    # otherwise auto-generate from tasks with pinned=true frontmatter.
    if "Pinned" in preserved_sections:
        content += preserved_sections["Pinned"]
    elif pinned_tasks:
        content += "## Pinned\n\n"
        for task in pinned_tasks:
            content += _format_item_line(task, " ") + "\n"
        content += "\n"

    # Focus today: skill-curated, only present if the /todo skill has run today.
    if "Focus today" in preserved_sections:
        content += preserved_sections["Focus today"]

    # Monday: auto-create 4Ps task and show reminder
    if today.weekday() == 0:
        fourps_task_exists = any(
            'complete' in t['frontmatter'].get('title', '').lower()
            and '4ps' in t['frontmatter'].get('title', '').lower()
            and t['frontmatter'].get('due-date') == today.strftime('%Y-%m-%d')
            and t['frontmatter'].get('status', 'active') not in ['completed', 'archived']
            for t in tasks
        )
        if not fourps_task_exists:
            import subprocess
            subprocess.run(
                ['python3', str(Path(__file__).parent / 'create_item.py'),
                 'task', 'Complete weekly 4Ps',
                 '--due', today.strftime('%Y-%m-%d'),
                 '--details', 'Write and submit weekly 4Ps update. Review daily summaries from the past week, gather context, and draft Progress, Plans, Problems, Priorities.',
                 '--tags', 'weekly, reflection'],
                capture_output=True, text=True
            )
            print("📋 Created weekly 4Ps task (Monday auto-reminder)")
            # Reload tasks to include the new one
            tasks = get_items_from_folder(inbox_path / "Tasks")

        # Monday 4Ps reminder is added to the Pinned section by the /todo skill,
        # not as a standalone section here.
        pass

    # Overdue tasks first
    if overdue_tasks:
        content += "## Overdue tasks\n\n"
        content += _format_tasks_by_day(overdue_tasks)

    # Tasks due today
    content += "## Tasks due today\n\n"

    if tasks_due_today_active or tasks_due_today_completed:
        for task in tasks_due_today_active:
            content += _format_item_line(task, " ") + "\n"
        for task in tasks_due_today_completed:
            content += _format_item_line(task, "x") + "\n"
    else:
        content += "*No tasks due today*\n"

    # Tasks due this week
    content += "\n## Tasks due this week\n\n"

    if tasks_due_this_week:
        content += _format_tasks_by_day(tasks_due_this_week)
    else:
        content += "*No tasks due this week*\n\n"

    # Reminders - grouped by date with subheadings
    if reminders_overdue or reminders_today or reminders_upcoming:
        content += "\n## Reminders\n\n"
        all_reminders = reminders_overdue + reminders_today + reminders_upcoming
        from collections import OrderedDict
        rem_grouped = OrderedDict()
        day_abbrevs_rem = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for r in all_reminders:
            date_str = r['frontmatter'].get('reminder-date') or r['frontmatter'].get('due-date', '')
            try:
                rem_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                day_name = day_abbrevs_rem[rem_date.weekday()]
                key = (rem_date, f"{day_name} {date_str}")
            except (ValueError, TypeError):
                key = (datetime.max.date(), "No date")
            if key not in rem_grouped:
                rem_grouped[key] = []
            rem_grouped[key].append(r)
        rem_grouped = OrderedDict(sorted(rem_grouped.items(), key=lambda x: x[0][0]))
        for (rem_date, heading), group_reminders in rem_grouped.items():
            overdue_label = " (overdue)" if rem_date < today else ""
            content += f"### {heading}{overdue_label}\n"
            for r in group_reminders:
                details = r.get('details', '')
                cb = "x" if r['frontmatter'].get('status') in ['completed', 'archived'] else " "
                content += f"- [{cb}] **{r['title']}**\n"
                if details:
                    detail_text = details[:200] + '...' if len(details) > 200 else details
                    content += f"  - *{detail_text}*\n"
            content += "\n"

    # Previous day overview: prefer skill-condensed version if it exists, else raw summary
    if "Yesterday's overview" in preserved_sections:
        content += preserved_sections["Yesterday's overview"]
    elif previous_overview:
        day_name = "Friday" if today.weekday() == 0 else "Yesterday"
        content += f"\n## {day_name}'s overview ({previous_date.strftime('%B %d')})\n\n"
        content += f"{previous_overview}\n\n"

    # Active actions (assigned to others) - filtered to team members only, sorted by date
    team_members = load_team_members()
    actions_active = []
    for a in actions:
        status = a['frontmatter'].get('status', 'active')
        if status in ['completed', 'archived']:
            # Keep if completed today
            completed_date_str = a['frontmatter'].get('completed-date', '')
            try:
                completed_date = datetime.strptime(completed_date_str, '%Y-%m-%d').date()
                if completed_date == today:
                    actions_active.append(a)
            except (ValueError, TypeError):
                pass
        else:
            actions_active.append(a)
    actions_team = [a for a in actions_active if is_team_member(a['frontmatter'].get('assignee', 'Unassigned'), team_members)]
    if actions_team:
        # Split into dated and undated
        actions_dated = [a for a in actions_team if a['frontmatter'].get('due-date')]
        actions_undated = [a for a in actions_team if not a['frontmatter'].get('due-date')]

        # Sort dated actions by due date (earliest first)
        actions_dated.sort(key=lambda x: x['frontmatter'].get('due-date', ''))

        content += "\n## Open actions\n\n"
        # Group dated actions by due date with subheadings
        from collections import OrderedDict
        act_grouped = OrderedDict()
        day_abbrevs_act = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for action in actions_dated:
            due_date_str = action['frontmatter'].get('due-date', '')
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                day_name = day_abbrevs_act[due_date.weekday()]
                key = (due_date, f"{day_name} {due_date_str}")
            except (ValueError, TypeError):
                key = (datetime.max.date(), "No date")
            if key not in act_grouped:
                act_grouped[key] = []
            act_grouped[key].append(action)
        act_grouped = OrderedDict(sorted(act_grouped.items(), key=lambda x: x[0][0]))
        for (act_date, heading), group_actions in act_grouped.items():
            overdue_label = " (overdue)" if act_date < today else ""
            content += f"### {heading}{overdue_label}\n"
            for action in group_actions:
                assignee = action['frontmatter'].get('assignee', 'Unassigned')
                details = action.get('details', '')
                cb = "x" if action['frontmatter'].get('status') in ['completed', 'archived'] else " "
                content += f"- [{cb}] **{assignee}**: **{action['title']}**\n"
                if details:
                    detail_text = details[:200] + '...' if len(details) > 200 else details
                    content += f"  - *{detail_text}*\n"
            content += "\n"
        if actions_undated:
            content += "### No due date\n"
            for action in actions_undated:
                assignee = action['frontmatter'].get('assignee', 'Unassigned')
                details = action.get('details', '')
                cb = "x" if action['frontmatter'].get('status') in ['completed', 'archived'] else " "
                content += f"- [{cb}] **{assignee}**: **{action['title']}**\n"
                if details:
                    detail_text = details[:200] + '...' if len(details) > 200 else details
                    content += f"  - *{detail_text}*\n"
            content += "\n"

    # External actions (assigned to people outside the team), sorted by date
    actions_external = [a for a in actions_active if not is_team_member(a['frontmatter'].get('assignee', 'Unassigned'), team_members)]
    if actions_external:
        actions_ext_dated = [a for a in actions_external if a['frontmatter'].get('due-date')]
        actions_ext_undated = [a for a in actions_external if not a['frontmatter'].get('due-date')]
        actions_ext_dated.sort(key=lambda x: x['frontmatter'].get('due-date', ''))

        content += "\n## External actions\n\n"
        if actions_ext_dated:
            from collections import OrderedDict
            ext_grouped = OrderedDict()
            day_abbrevs_ext = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            for action in actions_ext_dated:
                due_date_str = action['frontmatter'].get('due-date', '')
                try:
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                    day_name = day_abbrevs_ext[due_date.weekday()]
                    key = (due_date, f"{day_name} {due_date_str}")
                except (ValueError, TypeError):
                    key = (datetime.max.date(), "No date")
                if key not in ext_grouped:
                    ext_grouped[key] = []
                ext_grouped[key].append(action)
            ext_grouped = OrderedDict(sorted(ext_grouped.items(), key=lambda x: x[0][0]))
            for (ext_date, heading), group_actions in ext_grouped.items():
                overdue_label = " (overdue)" if ext_date < today else ""
                content += f"### {heading}{overdue_label}\n"
                for action in group_actions:
                    assignee = action['frontmatter'].get('assignee', 'Unassigned')
                    details = action.get('details', '')
                    cb = "x" if action['frontmatter'].get('status') in ['completed', 'archived'] else " "
                    content += f"- [{cb}] **{assignee}**: **{action['title']}**\n"
                    if details:
                        detail_text = details[:200] + '...' if len(details) > 200 else details
                        content += f"  - *{detail_text}*\n"
                    content += f"  - [ ] 🗑 Remove <!-- file:{action['file_name']} -->\n"
                content += "\n"
        if actions_ext_undated:
            if actions_ext_dated:
                content += "### No due date\n"
            for action in actions_ext_undated:
                assignee = action['frontmatter'].get('assignee', 'Unassigned')
                details = action.get('details', '')
                cb = "x" if action['frontmatter'].get('status') in ['completed', 'archived'] else " "
                content += f"- [{cb}] **{assignee}**: **{action['title']}**\n"
                if details:
                    detail_text = details[:200] + '...' if len(details) > 200 else details
                    content += f"  - *{detail_text}*\n"
                content += f"  - [ ] 🗑 Remove <!-- file:{action['file_name']} -->\n"
            content += "\n"

    content += "\n## Recent ideas\n\n"

    if ideas_active or ideas_completed:
        for idea in ideas_active:
            content += f"- [ ] {idea['title']}\n"
        for idea in ideas_completed:
            content += f"- [x] {idea['title']}\n"
    else:
        content += "*No active ideas*\n"

    content += "\n## Recent Features\n\n"

    if features_active or features_completed:
        for feature in features_active:
            content += f"- [ ] {feature['title']}\n"
        for feature in features_completed:
            content += f"- [x] {feature['title']}\n"
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
    file_name = f"todo_{today.strftime('%Y-%m-%d')}.md"
    file_path = today_folder / file_name

    return file_path, content


def update_todo_document():
    """
    Update today's to-do list with current state.
    This is called automatically after creating tasks/ideas/features.

    Returns:
        Path to the updated to-do document
    """
    file_path, content = generate_todo()
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
        description="Generate daily to-do list or weekly summaries"
    )

    parser.add_argument(
        'type',
        choices=['today', 'weekly'],
        help='Type of output to generate (today = to-do list, weekly = summary)'
    )

    args = parser.parse_args()

    try:
        if args.type == 'today':
            file_path, content = generate_todo()
        else:
            file_path, content = generate_weekly_summary()

        # Write the file
        file_path.write_text(content)

        print(f"✓ Generated {args.type}: {file_path}")
        return 0

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
