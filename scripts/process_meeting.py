#!/usr/bin/env python3
"""
Post-Meeting Processing Script for Julie Agent System

Processes completed meetings by querying Granola for meeting content,
extracting actions/decisions/takeaways, and creating structured outputs.

## Workflow

1. Search Granola for meeting by title/date
2. Extract key takeaways, actions, decisions
3. Create meeting summary with Slack-ready section
4. Create action items in Work/Inbox/Actions/
5. Create decision records in Work/Decisions/
6. Create observations in Work/People/Observations/ (if applicable)

## Usage

    # Via ./pos command
    ./pos "post meeting: Budget Review"
    ./pos "process meeting: Team Sync"

    # Direct Python execution
    python process_meeting.py "Budget Review"

## Integration

Called by:
- parse_command.py for "post meeting:" and "process meeting:" commands
- User directly via command line

Depends on:
- granola_helper.py for Granola queries
- create_item.py for action/decision creation
- Obsidian vault for file storage
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from granola_helper import (
    search_meetings,
    get_meeting_details,
    sanitize_filename
)


def get_vault_path() -> Path:
    """Get the Obsidian vault path."""
    return Path(__file__).parent.parent / "Work"


def extract_key_takeaways(summary: str, transcript: Optional[str] = None) -> List[str]:
    """
    Extract key takeaways from meeting summary.

    NOTE: This is a simplified implementation. Claude Code will enhance
    this with LLM-based extraction from Granola content.

    Args:
        summary: Meeting summary text
        transcript: Optional full transcript

    Returns:
        List of key takeaway strings (3-5 items)
    """
    # Simple extraction: split by sentences and take first few
    # Claude Code will typically provide extracted takeaways directly
    if not summary:
        return ["No summary available"]

    # Split into sentences
    sentences = summary.replace('!', '.').replace('?', '.').split('.')
    sentences = [s.strip() for s in sentences if s.strip()]

    # Take first 3-5 meaningful sentences as takeaways
    takeaways = []
    for sentence in sentences[:5]:
        if len(sentence) > 20:  # Skip very short sentences
            takeaways.append(sentence)

    return takeaways if takeaways else ["Meeting occurred - review Granola for details"]


def extract_actions(transcript: str) -> List[Dict[str, Any]]:
    """
    Extract action items from meeting transcript.

    NOTE: This is a STUB. Claude Code should call this with already-extracted
    actions from Granola, or implement LLM-based extraction.

    Args:
        transcript: Meeting transcript text

    Returns:
        List of action dicts with keys: person, task, due
    """
    # Stub implementation - returns empty
    # Claude Code will provide extracted actions from Granola analysis
    print("[Process Meeting] Action extraction from transcript - stub")
    return []


def extract_decisions(transcript: str) -> List[Dict[str, Any]]:
    """
    Extract decisions from meeting transcript.

    NOTE: This is a STUB. Claude Code should provide extracted decisions.

    Args:
        transcript: Meeting transcript text

    Returns:
        List of decision dicts with keys: decision, rationale, participants
    """
    # Stub implementation
    print("[Process Meeting] Decision extraction from transcript - stub")
    return []


def extract_observations(transcript: str) -> List[Dict[str, Any]]:
    """
    Extract team feedback/observations from meeting.

    NOTE: This is a STUB. Claude Code should identify feedback about team members.

    Args:
        transcript: Meeting transcript text

    Returns:
        List of observation dicts with keys: person, feedback, context
    """
    # Stub implementation
    print("[Process Meeting] Observation extraction from transcript - stub")
    return []


def create_slack_ready_summary(
    title: str,
    takeaways: List[str],
    actions: List[Dict[str, Any]]
) -> str:
    """
    Format a Slack-ready summary for easy copy-paste.

    Args:
        title: Meeting title
        takeaways: List of key takeaway strings
        actions: List of action dicts

    Returns:
        Formatted Slack-ready text
    """
    # Build Slack format
    lines = [f"Quick recap from {title}:"]

    # Add takeaways with Slack bullets
    for takeaway in takeaways[:3]:
        lines.append(f"* {takeaway}")

    # Add actions if present
    if actions:
        lines.append("")
        lines.append("Actions:")
        for action in actions:
            person = action.get('person', 'TBD')
            task = action.get('task', 'No task specified')
            due = action.get('due', 'TBD')
            lines.append(f"* {person} - {task} ({due})")

    return '\n'.join(lines)


def create_meeting_summary(
    title: str,
    meeting_data: Dict[str, Any],
    takeaways: List[str],
    actions: List[Dict[str, Any]],
    decisions: List[Dict[str, Any]],
    slack_summary: str
) -> str:
    """
    Create full meeting summary document.

    Args:
        title: Meeting title
        meeting_data: Meeting data from Granola
        takeaways: Extracted takeaways
        actions: Extracted actions
        decisions: Extracted decisions
        slack_summary: Pre-formatted Slack summary

    Returns:
        Full markdown document content
    """
    date = meeting_data.get('date', datetime.now().strftime("%Y-%m-%d"))
    attendees = meeting_data.get('attendees', [])
    duration = meeting_data.get('duration', 'N/A')
    granola_link = meeting_data.get('link', '')

    attendees_str = ', '.join(attendees) if attendees else 'Not recorded'

    # Build document
    content = f"""# {title} - {date}

