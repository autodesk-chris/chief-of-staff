#!/usr/bin/env python3
"""
Granola MCP Integration Helpers for Julie Agent System

Provides helper functions for working with Granola meeting integration.

## Architecture Note

Like the memory system, Granola integration relies on Claude Code calling MCP tools
directly. These Python helpers:
1. Format requests for Granola MCP calls
2. Process results from Granola queries
3. Create Obsidian summaries from Granola data

## MCP Tools (called by Claude Code)

- mcp__granola__query_granola_meetings - Search/query meetings
- (Additional Granola MCP tools as available)

## Current Status

This module contains STUB functions that will be enhanced when Granola MCP
integration is fully configured. The stubs demonstrate expected interfaces
and allow dependent code to work without Granola available.

## Usage

    from granola_helper import search_meetings, list_todays_meetings

    # Search for meetings (Claude Code will call actual MCP)
    meetings = search_meetings("Budget Review", time_range='last_30_days')

    # Create Obsidian summary from meeting data
    create_obsidian_meeting_summary(meeting_data, output_path)
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any


def get_vault_path() -> Path:
    """Get the Obsidian vault path."""
    return Path(__file__).parent.parent / "Work"


def search_meetings(query: str, time_range: str = 'last_30_days') -> List[Dict[str, Any]]:
    """
    Search for meetings in Granola.

    NOTE: This is a STUB. Claude Code will call mcp__granola__query_granola_meetings
    and pass results to dependent functions.

    Args:
        query: Search query (meeting title, keywords, attendees)
        time_range: Time range to search ('last_7_days', 'last_30_days', 'last_90_days')

    Returns:
        List of meeting objects with id, title, date, attendees, summary
    """
    print(f"[Granola STUB] Searching for: '{query}' in {time_range}")
    print("  Note: Claude Code should call mcp__granola__query_granola_meetings")
    return []


def get_meeting_details(meeting_id: str) -> Dict[str, Any]:
    """
    Get detailed meeting information from Granola.

    NOTE: This is a STUB.

    Args:
        meeting_id: Granola meeting UUID

    Returns:
        Dict with meeting details including title, date, attendees, summary, duration
    """
    print(f"[Granola STUB] Getting details for meeting: {meeting_id}")
    return {
        'id': meeting_id,
        'title': 'Unknown Meeting',
        'date': datetime.now().strftime("%Y-%m-%d"),
        'attendees': [],
        'summary': 'No summary available (Granola not connected)',
        'duration': 0,
        'link': ''
    }


def get_meeting_transcript(meeting_id: str) -> str:
    """
    Get full transcript for a meeting from Granola.

    NOTE: This is a STUB.

    Args:
        meeting_id: Granola meeting UUID

    Returns:
        Full meeting transcript text
    """
    print(f"[Granola STUB] Getting transcript for: {meeting_id}")
    return "Transcript not available (Granola not connected)"


def list_todays_meetings() -> List[Dict[str, Any]]:
    """
    List today's meetings from Granola.

    NOTE: This is a STUB.

    Returns:
        List of meeting objects from today
    """
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[Granola STUB] Listing meetings for: {today}")
    return []


def search_by_title(title: str, date_range_days: int = 7) -> Optional[Dict[str, Any]]:
    """
    Search for a specific meeting by title within a date range.

    NOTE: This is a STUB.

    Args:
        title: Meeting title to search for
        date_range_days: How many days back to search

    Returns:
        Meeting object or None if not found
    """
    print(f"[Granola STUB] Searching for meeting titled: '{title}' (last {date_range_days} days)")
    return None


def sanitize_filename(title: str) -> str:
    """
    Sanitize meeting title for use as filename.

    Args:
        title: Meeting title

    Returns:
        Safe filename string
    """
    # Remove special characters, keep alphanumeric, spaces, hyphens, underscores
    safe = "".join(c if c.isalnum() or c in [' ', '-', '_'] else '' for c in title)
    # Replace spaces with underscores
    safe = safe.replace(' ', '_')
    # Remove duplicate underscores
    while '__' in safe:
        safe = safe.replace('__', '_')
    return safe.strip('_')


def create_obsidian_meeting_summary(
    meeting_data: Dict[str, Any],
    output_path: Optional[str] = None
) -> str:
    """
    Create short Obsidian meeting summary from Granola data.

    Args:
        meeting_data: Meeting data from Granola with keys:
            - id: Meeting UUID
            - title: Meeting title
            - date: Meeting date (YYYY-MM-DD)
            - attendees: List of attendee names
            - summary: AI-generated summary
            - duration: Duration in minutes
            - link: Granola deep link (optional)

    Returns:
        Path to created summary file
    """
    vault = get_vault_path()

    title = meeting_data.get('title', 'Unknown Meeting')
    date = meeting_data.get('date', datetime.now().strftime("%Y-%m-%d"))
    attendees = meeting_data.get('attendees', [])
    duration = meeting_data.get('duration', 'N/A')
    summary = meeting_data.get('summary', 'No summary available')
    granola_link = meeting_data.get('link', '')

    # Generate output path if not provided
    if not output_path:
        safe_title = sanitize_filename(title)
        output_path = vault / "Meetings" / f"{date}_{safe_title}.md"
    else:
        output_path = Path(output_path)

    # Ensure directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Format attendees
    attendees_str = ', '.join(attendees) if attendees else 'Not recorded'

    # Build content
    content = f"""# {title} - {date}

**Attendees:** {attendees_str}
**Duration:** {duration} min

## Summary

{summary}

## Key decisions

- [To be extracted]

## Action items

- [ ] [To be extracted]

---
"""
    if granola_link:
        content += f"[View full transcript in Granola]({granola_link})\n"
    content += "Synced from Granola by Meetings Agent\n"

    # Write file
    output_path.write_text(content)

    print(f"[Granola] Created summary at {output_path}")
    return str(output_path)


def format_granola_query(title: str, date: Optional[str] = None) -> Dict[str, Any]:
    """
    Format a query for Granola MCP.

    Claude Code can use this to prepare mcp__granola__query_granola_meetings call.

    Args:
        title: Meeting title to search for
        date: Optional date filter (YYYY-MM-DD)

    Returns:
        Query parameters dict
    """
    query = {'title': title}
    if date:
        query['date'] = date
    return query


# Test function
if __name__ == '__main__':
    print("Testing Granola helpers...")
    print("Note: These are STUB functions. Actual Granola calls happen via MCP.\n")

    # Test 1: Search meetings
    print("1. Testing search_meetings()...")
    search_meetings("Budget Review")

    # Test 2: List today's meetings
    print("\n2. Testing list_todays_meetings()...")
    list_todays_meetings()

    # Test 3: Create Obsidian summary
    print("\n3. Testing create_obsidian_meeting_summary()...")
    test_meeting = {
        'id': 'test-123',
        'title': 'Test Meeting',
        'date': datetime.now().strftime("%Y-%m-%d"),
        'attendees': ['Alice', 'Bob'],
        'summary': 'This is a test meeting summary.',
        'duration': 30,
        'link': 'granola://meeting/test-123'
    }

    # Create in a test location
    vault = get_vault_path()
    test_path = vault / "Meetings" / "test_meeting_summary.md"
    result = create_obsidian_meeting_summary(test_meeting, str(test_path))
    print(f"  Created: {result}")

    # Show content preview
    if Path(result).exists():
        content = Path(result).read_text()
        print(f"\n  Content preview:\n{content[:300]}...")

    print("\n" + "="*50)
    print("Granola helpers test complete!")
    print("="*50)
