#!/usr/bin/env python3
"""
4Ps Generator for Julie Agent System

Generates weekly 4Ps (Priorities, Progress, Plans, Problems) draft
by gathering context from multiple sources.

## Workflow
1. Gather context:
   - Previous week's 4Ps (Plans section as baseline for Progress)
   - Daily summaries from this week
   - Session logs from this week
   - Completed tasks
   - Meeting summaries
   - Blocked/open tasks

2. Generate draft with:
   - Priorities: Carry forward (usually stable week-to-week)
   - Progress: Last week's Plans + completed work
   - Plans: Suggested based on open tasks and context
   - Problems: Blocked tasks and challenges

3. Return draft for Claude to review with user
4. Finalize and append to 4Ps file
"""

import os
import re
import glob
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def get_vault_path() -> Path:
    """Get the Obsidian vault path."""
    return Path(__file__).parent.parent / "Work"


def get_previous_week_boundaries() -> Tuple[datetime, datetime]:
    """
    Get previous calendar week boundaries (Monday to Friday).

    Returns:
        Tuple of (prev_monday, prev_friday)
    """
    today = datetime.now()
    # Current week's Monday
    current_monday = today - timedelta(days=today.weekday())
    # Previous week's Monday and Friday
    prev_monday = current_monday - timedelta(days=7)
    prev_friday = prev_monday + timedelta(days=4)
    return prev_monday, prev_friday


def get_current_week_boundaries() -> Tuple[datetime, datetime]:
    """
    Get current calendar week boundaries (Monday to Friday).

    Returns:
        Tuple of (current_monday, current_friday)
    """
    today = datetime.now()
    current_monday = today - timedelta(days=today.weekday())
    current_friday = current_monday + timedelta(days=4)
    return current_monday, current_friday


def get_week_dates() -> Tuple[datetime, datetime, str]:
    """
    Get the current week's date range.

    Returns:
        Tuple of (week_start, week_end, week_label)
    """
    today = datetime.now()
    # Week starts on Monday
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    week_label = f"Week beginning {week_start.strftime('%d %b %Y')}"
    return week_start, week_end, week_label


def read_file_if_exists(filepath: Path) -> Optional[str]:
    """Read file content if it exists."""
    if filepath.exists():
        try:
            return filepath.read_text()
        except Exception as e:
            print(f"  ⚠️  Error reading {filepath}: {e}")
    return None


def get_previous_4ps() -> Dict[str, any]:
    """
    Get the previous week's 4Ps entry.

    Returns:
        Dict with 'priorities', 'plans', 'raw' keys
    """
    vault = get_vault_path()
    fourps_file = vault / "4Ps" / "4Ps_2026.md"

    result = {
        'priorities': [],
        'plans': [],
        'raw': None,
        'found': False
    }

    content = read_file_if_exists(fourps_file)
    if not content:
        return result

    # Find the most recent week entry
    # Pattern: ### Week beginning DD Mon YYYY or ### Week ending DD Month
    week_pattern = r'###\s+Week\s+(?:beginning|ending)\s+\d{1,2}\s+\w+'
    matches = list(re.finditer(week_pattern, content))

    if not matches:
        return result

    # Get the most recent entry (first match after outline)
    last_match = matches[0]
    next_match_start = matches[1].start() if len(matches) > 1 else len(content)

    last_entry = content[last_match.start():next_match_start]
    result['raw'] = last_entry
    result['found'] = True

    # Extract Priorities section
    priorities_match = re.search(r'Priorities\s*\n(.*?)(?=\nProgress|\nPlans|\nProblems|\n###|$)',
                                  last_entry, re.DOTALL | re.IGNORECASE)
    if priorities_match:
        priorities_text = priorities_match.group(1).strip()
        result['priorities'] = [line.strip('- ').strip() for line in priorities_text.split('\n')
                                if line.strip() and line.strip().startswith('-')]

    # Extract Plans section (these become Progress baseline)
    plans_match = re.search(r'Plans\s*\n(.*?)(?=\nProblems|\nLeadership|\n###|$)',
                            last_entry, re.DOTALL | re.IGNORECASE)
    if plans_match:
        plans_text = plans_match.group(1).strip()
        result['plans'] = [line.strip('- ').strip() for line in plans_text.split('\n')
                          if line.strip() and line.strip().startswith('-')]

    return result


