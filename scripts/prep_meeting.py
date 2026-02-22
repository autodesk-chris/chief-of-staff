#!/usr/bin/env python3
"""
Meeting Preparation Script for Julie Agent System

Generates pre-meeting context documents by synthesizing relevant information
from memory, observations, past meetings, and Granola.

## Workflow

1. Detect meeting type (121, strategy, budget, team, general)
2. Gather type-specific context from relevant sources
3. Generate structured prep document
4. Save to Work/Meetings/Prep/

## Usage

    # Via ./pos command
    ./pos "prep meeting: Budget Review"
    ./pos "121: Sarah Johnson"

    # Direct Python execution
    python prep_meeting.py "Budget Review" "Alice, Bob"

## Integration

Called by:
- parse_command.py for "prep meeting:" and "121:" commands
- User directly via command line

Depends on:
- memory.py for memory queries
- granola_helper.py for Granola queries
- Obsidian vault for observations and past meetings
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from granola_helper import search_meetings, sanitize_filename


def get_vault_path() -> Path:
    """Get the Obsidian vault path."""
    return Path(__file__).parent.parent / "Work"


def detect_meeting_type(title: str, attendees: Optional[List[str]] = None) -> str:
    """
    Detect meeting type from title and attendees.

    Args:
        title: Meeting title
        attendees: Optional list of attendee names

    Returns:
        Meeting type: '121', 'strategy', 'budget', 'team', or 'general'
    """
    title_lower = title.lower()

    # Check for 1-on-1 indicators
    one_on_one_keywords = ['1:1', '1-1', 'one on one', '1on1', 'check-in', 'checkin']
    if any(kw in title_lower for kw in one_on_one_keywords):
        return '121'

    # Single attendee often means 1-on-1
    if attendees and len(attendees) == 1:
        return '121'

    # Check for strategy indicators
    strategy_keywords = ['strategy', 'strategic', 'roadmap', 'planning', 'okr', 'quarterly']
    if any(kw in title_lower for kw in strategy_keywords):
        return 'strategy'

    # Check for budget/finance indicators
    budget_keywords = ['budget', 'finance', 'financial', 'spend', 'cost', 'investment']
    if any(kw in title_lower for kw in budget_keywords):
        return 'budget'

    # Check for team meeting indicators
    team_keywords = ['team', 'all-hands', 'retro', 'retrospective', 'standup', 'sync']
    if any(kw in title_lower for kw in team_keywords):
        return 'team'

    return 'general'


def gather_observations(person_name: str, days: int = 30) -> List[Dict[str, Any]]:
    """
    Gather recent observations about a person.

    Args:
        person_name: Name of the person
        days: How many days back to search

    Returns:
        List of observation dicts with date, content, tags
    """
    vault = get_vault_path()
    observations_dir = vault / "People" / "Observations"

    if not observations_dir.exists():
        return []

    observations = []
    cutoff_date = datetime.now() - timedelta(days=days)

    # Search for observations about this person
    for obs_file in observations_dir.glob("observation_*.md"):
        try:
            content = obs_file.read_text()

            # Check if this observation is about the person
            name_lower = person_name.lower()
            filename_lower = obs_file.name.lower()

            # Check filename or content for person's name
            if name_lower.replace(' ', '_') in filename_lower or name_lower in content.lower():
                # Extract date from filename (observation_Name_YYYY-MM-DD.md)
                parts = obs_file.stem.split('_')
                if len(parts) >= 3:
                    try:
                        date_str = parts[-1]
                        obs_date = datetime.strptime(date_str, "%Y-%m-%d")

                        if obs_date >= cutoff_date:
                            observations.append({
                                'date': date_str,
                                'file': str(obs_file),
                                'content': content[:500]  # First 500 chars
                            })
                    except ValueError:
                        pass  # Skip files with invalid date format

        except Exception as e:
            print(f"Warning: Could not read {obs_file}: {e}")

    # Sort by date descending
    observations.sort(key=lambda x: x['date'], reverse=True)
    return observations[:5]  # Return latest 5


def gather_past_meetings(title: str, attendees: Optional[List[str]] = None, days: int = 90) -> List[Dict[str, Any]]:
    """
    Gather past meetings with similar title or attendees.

    Args:
        title: Meeting title to search for
        attendees: Optional attendee names to search for
        days: How many days back to search

    Returns:
        List of meeting dicts with date, title, summary
    """
    vault = get_vault_path()
    meetings_dir = vault / "Meetings"

    if not meetings_dir.exists():
        return []

    past_meetings = []
    cutoff_date = datetime.now() - timedelta(days=days)
    title_lower = title.lower()

    # Search meeting files
    for meeting_file in meetings_dir.glob("*.md"):
        # Skip prep files
        if '_prep.md' in meeting_file.name:
            continue

        try:
            # Check if title matches
            filename_lower = meeting_file.name.lower()
            title_words = title_lower.split()

            # Check if any significant word from title is in filename
            matches_title = any(len(word) > 3 and word in filename_lower for word in title_words)

            if matches_title:
                content = meeting_file.read_text()

                # Extract date from filename (YYYY-MM-DD_Title.md)
                date_str = meeting_file.name[:10]
                try:
                    meeting_date = datetime.strptime(date_str, "%Y-%m-%d")

                    if meeting_date >= cutoff_date:
                        past_meetings.append({
                            'date': date_str,
                            'title': meeting_file.stem[11:].replace('_', ' '),  # Remove date prefix
                            'file': str(meeting_file),
                            'summary': content[:300]  # First 300 chars as summary
                        })
                except ValueError:
                    pass

        except Exception as e:
            print(f"Warning: Could not read {meeting_file}: {e}")

    # Sort by date descending
    past_meetings.sort(key=lambda x: x['date'], reverse=True)
    return past_meetings[:3]  # Return latest 3


def gather_open_actions(person_name: Optional[str] = None, topic: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Gather open action items related to person or topic.

    Args:
        person_name: Optional person to filter actions for
        topic: Optional topic to filter actions for

    Returns:
        List of action dicts with title, assignee, due_date
    """
    vault = get_vault_path()
    actions_dir = vault / "Inbox" / "Actions"

    if not actions_dir.exists():
        return []

    open_actions = []

    for action_file in actions_dir.glob("action_*.md"):
        try:
            content = action_file.read_text()

            # Skip completed actions
            if 'status: completed' in content.lower() or 'status: archived' in content.lower():
                continue

            # Filter by person if specified
            if person_name:
                name_lower = person_name.lower()
                if name_lower not in content.lower():
                    continue

            # Filter by topic if specified
            if topic:
                topic_lower = topic.lower()
                if topic_lower not in content.lower():
                    continue

            # Extract title from filename
            title = action_file.stem.replace('action_', '').replace('_', ' ')

            open_actions.append({
                'title': title,
                'file': str(action_file),
                'preview': content[:200]
            })

        except Exception as e:
            print(f"Warning: Could not read {action_file}: {e}")

    return open_actions[:5]  # Return top 5