**Attendees:** {attendees_str}
**Duration:** {duration} min

## Key takeaways

"""

    for takeaway in takeaways:
        content += f"- {takeaway}\n"

    content += "\n## Actions\n\n"
    if actions:
        for action in actions:
            person = action.get('person', 'TBD')
            task = action.get('task', '')
            due = action.get('due', '')
            content += f"- {person} to {task}"
            if due:
                content += f" by {due}"
            content += "\n"
    else:
        content += "- No actions recorded\n"

    content += "\n## Decisions\n\n"
    if decisions:
        for decision in decisions:
            content += f"- {decision.get('decision', 'No decision specified')}\n"
    else:
        content += "- No decisions recorded\n"

    content += f"""
---

**Slack-ready summary:**

{slack_summary}

---
"""

    if granola_link:
        content += f"[View full transcript in Granola]({granola_link})\n"

    content += "Processed by Meetings Agent\n"

    return content


def create_action_items(actions: List[Dict[str, Any]], meeting_title: str) -> List[str]:
    """
    Create action item files in Work/Inbox/Actions/.

    Args:
        actions: List of action dicts
        meeting_title: Source meeting title (for reference)

    Returns:
        List of created file paths
    """
    if not actions:
        return []

    vault = get_vault_path()
    actions_dir = vault / "Inbox" / "Actions"
    actions_dir.mkdir(parents=True, exist_ok=True)

    created_files = []
    today = datetime.now().strftime("%Y-%m-%d")

    for action in actions:
        person = action.get('person', 'Unknown')
        task = action.get('task', 'No task specified')
        due = action.get('due', '')

        # Create action file
        safe_task = sanitize_filename(task[:50])  # Limit filename length
        filename = f"action_{safe_task}.md"
        filepath = actions_dir / filename

        content = f"""---
type: action
assignee: {person}
created: {today}
due: {due if due else 'TBD'}
status: active
source: {meeting_title}
tags: []
---

# {task}

**Assignee:** {person}
**Due:** {due if due else 'TBD'}
**Source:** {meeting_title}

## Details

[Add details]

## Notes