def get_daily_summaries(week_start: datetime, week_end: datetime) -> List[Dict]:
    """
    Get daily summaries from this week.

    Returns:
        List of dicts with 'date' and 'content' keys
    """
    vault = get_vault_path()
    summaries = []

    current = week_start
    while current <= week_end:
        date_str = current.strftime("%Y-%m-%d")
        summary_file = vault / "Daily_Logs" / f"daily_summary_{date_str}.md"

        content = read_file_if_exists(summary_file)
        if content:
            summaries.append({
                'date': date_str,
                'day': current.strftime("%A"),
                'content': content
            })
        current += timedelta(days=1)

    return summaries


def get_session_logs(week_start: datetime, week_end: datetime) -> List[Dict]:
    """
    Get Claude session logs from this week.

    Returns:
        List of dicts with 'date' and 'content' keys
    """
    vault = get_vault_path()
    logs = []

    current = week_start
    while current <= week_end:
        date_str = current.strftime("%Y-%m-%d")
        log_file = vault.parent / "Work" / "Daily_Logs" / f"claude_sessions_{date_str}.md"
        # Also check alternate path
        if not log_file.exists():
            log_file = Path(__file__).parent.parent / "Work" / "Daily_Logs" / f"claude_sessions_{date_str}.md"

        content = read_file_if_exists(log_file)
        if content:
            logs.append({
                'date': date_str,
                'content': content
            })
        current += timedelta(days=1)

    return logs


def get_completed_tasks(prev_monday: datetime, prev_friday: datetime) -> List[Dict]:
    """
    Get tasks completed during the previous calendar week (Mon-Fri).

    Args:
        prev_monday: Previous week's Monday
        prev_friday: Previous week's Friday

    Returns:
        List of dicts with 'title', 'completed_date' keys
    """
    vault = get_vault_path()
    tasks_folder = vault / "Inbox" / "Tasks"
    completed = []

    if not tasks_folder.exists():
        return completed

    for task_file in tasks_folder.glob("task_*.md"):
        content = read_file_if_exists(task_file)
        if not content:
            continue

        # Check if completed
        if 'status: completed' not in content.lower():
            continue

        # Extract title from filename or content
        title = task_file.stem.replace('task_', '').replace('_', ' ')

        # Try to get completed date
        date_match = re.search(r'completed-date:\s*(\d{4}-\d{2}-\d{2})', content)
        if date_match:
            completed_date = datetime.strptime(date_match.group(1), '%Y-%m-%d')
            if prev_monday <= completed_date <= prev_friday:
                completed.append({
                    'title': title,
                    'completed_date': date_match.group(1)
                })

    return completed


def get_blocked_tasks() -> List[Dict]:
    """
    Get currently blocked or waiting tasks.

    Returns:
        List of dicts with 'title', 'status', 'note' keys
    """
    vault = get_vault_path()
    tasks_folder = vault / "Inbox" / "Tasks"
    blocked = []

    if not tasks_folder.exists():
        return blocked

    for task_file in tasks_folder.glob("task_*.md"):
        content = read_file_if_exists(task_file)
        if not content:
            continue

        # Check if blocked or waiting
        status_match = re.search(r'status:\s*(blocked|waiting)', content, re.IGNORECASE)
        if not status_match:
            continue

        title = task_file.stem.replace('task_', '').replace('_', ' ')
        status = status_match.group(1)

        # Try to get status note
        note_match = re.search(r'status-note:\s*(.+)', content)
        note = note_match.group(1).strip() if note_match else None

        blocked.append({
            'title': title,
            'status': status,
            'note': note
        })

    return blocked


def get_open_tasks() -> List[Dict]:
    """
    Get active/in-progress tasks.

    Returns:
        List of dicts with 'title', 'due_date' keys
    """
    vault = get_vault_path()
    tasks_folder = vault / "Inbox" / "Tasks"
    open_tasks = []

    if not tasks_folder.exists():
        return open_tasks

    for task_file in tasks_folder.glob("task_*.md"):
        content = read_file_if_exists(task_file)
        if not content:
            continue

        # Check if active or in-progress
        if not re.search(r'status:\s*(active|in-progress)', content, re.IGNORECASE):
            continue

        title = task_file.stem.replace('task_', '').replace('_', ' ')

        # Try to get due date
        due_match = re.search(r'due-date:\s*(\d{4}-\d{2}-\d{2})', content)
        due_date = due_match.group(1) if due_match else None

        open_tasks.append({
            'title': title,
            'due_date': due_date
        })

    return open_tasks