def gather_context_for_type(
    meeting_type: str,
    title: str,
    attendees: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Gather context based on meeting type.

    Args:
        meeting_type: Type of meeting (121, strategy, budget, team, general)
        title: Meeting title
        attendees: Optional list of attendees

    Returns:
        Dict with context sections
    """
    context = {
        'meeting_type': meeting_type,
        'past_meetings': [],
        'observations': [],
        'open_actions': [],
        'memory_context': [],
        'granola_context': []
    }

    # Get past meetings with similar title
    context['past_meetings'] = gather_past_meetings(title, attendees)

    # Get open actions related to meeting topic
    context['open_actions'] = gather_open_actions(topic=title)

    # Type-specific context
    if meeting_type == '121':
        # For 1-on-1s, get observations about the person
        if attendees and len(attendees) > 0:
            person = attendees[0]
            context['observations'] = gather_observations(person)
            context['open_actions'] = gather_open_actions(person_name=person)

    elif meeting_type == 'strategy':
        # For strategy meetings, we'd query strategy memory
        # This is a stub - Claude Code will call MCP directly
        context['memory_context'] = [
            {'note': 'Query claude-mem for strategy-related context'}
        ]

    elif meeting_type == 'budget':
        # For budget meetings, gather financial context
        context['memory_context'] = [
            {'note': 'Query claude-mem for budget/financial context'}
        ]

    # Query Granola for previous meetings (stub)
    context['granola_context'] = search_meetings(title, time_range='last_30_days')

    return context


def create_prep_document(
    title: str,
    meeting_type: str,
    context: Dict[str, Any],
    attendees: Optional[List[str]] = None,
    meeting_date: Optional[str] = None
) -> str:
    """
    Generate meeting prep document content.

    Args:
        title: Meeting title
        meeting_type: Detected meeting type
        context: Gathered context dict
        attendees: Optional list of attendees
        meeting_date: Optional meeting date (defaults to today)

    Returns:
        Markdown content for prep document
    """
    if not meeting_date:
        meeting_date = datetime.now().strftime("%Y-%m-%d")

    attendees_str = ', '.join(attendees) if attendees else 'TBD'

    # Build document
    content = f"""# Meeting Prep: {title}

**Date:** {meeting_date}
**Attendees:** {attendees_str}
**Type:** {meeting_type.upper()}

---

## Context

"""

    # Add past meetings context
    if context.get('past_meetings'):
        content += "### Previous meetings\n\n"
        for meeting in context['past_meetings']:
            content += f"- **{meeting['date']}**: {meeting['title']}\n"
        content += "\n"

    # Add observations (for 121s)
    if context.get('observations'):
        content += "### Recent observations\n\n"
        for obs in context['observations']:
            content += f"- **{obs['date']}**: {obs['content'][:100]}...\n"
        content += "\n"

    # Add open actions
    if context.get('open_actions'):
        content += "### Open actions to follow up\n\n"
        for action in context['open_actions']:
            content += f"- [ ] {action['title']}\n"
        content += "\n"

    # Add memory context notes
    if context.get('memory_context'):
        content += "### Memory context\n\n"
        for mem in context['memory_context']:
            content += f"- {mem.get('note', 'No context')}\n"
        content += "\n"

    # Key topics section (user fills in)
    content += """## Key topics to cover

- [ ] [Add topics]

## Notes

[Space for meeting notes]

---
Generated by Meetings Agent
"""

    return content


def prep_meeting(title: str, attendees: Optional[List[str]] = None) -> str:
    """
    Main entry point for meeting preparation.

    Args:
        title: Meeting title
        attendees: Optional list of attendee names

    Returns:
        Path to created prep document
    """
    print(f"\n{'='*60}")
    print(f"Preparing for Meeting: {title}")
    print(f"{'='*60}\n")

    # Step 1: Detect meeting type
    meeting_type = detect_meeting_type(title, attendees)
    print(f"Detected meeting type: {meeting_type}")

    # Step 2: Gather context
    print("Gathering context...")
    context = gather_context_for_type(meeting_type, title, attendees)

    # Show what was found
    print(f"  - Past meetings: {len(context.get('past_meetings', []))}")
    print(f"  - Observations: {len(context.get('observations', []))}")
    print(f"  - Open actions: {len(context.get('open_actions', []))}")

    # Step 3: Create prep document
    prep_content = create_prep_document(title, meeting_type, context, attendees)

    # Step 4: Save document
    vault = get_vault_path()
    prep_dir = vault / "Meetings" / "Prep"
    prep_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    safe_title = sanitize_filename(title)
    output_path = prep_dir / f"{today}_{safe_title}_prep.md"

    output_path.write_text(prep_content)

    print(f"\nCreated prep document: {output_path}")
    return str(output_path)


def run_prep() -> str:
    """
    Entry point for command-line usage.

    Returns:
        Status message
    """
    if len(sys.argv) < 2:
        return "Usage: python prep_meeting.py 'Meeting Title' ['Attendee1, Attendee2']"

    title = sys.argv[1]
    attendees = None

    if len(sys.argv) > 2:
        attendees = [a.strip() for a in sys.argv[2].split(',')]

    filepath = prep_meeting(title, attendees)
    return f"Created prep document: {filepath}"


# Test/standalone execution
if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(run_prep())
    else:
        # Run test
        print("Testing prep_meeting...\n")

        # Test 1: 1-on-1 meeting
        print("Test 1: 1-on-1 meeting")
        prep_meeting("Sarah Johnson", attendees=["Sarah Johnson"])

        # Test 2: Strategy meeting
        print("\nTest 2: Strategy meeting")
        prep_meeting("Q2 Strategy Planning", attendees=["Alice", "Bob", "Charlie"])

        # Test 3: Budget meeting
        print("\nTest 3: Budget meeting")
        prep_meeting("Budget Review", attendees=["Finance Team"])

        print("\nTests complete!")