[Add notes]
"""

        filepath.write_text(content)
        created_files.append(str(filepath))
        print(f"  Created action: {filepath}")

    return created_files


def create_decision_items(decisions: List[Dict[str, Any]], meeting_title: str) -> List[str]:
    """
    Create decision record files in Work/Decisions/.

    Args:
        decisions: List of decision dicts
        meeting_title: Source meeting title

    Returns:
        List of created file paths
    """
    if not decisions:
        return []

    vault = get_vault_path()
    decisions_dir = vault / "Decisions"
    decisions_dir.mkdir(parents=True, exist_ok=True)

    created_files = []
    today = datetime.now().strftime("%Y-%m-%d")

    for decision in decisions:
        text = decision.get('decision', 'Decision not specified')
        rationale = decision.get('rationale', '')
        participants = decision.get('participants', [])

        # Create decision file
        safe_text = sanitize_filename(text[:50])
        filename = f"decision_{today}_{safe_text}.md"
        filepath = decisions_dir / filename

        participants_str = ', '.join(participants) if participants else 'Not recorded'

        content = f"""---
type: decision
date: {today}
source: {meeting_title}
participants: {participants_str}
status: active
tags: []
---

# {text}

**Date:** {today}
**Source:** {meeting_title}
**Participants:** {participants_str}

## Decision

{text}

## Rationale

{rationale if rationale else '[Add rationale]'}

## Implications

[Add implications]

## Related decisions

[Add related decisions]
"""

        filepath.write_text(content)
        created_files.append(str(filepath))
        print(f"  Created decision: {filepath}")

    return created_files


def create_observation_items(observations: List[Dict[str, Any]], meeting_title: str) -> List[str]:
    """
    Create observation files in Work/People/Observations/.

    Args:
        observations: List of observation dicts
        meeting_title: Source meeting title

    Returns:
        List of created file paths
    """
    if not observations:
        return []

    vault = get_vault_path()
    obs_dir = vault / "People" / "Observations"
    obs_dir.mkdir(parents=True, exist_ok=True)

    created_files = []
    today = datetime.now().strftime("%Y-%m-%d")

    for obs in observations:
        person = obs.get('person', 'Unknown')
        feedback = obs.get('feedback', '')
        context = obs.get('context', '')

        # Create observation file
        safe_person = sanitize_filename(person)
        filename = f"observation_{safe_person}_{today}.md"
        filepath = obs_dir / filename

        content = f"""---
type: observation
person: {person}
date: {today}
source: {meeting_title}
tags: []
---

# Observation - {person}

**Date:** {today}
**Source:** {meeting_title}

## Observation

{feedback}

## Context