def get_meetings(week_start: datetime, week_end: datetime) -> List[Dict]:
    """
    Get meeting summaries from this week.

    Returns:
        List of dicts with 'title', 'date', 'content' keys
    """
    vault = get_vault_path()
    meetings_folder = vault / "Meetings"
    meetings = []

    if not meetings_folder.exists():
        return meetings

    for meeting_file in meetings_folder.glob("*.md"):
        if meeting_file.is_dir():
            continue

        # Try to extract date from filename (format: YYYY-MM-DD_Title.md)
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})_(.+)\.md', meeting_file.name)
        if not date_match:
            continue

        meeting_date = datetime.strptime(date_match.group(1), '%Y-%m-%d')
        if meeting_date < week_start or meeting_date > week_end:
            continue

        title = date_match.group(2).replace('_', ' ')
        content = read_file_if_exists(meeting_file)

        meetings.append({
            'title': title,
            'date': date_match.group(1),
            'content': content or ''
        })

    return meetings


def get_granola_query_info(prev_monday: datetime, prev_friday: datetime,
                           curr_monday: datetime, curr_friday: datetime) -> Dict:
    """
    Get info for Claude to query Granola for meetings.

    Uses last_week for Progress (previous Mon-Fri) and this_week for Plans context.

    Returns:
        Dict with query instructions for Claude
    """
    return {
        'progress_query': f"meetings from {prev_monday.strftime('%Y-%m-%d')} to {prev_friday.strftime('%Y-%m-%d')}",
        'progress_time_range': 'last_week',
        'plans_query': f"meetings from {curr_monday.strftime('%Y-%m-%d')} to {curr_friday.strftime('%Y-%m-%d')}",
        'plans_time_range': 'this_week',
        'instructions': f"""
**Granola Meeting Queries Required:**

For **Progress** (previous week: {prev_monday.strftime('%d %b')} - {prev_friday.strftime('%d %b')}):
Claude should call: mcp__granola__list_meetings(time_range="last_week")
Then for each relevant meeting, get details with: mcp__granola__get_meetings(meeting_ids=[...])

For **Plans** context (current week: {curr_monday.strftime('%d %b')} - {curr_friday.strftime('%d %b')}):
Claude should call: mcp__granola__list_meetings(time_range="this_week")

Key meetings to look for:
- 1:1s with direct reports
- Leadership/strategy meetings
- MFM (Monthly Focus Meetings)
- Planning/review sessions
"""
    }


def gather_context() -> Dict:
    """
    Gather all context needed for 4Ps generation.

    Returns:
        Dict with all context data
    """
    week_start, week_end, week_label = get_week_dates()
    prev_monday, prev_friday = get_previous_week_boundaries()
    curr_monday, curr_friday = get_current_week_boundaries()

    print("=" * 60)
    print("4Ps Generation - Julie")
    print("=" * 60)
    print(f"\n📅 {week_label}")
    print(f"  Progress period: {prev_monday.strftime('%d %b')} - {prev_friday.strftime('%d %b')}")
    print(f"  Plans period: {curr_monday.strftime('%d %b')} - {curr_friday.strftime('%d %b')}")
    print("\n🤖 Gathering context from all sources...\n")

    context = {
        'week_label': week_label,
        'week_start': week_start,
        'week_end': week_end,
        'prev_monday': prev_monday,
        'prev_friday': prev_friday,
        'curr_monday': curr_monday,
        'curr_friday': curr_friday
    }

    print("  ✓ Reading previous week's 4Ps...")
    context['previous_4ps'] = get_previous_4ps()

    print("  ✓ Gathering daily summaries (previous week)...")
    context['daily_summaries'] = get_daily_summaries(prev_monday, prev_friday)

    print("  ✓ Gathering session logs (previous week)...")
    context['session_logs'] = get_session_logs(prev_monday, prev_friday)

    print("  ✓ Finding completed tasks (previous week)...")
    context['completed_tasks'] = get_completed_tasks(prev_monday, prev_friday)

    print("  ✓ Finding blocked tasks...")
    context['blocked_tasks'] = get_blocked_tasks()

    print("  ✓ Finding open tasks...")
    context['open_tasks'] = get_open_tasks()

    print("  ✓ Gathering local meeting summaries (previous week)...")
    context['meetings'] = get_meetings(prev_monday, prev_friday)

    print("  ⏳ Granola meetings query ready (Claude will execute)...")
    context['granola_query'] = get_granola_query_info(prev_monday, prev_friday, curr_monday, curr_friday)

    return context


