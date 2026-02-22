#!/usr/bin/env python3
"""
Sync Today's Granola Meetings to Obsidian

Syncs meeting summaries from Granola to Obsidian vault for daily summary integration.

## Workflow

1. Query Granola for today's meetings
2. For each meeting, get details
3. Create short Obsidian summary in Work/Meetings/
4. Daily summary can then include these meetings automatically

## Usage

    # Via ./pos command
    ./pos "sync meetings"

    # Direct Python execution
    python sync_meetings.py

## Integration

Called by:
- Reflection Agent during daily summary (optional)
- User via "sync meetings" command
- Scheduled automation (future)

Depends on:
- granola_helper.py for Granola queries
- Granola MCP tools called by Claude Code
"""

import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Import Granola helpers
try:
    from granola_helper import (
        list_todays_meetings,
        get_meeting_details,
        create_obsidian_meeting_summary,
        sanitize_filename
    )
except ImportError:
    # Fallback if running standalone
    print("Warning: Could not import granola_helper")
    def list_todays_meetings(): return []
    def get_meeting_details(id): return {}
    def create_obsidian_meeting_summary(data, path=None): return ""
    def sanitize_filename(title): return title.replace(' ', '_')


def get_vault_path() -> Path:
    """Get the Obsidian vault path."""
    return Path(__file__).parent.parent / "Work"


def sync_todays_meetings(meetings_data: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Sync today's meetings from Granola to Obsidian.

    This function can work in two modes:
    1. If meetings_data is provided: Use the provided meeting data
    2. If meetings_data is None: Call stub functions (Claude Code should provide data)

    Args:
        meetings_data: Optional list of meeting dicts from Granola MCP query.
            If not provided, will call list_todays_meetings() stub.

    Returns:
        Dict with sync results: {
            'synced': int,
            'files': list of paths,
            'errors': list of error messages
        }
    """
    print("\n" + "="*60)
    print("Syncing Today's Meetings from Granola")
    print("="*60 + "\n")

    today = datetime.now().strftime("%Y-%m-%d")
    vault = get_vault_path()
    meetings_dir = vault / "Meetings"

    # Ensure directory exists
    meetings_dir.mkdir(parents=True, exist_ok=True)

    # Get meetings (from provided data or stub)
    if meetings_data:
        meetings = meetings_data
        print(f"Using provided meeting data ({len(meetings)} meetings)")
    else:
        print("Querying Granola for today's meetings...")
        meetings = list_todays_meetings()

    if not meetings:
        print("No meetings found for today")
        return {
            'synced': 0,
            'files': [],
            'errors': []
        }

    print(f"Found {len(meetings)} meeting(s) for {today}\n")

    synced_files = []
    errors = []

    for meeting in meetings:
        meeting_id = meeting.get('id', 'unknown')
        meeting_title = meeting.get('title', 'Unknown Meeting')

        print(f"  Processing: {meeting_title}...")

        try:
            # Get full details if not already included
            if 'summary' not in meeting or not meeting.get('summary'):
                details = get_meeting_details(meeting_id)
                meeting.update(details)

            # Ensure date is set
            if 'date' not in meeting:
                meeting['date'] = today

            # Create Obsidian summary
            safe_title = sanitize_filename(meeting_title)
            output_path = meetings_dir / f"{today}_{safe_title}.md"

            result_path = create_obsidian_meeting_summary(meeting, str(output_path))

            synced_files.append(result_path)
            print(f"    Synced to {result_path}")

        except Exception as e:
            error_msg = f"Error syncing '{meeting_title}': {e}"
            errors.append(error_msg)
            print(f"    Error: {e}")

    # Summary
    print(f"\nSynced {len(synced_files)} meeting(s) to Obsidian")
    if errors:
        print(f"Encountered {len(errors)} error(s)")

    return {
        'synced': len(synced_files),
        'files': synced_files,
        'errors': errors
    }


def run_sync() -> str:
    """
    Main entry point for sync command.

    Returns:
        Status message string
    """
    result = sync_todays_meetings()

    if result['synced'] == 0:
        return "No meetings found for today"
    elif result['errors']:
        return f"Synced {result['synced']} meeting(s) with {len(result['errors'])} error(s)"
    else:
        return f"Successfully synced {result['synced']} meeting(s) to Obsidian"


# Test/standalone execution
if __name__ == '__main__':
    print("Testing sync_meetings...\n")

    # Test with mock meeting data
    test_meetings = [
        {
            'id': 'test-1',
            'title': 'Test Team Sync',
            'date': datetime.now().strftime("%Y-%m-%d"),
            'attendees': ['Alice', 'Bob', 'Charlie'],
            'summary': 'Discussed project progress. Decided to move deadline. Alice to send update.',
            'duration': 30,
            'link': 'granola://meeting/test-1'
        },
        {
            'id': 'test-2',
            'title': 'Test 1on1 with Manager',
            'date': datetime.now().strftime("%Y-%m-%d"),
            'attendees': ['You', 'Manager'],
            'summary': 'Career discussion. Feedback on Q4 performance. Goals for Q1.',
            'duration': 45,
            'link': 'granola://meeting/test-2'
        }
    ]

    print("Running sync with test data...\n")
    result = sync_todays_meetings(test_meetings)

    print("\n" + "="*50)
    print("SYNC RESULTS:")
    print("="*50)
    print(f"Synced: {result['synced']}")
    print(f"Files: {result['files']}")
    print(f"Errors: {result['errors']}")
