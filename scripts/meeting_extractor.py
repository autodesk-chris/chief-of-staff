#!/usr/bin/env python3
"""
Meeting Transcript Extractor for Julie Agent System

Provides extraction workflow for automatically identifying tasks, actions,
decisions, and observations from meeting transcripts via Granola MCP.

## Workflow

1. User runs: ./pos "post meeting: [title]"
2. Script returns instructions for Claude to:
   - Query Granola for the meeting
   - Get the full transcript
   - Extract items using LLM analysis
   - Create items using existing commands
3. Claude executes the workflow and creates all items

## Integration

Called by parse_command.py for "post meeting:" commands.
Uses Granola MCP tools called by Claude Code.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


def get_extraction_prompt() -> str:
    """
    Get the prompt template for extracting items from a transcript.

    This prompt guides Claude on how to identify and categorize items.
    """
    return '''
Analyze this meeting transcript and extract the following:

## 1. ACTIONS (tasks assigned to specific people)

Look for phrases like:
- "[Person] will...", "[Person] to...", "[Person] should..."
- "Can you...", "Could you...", "Would you..."
- "Action item:", "TODO:", "Follow up:"
- "[Person] agreed to...", "[Person] committed to..."
- "By [date]", "due [date]", "before [date]"

For each action, extract:
- **assignee**: Person responsible (use first name)
- **task**: What they need to do (clear, actionable description)
- **due**: When it's due (convert to YYYY-MM-DD if possible, or use "this week", "next Friday", etc.)

## 2. DECISIONS (choices made during the meeting)

Look for phrases like:
- "We decided...", "Decision:", "Agreed that..."
- "Going forward, we will...", "The plan is to..."
- "Let's go with...", "We're going to..."
- Final statements after discussion/debate

For each decision, extract:
- **decision**: What was decided (clear statement)
- **rationale**: Why (if mentioned)
- **participants**: Who was involved in the decision

## 3. TASKS FOR ME (things I need to do)

Look for:
- Things "I" or "Chris" committed to doing
- Self-assigned follow-ups
- Notes to self about next steps

For each task, extract:
- **title**: Clear task description
- **due**: When it's due
- **details**: Additional context

## 4. OBSERVATIONS (feedback about team members)

Look for:
- Positive comments about someone's work
- Recognition of contributions
- Areas for development mentioned
- Notable behaviors or skills demonstrated

For each observation, extract:
- **person**: Who the feedback is about
- **feedback**: The observation (specific and behavioral)
- **context**: Meeting context

## Output Format

Return your findings in this exact format:

### ACTIONS
1. assignee: [Name] | task: [description] | due: [date]
2. assignee: [Name] | task: [description] | due: [date]

### DECISIONS
1. decision: [description] | rationale: [why] | participants: [names]
2. decision: [description] | rationale: [why] | participants: [names]

### TASKS FOR ME
1. title: [description] | due: [date] | details: [context]

### OBSERVATIONS
1. person: [Name] | feedback: [observation] | context: [meeting context]

If a category has no items, write "None identified."
'''


def format_post_meeting_instructions(title: str) -> str:
    """
    Format the complete post-meeting processing instructions for Claude.

    Args:
        title: Meeting title to search for

    Returns:
        Formatted instructions string
    """
    today = datetime.now().strftime("%Y-%m-%d")
    extraction_prompt = get_extraction_prompt()

    instructions = f'''
{'='*70}
POST-MEETING PROCESSING: {title}
{'='*70}

**Step 1: Find the meeting in Granola**

Call: mcp__granola__query_granola_meetings
Query: "{title}"

Or list recent meetings:
Call: mcp__granola__list_meetings(time_range="this_week")

**Step 2: Get the full transcript**

Once you have the meeting ID, call:
mcp__granola__get_meeting_transcript(meeting_id="[UUID]")

Also get meeting details:
mcp__granola__get_meetings(meeting_ids=["[UUID]"])

**Step 3: Extract items from the transcript**

{extraction_prompt}

**Step 4: Create items using Julie commands**

For each ACTION extracted, run:
./pos "new action: [Assignee] to [task] due: [YYYY-MM-DD]"

For each DECISION extracted, run:
./pos "new decision: [decision] participants: [names] rationale: [why]"

For each TASK FOR ME extracted, run:
./pos "new task: [title] due: [YYYY-MM-DD] details: [context]"

For each OBSERVATION extracted, run:
./pos "observation: [Person] - [feedback] details: [context]"

**Step 5: Create meeting summary**

After creating all items, run:
./pos "finalize meeting: {title}"

This will create the meeting summary document in Work/Meetings/

{'='*70}
BEGIN PROCESSING
{'='*70}

Please proceed with Step 1: Query Granola for "{title}"
'''

    return instructions


def format_finalize_meeting_instructions(
    title: str,
    meeting_data: Dict[str, Any],
    items_created: Dict[str, int]
) -> str:
    """
    Format instructions for finalizing meeting processing.

    Args:
        title: Meeting title
        meeting_data: Meeting metadata from Granola
        items_created: Count of items created by type

    Returns:
        Summary of processing
    """
    date = meeting_data.get('date', datetime.now().strftime("%Y-%m-%d"))
    attendees = meeting_data.get('attendees', [])
    duration = meeting_data.get('duration', 'N/A')

    summary = f'''
{'='*70}
MEETING PROCESSING COMPLETE: {title}
{'='*70}

**Meeting Details:**
- Date: {date}
- Attendees: {', '.join(attendees) if attendees else 'Not recorded'}
- Duration: {duration} min

**Items Created:**
- Actions: {items_created.get('actions', 0)}
- Decisions: {items_created.get('decisions', 0)}
- Tasks: {items_created.get('tasks', 0)}
- Observations: {items_created.get('observations', 0)}

**Files:**
- Meeting summary: Work/Meetings/{date}_{title.replace(' ', '_')}.md
'''

    return summary


def create_meeting_summary_from_extraction(
    title: str,
    date: str,
    attendees: List[str],
    duration: int,
    takeaways: List[str],
    actions: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    granola_link: str = ''
) -> str:
    """
    Create meeting summary markdown content.

    Args:
        title: Meeting title
        date: Meeting date
        attendees: List of attendee names
        duration: Meeting duration in minutes
        takeaways: Key takeaway points
        actions: List of action dicts
        decisions: List of decision dicts
        granola_link: Link to Granola meeting

    Returns:
        Markdown content for meeting summary
    """
    attendees_str = ', '.join(attendees) if attendees else 'Not recorded'

    content = f'''# {title} - {date}

**Attendees:** {attendees_str}
**Duration:** {duration} min

## Key takeaways

'''

    for takeaway in takeaways:
        content += f"- {takeaway}\n"

    content += "\n## Actions\n\n"
    if actions:
        for action in actions:
            assignee = action.get('assignee', 'TBD')
            task = action.get('task', '')
            due = action.get('due', '')
            due_str = f" (due: {due})" if due else ""
            content += f"- {assignee} to {task}{due_str}\n"
    else:
        content += "- No actions recorded\n"

    content += "\n## Decisions\n\n"
    if decisions:
        for decision in decisions:
            text = decision.get('decision', '')
            content += f"- {text}\n"
    else:
        content += "- No decisions recorded\n"

    # Slack-ready summary
    content += "\n---\n\n**Slack-ready summary:**\n\n"
    content += f"Quick recap from {title}:\n"
    for takeaway in takeaways[:3]:
        content += f"* {takeaway}\n"

    if actions:
        content += "\nActions:\n"
        for action in actions[:5]:
            assignee = action.get('assignee', 'TBD')
            task = action.get('task', '')
            due = action.get('due', 'TBD')
            content += f"* {assignee} - {task} ({due})\n"

    content += "\n---\n"
    if granola_link:
        content += f"[View full transcript in Granola]({granola_link})\n"
    content += "Processed by Meetings Agent\n"

    return content


def save_meeting_summary(
    title: str,
    content: str,
    date: Optional[str] = None
) -> str:
    """
    Save meeting summary to Work/Meetings/.

    Args:
        title: Meeting title
        content: Markdown content
        date: Meeting date (defaults to today)

    Returns:
        Path to created file
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    project_root = Path(__file__).parent.parent
    meetings_dir = project_root / "Work" / "Meetings"
    meetings_dir.mkdir(parents=True, exist_ok=True)

    # Sanitize title for filename
    safe_title = "".join(c if c.isalnum() or c in [' ', '-', '_'] else '' for c in title)
    safe_title = safe_title.replace(' ', '_')

    filepath = meetings_dir / f"{date}_{safe_title}.md"
    filepath.write_text(content)

    return str(filepath)


# Test
if __name__ == '__main__':
    print("Testing meeting extractor...")

    # Test format_post_meeting_instructions
    instructions = format_post_meeting_instructions("Budget Review Q1")
    print(instructions[:1000])
    print("...")

    print("\n\nTest complete!")