def generate_draft(context: Dict) -> str:
    """
    Generate 4Ps draft from gathered context.

    Args:
        context: Dict with all gathered context

    Returns:
        Formatted 4Ps draft string
    """
    lines = []
    lines.append(f"### {context['week_label']}")
    lines.append("")

    # PRIORITIES - Carry forward from last week
    lines.append("Priorities")
    if context['previous_4ps']['priorities']:
        for p in context['previous_4ps']['priorities']:
            lines.append(f"- {p}")
    else:
        lines.append("- [Carry forward from last week or update based on MFM/OKRs]")
    lines.append("")

    # PROGRESS - Based on previous week's plans + completed work (Mon-Fri)
    prev_mon = context['prev_monday'].strftime('%d %b')
    prev_fri = context['prev_friday'].strftime('%d %b')
    curr_mon = context['curr_monday'].strftime('%d %b')
    curr_fri = context['curr_friday'].strftime('%d %b')

    lines.append(f"Progress (week of {prev_mon} - {prev_fri})")

    # First, follow up on last week's plans
    if context['previous_4ps']['plans']:
        lines.append("<!-- Last week's plans to follow up on: -->")
        for plan in context['previous_4ps']['plans'][:5]:
            lines.append(f"- {plan} [UPDATE STATUS]")

    # Add completed tasks
    if context['completed_tasks']:
        lines.append("<!-- Completed tasks (previous week): -->")
        for task in context['completed_tasks'][:5]:
            lines.append(f"- {task['title']}")

    # Add meeting highlights
    if context['meetings']:
        lines.append("<!-- Meetings (previous week): -->")
        for meeting in context['meetings'][:3]:
            lines.append(f"- {meeting['title']} [ADD KEY OUTCOMES]")

    if not (context['previous_4ps']['plans'] or context['completed_tasks'] or context['meetings']):
        lines.append("- [Add progress items]")

    lines.append("")

    # PLANS - Based on open tasks and context (current week Mon-Fri)
    lines.append(f"Plans (week of {curr_mon} - {curr_fri})")
    if context['open_tasks']:
        for task in context['open_tasks'][:5]:
            due_str = f" (due: {task['due_date']})" if task['due_date'] else ""
            lines.append(f"- {task['title']}{due_str}")
    else:
        lines.append("- [Add plans for next week]")
    lines.append("")

    # PROBLEMS - Based on blocked tasks
    lines.append("Problems")
    if context['blocked_tasks']:
        for task in context['blocked_tasks']:
            note_str = f" - {task['note']}" if task['note'] else ""
            lines.append(f"- {task['title']} ({task['status']}){note_str}")
    else:
        lines.append("- NA")
    lines.append("")

    return '\n'.join(lines)


def generate_4ps() -> Dict:
    """
    Main function to generate 4Ps draft.

    Returns:
        Dict with 'draft', 'context', 'output_path' keys
    """
    context = gather_context()

    print("\n📝 Generating draft...\n")
    draft = generate_draft(context)

    # Determine output path
    vault = get_vault_path()
    output_path = vault / "4Ps" / "4Ps_2026.md"

    # Summary stats
    print("=" * 60)
    print("CONTEXT SUMMARY")
    print("=" * 60)
    print(f"  Previous 4Ps found: {'Yes' if context['previous_4ps']['found'] else 'No'}")
    print(f"  Daily summaries: {len(context['daily_summaries'])}")
    print(f"  Session logs: {len(context['session_logs'])}")
    print(f"  Completed tasks: {len(context['completed_tasks'])}")
    print(f"  Blocked tasks: {len(context['blocked_tasks'])}")
    print(f"  Open tasks: {len(context['open_tasks'])}")
    print(f"  Meetings: {len(context['meetings'])}")

    return {
        'draft': draft,
        'context': context,
        'output_path': str(output_path)
    }