{context if context else f'Observed during {meeting_title}'}
"""

        filepath.write_text(content)
        created_files.append(str(filepath))
        print(f"  Created observation: {filepath}")

    return created_files


def process_meeting(
    title: str,
    meeting_data: Optional[Dict[str, Any]] = None,
    takeaways: Optional[List[str]] = None,
    actions: Optional[List[Dict[str, Any]]] = None,
    decisions: Optional[List[Dict[str, Any]]] = None,
    observations: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Main entry point for post-meeting processing.

    This function can work in two modes:
    1. If data is provided: Use the provided meeting data directly
    2. If data is None: Query Granola (stub - Claude Code should provide data)

    Args:
        title: Meeting title to search for
        meeting_data: Optional pre-populated meeting data from Granola
        takeaways: Optional pre-extracted takeaways
        actions: Optional pre-extracted actions
        decisions: Optional pre-extracted decisions
        observations: Optional pre-extracted observations

    Returns:
        Dict with processing results
    """
    print(f"\n{'='*60}")
    print(f"Processing Meeting: {title}")
    print(f"{'='*60}\n")

    results = {
        'summary_file': None,
        'action_files': [],
        'decision_files': [],
        'observation_files': [],
        'errors': []
    }

    # Step 1: Get meeting data
    if not meeting_data:
        print("Searching Granola for meeting...")
        granola_results = search_meetings(title, time_range='last_7_days')

        if not granola_results:
            print(f"No meeting found in Granola matching: {title}")
            print("Proceeding with minimal data...")
            meeting_data = {
                'id': 'manual',
                'title': title,
                'date': datetime.now().strftime("%Y-%m-%d"),
                'attendees': [],
                'summary': 'Meeting data not available from Granola',
                'duration': 0,
                'link': ''
            }
        else:
            # Use first result
            meeting_data = granola_results[0]
            print(f"Found meeting: {meeting_data.get('title')}")

            # Get full details
            meeting_id = meeting_data.get('id')
            if meeting_id:
                details = get_meeting_details(meeting_id)
                meeting_data.update(details)

    # Step 2: Extract information (use provided or extract)
    if takeaways is None:
        summary = meeting_data.get('summary', '')
        takeaways = extract_key_takeaways(summary)
        print(f"Extracted {len(takeaways)} takeaways")

    if actions is None:
        actions = extract_actions(meeting_data.get('transcript', ''))
        print(f"Extracted {len(actions)} actions")

    if decisions is None:
        decisions = extract_decisions(meeting_data.get('transcript', ''))
        print(f"Extracted {len(decisions)} decisions")

    if observations is None:
        observations = extract_observations(meeting_data.get('transcript', ''))
        print(f"Extracted {len(observations)} observations")

    # Step 3: Create Slack-ready summary
    slack_summary = create_slack_ready_summary(title, takeaways, actions)

    # Step 4: Create meeting summary document
    summary_content = create_meeting_summary(
        title, meeting_data, takeaways, actions, decisions, slack_summary
    )

    vault = get_vault_path()
    meetings_dir = vault / "Meetings"
    meetings_dir.mkdir(parents=True, exist_ok=True)

    date = meeting_data.get('date', datetime.now().strftime("%Y-%m-%d"))
    safe_title = sanitize_filename(title)
    summary_path = meetings_dir / f"{date}_{safe_title}.md"

    summary_path.write_text(summary_content)
    results['summary_file'] = str(summary_path)
    print(f"\nCreated summary: {summary_path}")

    # Step 5: Create action items
    if actions:
        results['action_files'] = create_action_items(actions, title)

    # Step 6: Create decision records
    if decisions:
        results['decision_files'] = create_decision_items(decisions, title)

    # Step 7: Create observations
    if observations:
        results['observation_files'] = create_observation_items(observations, title)

    # Summary
    print(f"\n{'='*60}")
    print("PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"Summary: {results['summary_file']}")
    print(f"Actions created: {len(results['action_files'])}")
    print(f"Decisions created: {len(results['decision_files'])}")
    print(f"Observations created: {len(results['observation_files'])}")

    return results


def run_process() -> str:
    """
    Entry point for command-line usage.

    Returns:
        Status message
    """
    if len(sys.argv) < 2:
        return "Usage: python process_meeting.py 'Meeting Title'"

    title = sys.argv[1]
    results = process_meeting(title)

    if results['summary_file']:
        return f"Processed meeting: {results['summary_file']}"
    else:
        return "Failed to process meeting"


# Test/standalone execution
if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(run_process())
    else:
        # Run test with mock data
        print("Testing process_meeting...\n")

        test_meeting_data = {
            'id': 'test-123',
            'title': 'Test Budget Review',
            'date': datetime.now().strftime("%Y-%m-%d"),
            'attendees': ['Alice', 'Bob', 'Charlie'],
            'summary': 'Reviewed Q1 budget allocations. Decided to increase marketing spend by 15%. Need to finalize vendor contracts by Friday.',
            'duration': 45,
            'link': 'granola://meeting/test-123'
        }

        test_actions = [
            {'person': 'Alice', 'task': 'finalize vendor contracts', 'due': 'Friday'},
            {'person': 'Bob', 'task': 'update budget spreadsheet', 'due': 'this week'}
        ]

        test_decisions = [
            {'decision': 'Increase marketing spend by 15%', 'rationale': 'Q4 campaign success', 'participants': ['Alice', 'Charlie']}
        ]

        results = process_meeting(
            "Test Budget Review",
            meeting_data=test_meeting_data,
            actions=test_actions,
            decisions=test_decisions
        )

        print("\nTest complete!")