def finalize_4ps(draft: str, user_edits: Optional[str] = None) -> Path:
    """
    Finalize and save the 4Ps entry.

    Args:
        draft: The draft 4Ps content
        user_edits: Optional user edits/replacements

    Returns:
        Path to the saved file
    """
    vault = get_vault_path()
    output_path = vault / "4Ps" / "4Ps_2026.md"

    # Use user edits if provided, otherwise use draft
    final_content = user_edits if user_edits else draft

    # Read existing content
    existing = read_file_if_exists(output_path) or ""

    # Find where to insert (after the Outline/Framework section)
    # Look for the first ### Week entry
    week_pattern = r'(###\s+Week\s+(?:beginning|ending))'
    match = re.search(week_pattern, existing)

    if match:
        # Insert before the first week entry
        insert_pos = match.start()
        new_content = existing[:insert_pos] + final_content + "\n\n" + existing[insert_pos:]
    else:
        # No existing weeks, append after content
        new_content = existing.rstrip() + "\n\n___\n" + final_content

    # Write the file
    output_path.write_text(new_content)

    return output_path


def format_4ps_response(result: Dict) -> str:
    """
    Format the 4Ps generation response for display.

    Args:
        result: Dict from generate_4ps()

    Returns:
        Formatted string for output
    """
    output = []

    # Granola query instructions first
    output.append("=" * 60)
    output.append("STEP 1: FETCH GRANOLA MEETINGS")
    output.append("=" * 60)
    output.append("")
    output.append("Claude should now query Granola for meetings:")
    output.append("")
    output.append("**For Progress (previous week):**")
    output.append("```")
    output.append("mcp__granola__list_meetings(time_range=\"last_week\")")
    output.append("```")
    output.append("")
    output.append("**For Plans context (current week):**")
    output.append("```")
    output.append("mcp__granola__list_meetings(time_range=\"this_week\")")
    output.append("```")
    output.append("")
    output.append("Then get details for key meetings (1:1s, leadership, MFMs):")
    output.append("")
    output.append("```")
    output.append("mcp__granola__get_meetings(meeting_ids=[\"id1\", \"id2\", ...])")
    output.append("```")
    output.append("")

    # Draft
    output.append("=" * 60)
    output.append("STEP 2: PRELIMINARY DRAFT (enhance with Granola data)")
    output.append("=" * 60)
    output.append("")
    output.append(result['draft'])
    output.append("")

    # Instructions
    output.append("=" * 60)
    output.append("STEP 3: WORKFLOW FOR CLAUDE")
    output.append("=" * 60)
    output.append("")
    output.append("1. **Read team context** from Work/LLM_Context/Squads/Squads_overview.md for audience awareness")
    output.append("2. **Fetch Granola meetings** using the MCP calls above")
    output.append("3. **Review leadership Slack** (#priv-forma-design-leadership-fy27) for key discussions to include")
    output.append("4. **Enhance the draft** following the 4Ps writing guidance in CLAUDE.md:")
    output.append("   - Priorities: 2-3 high-level themes, not a task category list")
    output.append("   - Progress: Group related work into narrative bullets (one per initiative, not per event)")
    output.append("   - Plans: Initiative-level, not task-level. Must make sense to a leadership audience")
    output.append("   - Problems: Frame as strategic questions or decisions needed")
    output.append("   - Exclude sensitive HR/performance/comp matters")
    output.append("   - Add a 'Leadership discussions' section from the leadership channel")
    output.append("5. **Present enhanced draft** to user for review")
    output.append("6. **Finalize** with: ./pos \"finalize 4ps: [final content]\"")
    output.append("")
    output.append(f"Output will be appended to: {result['output_path']}")

    return '\n'.join(output)


# Test
if __name__ == '__main__':
    result = generate_4ps()
    print("\n" + format_4ps_response(result))
