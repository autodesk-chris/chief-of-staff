#!/usr/bin/env python3
"""
Daily Summary Interview System

Interactive end-of-day interview that collects summary of daily work.
Gathers context from 4Ps, today summary, session logs, and observations.
Generates structured bullet-point summary for weekly 4Ps writing.
"""

from datetime import datetime, timedelta
from pathlib import Path
import re
from utils import get_vault_path, get_observations_path, extract_title_from_file, parse_tags
from session_log import read_session_log, parse_session_log
from create_item import create_item


class InterviewCancelled(Exception):
    """Exception raised when user cancels interview."""
    pass


def extract_actionable_items(summary_content):
    """
    Scan summary content for actionable items using pattern matching.

    Looks for phrases indicating tasks, actions, ideas, or features.

    Args:
        summary_content: The full summary markdown content

    Returns:
        List of dictionaries with 'text' and 'context' keys
    """
    actionable_patterns = [
        r'(?:need to|should|will|must|have to|going to)\s+(.+?)(?:\.|$)',
        r'(?:follow up|check|send|review|prepare|schedule|create|write|update|finalize|complete)\s+(.+?)(?:\.|$)',
        r'(?:todo|action item):\s*(.+?)(?:\.|$)',
        r'(?:next steps?|action):\s*(.+?)(?:\.|$)',
    ]

    items = []
    lines = summary_content.split('\n')

    for i, line in enumerate(lines):
        line_lower = line.lower().strip()

        # Skip headers, frontmatter, and very short lines
        if not line_lower or line.startswith('#') or line.startswith('---') or len(line_lower) < 10:
            continue

        # Check each pattern
        for pattern in actionable_patterns:
            matches = re.finditer(pattern, line_lower, re.IGNORECASE)
            for match in matches:
                action_text = match.group(1).strip()

                # Clean up the text
                action_text = action_text.rstrip('.,;:')

                # Skip if too short or looks like a heading
                if len(action_text) < 5:
                    continue

                # Get context (section this appears in)
                context = _find_section_context(lines, i)

                items.append({
                    'text': action_text,
                    'context': context,
                    'original_line': line.strip()
                })

    # Deduplicate based on similar text
    unique_items = []
    seen_texts = set()

    for item in items:
        text_normalized = item['text'].lower().strip()
        if text_normalized not in seen_texts:
            seen_texts.add(text_normalized)
            unique_items.append(item)

    return unique_items


def _find_section_context(lines, line_index):
    """Find the section header for a given line."""
    # Look backwards for the nearest ## heading
    for i in range(line_index, -1, -1):
        if lines[i].startswith('## '):
            return lines[i].replace('## ', '').strip()
    return "General"


def process_actionable_items(summary_path):
    """
    Process actionable items from the summary and create tasks/actions/ideas/features.

    Args:
        summary_path: Path to the summary file

    Returns:
        List of created item paths
    """
    # Read summary content
    content = summary_path.read_text(encoding='utf-8')

    # Extract actionable items
    items = extract_actionable_items(content)

    if not items:
        print("\nNo actionable items identified in the summary.")
        return []

    print("\n" + "="*60)
    print("Actionable Items Identified")
    print("="*60)
    print(f"\nFound {len(items)} potential items to create:")
    print()

    # Present items to user
    for i, item in enumerate(items, 1):
        print(f"{i}. {item['text']}")
        print(f"   Context: {item['context']}")
        print()

    # Ask user what to do with each item
    proceed = input("Would you like to create items from these? (yes/no): ").strip().lower()
    if proceed not in ['yes', 'y']:
        print("Skipped item creation.")
        return []

    created_items = []

    for i, item in enumerate(items, 1):
        print(f"\n--- Item {i}/{len(items)} ---")
        print(f"Text: {item['text']}")
        print(f"Context: {item['context']}")

        # Ask what type this should be
        print("\nWhat type should this be?")
        print("  1. Task (due-dated work)")
        print("  2. Action (quick actionable item)")
        print("  3. Idea (potential enhancement)")
        print("  4. Feature (larger implementation)")
        print("  5. Skip this item")

        choice = input("Choice (1-5): ").strip()

        if choice == '5' or not choice:
            print("Skipped.")
            continue

        type_map = {
            '1': 'task',
            '2': 'action',
            '3': 'idea',
            '4': 'feature'
        }

        item_type = type_map.get(choice)
        if not item_type:
            print("Invalid choice, skipping.")
            continue

        # Get title (offer default)
        default_title = item['text'][:50]  # Limit length
        title_input = input(f"Title (press Enter for: '{default_title}'): ").strip()
        title = title_input if title_input else default_title

        # Get details
        details = input("Details (optional, press Enter to skip): ").strip()

        # Get due date if task
        due_date = None
        if item_type == 'task':
            due_input = input("Due date (YYYY-MM-DD, press Enter to skip): ").strip()
            if due_input:
                # Validate date format
                try:
                    datetime.strptime(due_input, '%Y-%m-%d')
                    due_date = due_input
                except ValueError:
                    print("Invalid date format, skipping due date.")

        # Get tags
        tags_input = input("Tags (comma-separated, press Enter to skip): ").strip()
        tags = parse_tags(tags_input) if tags_input else []

        # Create the item
        try:
            file_path = create_item(
                item_type=item_type,
                title=title,
                due_date=due_date,
                details=details,
                tags=tags
            )
            created_items.append(file_path)
            print(f"✓ Created {item_type}: {file_path}")
        except Exception as e:
            print(f"✗ Error creating item: {e}")

    if created_items:
        print(f"\n✓ Created {len(created_items)} items from summary")

        # Auto-update today document
        from summary import update_today_document
        today_path = update_today_document()
        print(f"✓ Updated today summary: {today_path}")

    return created_items


def gather_context():
    """
    Automatically read context documents.

    Returns:
        Dict with keys: week_4ps, today_summary, session_log, observations, errors
    """
    context = {
        'week_4ps': None,
        'today_summary': None,
        'session_log': None,
        'observations': [],
        'errors': []
    }

    # Read this week's 4Ps
    try:
        fourps_path = Path(get_vault_path()) / "4Ps" / "4Ps_2026.md"
        if fourps_path.exists():
            content = fourps_path.read_text(encoding='utf-8')
            current_week = extract_current_week_section(content)
            context['week_4ps'] = parse_4ps_section(current_week)
    except Exception as e:
        context['errors'].append(f"Could not read 4Ps: {e}")

    # Read today summary
    try:
        today = datetime.now().date()
        today_path = Path(get_vault_path()) / "Inbox" / "Today" / f"today_{today.strftime('%Y-%m-%d')}.md"
        if today_path.exists():
            context['today_summary'] = parse_today_summary(today_path.read_text(encoding='utf-8'))
    except Exception as e:
        context['errors'].append(f"Could not read today summary: {e}")

    # Read session log
    try:
        today = datetime.now().date()
        session_content = read_session_log(today)
        if session_content:
            context['session_log'] = parse_session_log(session_content)
    except Exception as e:
        context['errors'].append(f"Could not read session log: {e}")

    # Read observations from today - DISABLED
    # try:
    #     obs_path = get_observations_path()
    #     today = datetime.now().date()
    #     if obs_path.exists():
    #         for obs_file in obs_path.glob(f"observation_*_{today.strftime('%Y-%m-%d')}*.md"):
    #             context['observations'].append({
    #                 'file': obs_file.name,
    #                 'title': extract_title_from_file(obs_file)
    #             })
    # except Exception as e:
    #     context['errors'].append(f"Could not read observations: {e}")

    return context


def extract_current_week_section(fourps_content):
    """
    Extract the section for current week from 4Ps document.

    Looks for heading matching current week date.
    Returns section text from that heading to next ### heading or end of file.
    """
    today = datetime.now().date()

    # Calculate start of current week (Monday)
    days_since_monday = today.weekday()
    week_start = today - timedelta(days=days_since_monday)

    # Format to match 4Ps heading: "### Week beginning 05 Jan 2026"
    week_heading = f"### Week beginning {week_start.strftime('%d %b %Y')}"

    # Find the section
    lines = fourps_content.split('\n')
    section_start = None
    section_lines = []

    for i, line in enumerate(lines):
        if line.startswith(week_heading):
            section_start = i
        elif section_start is not None:
            # Check if we've hit the next week section
            if line.startswith('###'):
                break
            section_lines.append(line)

    if section_start is None:
        # Try alternate format without leading zero: "### Week beginning 5 Jan 2026"
        week_heading_alt = f"### Week beginning {week_start.strftime('%-d %b %Y')}"
        for i, line in enumerate(lines):
            if line.startswith(week_heading_alt):
                section_start = i
            elif section_start is not None:
                if line.startswith('###'):
                    break
                section_lines.append(line)

    return '\n'.join(section_lines) if section_lines else None


def parse_4ps_section(section_text):
    """
    Parse 4Ps section into structured dict.

    Extracts: Priorities, Progress, Plans, Problems

    Returns:
        Dict with lists for each section
    """
    if not section_text:
        return {
            'priorities': [],
            'progress': [],
            'plans': [],
            'problems': []
        }

    result = {
        'priorities': [],
        'progress': [],
        'plans': [],
        'problems': []
    }

    lines = section_text.split('\n')
    current_section = None
    current_content = []

    for line in lines:
        line_stripped = line.strip()

        # Detect section headers
        if line_stripped.lower() in ['priorities', 'priority']:
            if current_section and current_content:
                result[current_section] = parse_section_content(current_content)
            current_section = 'priorities'
            current_content = []
        elif line_stripped.lower() == 'progress':
            if current_section and current_content:
                result[current_section] = parse_section_content(current_content)
            current_section = 'progress'
            current_content = []
        elif line_stripped.lower() in ['plans', 'plan']:
            if current_section and current_content:
                result[current_section] = parse_section_content(current_content)
            current_section = 'plans'
            current_content = []
        elif line_stripped.lower() == 'problems':
            if current_section and current_content:
                result[current_section] = parse_section_content(current_content)
            current_section = 'problems'
            current_content = []
        elif current_section and line_stripped:
            current_content.append(line_stripped)

    # Don't forget the last section
    if current_section and current_content:
        result[current_section] = parse_section_content(current_content)

    return result


def parse_section_content(lines):
    """
    Parse section content into list of items.

    Handles bullet points, numbered lists, and plain paragraphs.
    """
    items = []
    current_item = []

    for line in lines:
        line = line.strip()
        if not line:
            if current_item:
                items.append(' '.join(current_item))
                current_item = []
            continue

        # Check if this is a bullet or number
        if line.startswith('- ') or line.startswith('* '):
            if current_item:
                items.append(' '.join(current_item))
            current_item = [line[2:]]
        elif re.match(r'^\d+\. ', line):
            if current_item:
                items.append(' '.join(current_item))
            current_item = [line.split('. ', 1)[1]]
        else:
            current_item.append(line)

    # Don't forget the last item
    if current_item:
        items.append(' '.join(current_item))

    return items


def parse_today_summary(summary_content):
    """
    Parse today summary into structured dict.

    Extracts task counts and lists of tasks.

    Returns:
        Dict with task lists
    """
    result = {
        'tasks_due_today': [],
        'tasks_completed': [],
        'tasks_due_week': [],
        'tasks_in_progress': []
    }

    lines = summary_content.split('\n')
    current_section = None

    for line in lines:
        line_stripped = line.strip()

        # Detect sections
        if '## Tasks Due Today' in line:
            current_section = 'tasks_due_today'
        elif '## Tasks Due This Week' in line:
            current_section = 'tasks_due_week'
        elif current_section and line_stripped.startswith('- '):
            # Check if completed (strikethrough)
            if line_stripped.startswith('- ~~') and '~~' in line_stripped[4:]:
                # Extract task text (remove strikethrough)
                task_text = line_stripped[4:].replace('~~', '').strip()
                result['tasks_completed'].append(task_text)
            else:
                # Active task
                task_text = line_stripped[2:].strip()

                if current_section == 'tasks_due_today':
                    result['tasks_due_today'].append(task_text)
                elif current_section == 'tasks_due_week':
                    result['tasks_due_week'].append(task_text)

    return result


class DailySummaryInterview:
    """
    Manages multi-turn conversation for daily summary interview.

    Handles context gathering, validation, questioning, and summary generation.
    """

    def __init__(self):
        self.context = {}
        self.responses = {}
        self.current_question = 0
        self.questions = [
            ('meetings', self._ask_meetings),
            ('progress', self._ask_progress),
            ('decisions', self._ask_decisions),
            ('slack', self._ask_slack),
            ('surprises', self._ask_surprises),
            ('other', self._ask_other)
        ]

    def start(self):
        """
        Begin interview - gather context and present validation.

        Returns:
            Path to saved summary file, or None if cancelled
        """
        print("Gathering context for daily summary...")
        self.context = gather_context()

        # Present validation
        self._present_context()

        # Get user confirmation
        response = input("\nReady to proceed with interview? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Interview cancelled.")
            return None

        # Start interview loop
        try:
            return self._conduct_interview()
        except InterviewCancelled:
            print("\nInterview cancelled by user.")
            return None

    def _conduct_interview(self):
        """
        Run through question sequence.

        Returns:
            Path to saved summary file
        """
        print("\n" + "="*60)
        print("Daily Summary Interview")
        print("="*60)
        print("(Type 'cancel' or 'exit' at any time to stop)")
        print()

        for question_key, question_func in self.questions:
            try:
                response = question_func()
                self.responses[question_key] = response
            except InterviewCancelled:
                raise

        # Generate summary
        return self._generate_summary()

    def _present_context(self):
        """Show user what context was gathered."""
        print("\n" + "="*60)
        print("Daily Summary Interview - Context Gathered")
        print("="*60)

        # Show 4Ps context
        if self.context.get('week_4ps'):
            fourps = self.context['week_4ps']
            print("\n✓ This week's 4Ps:")

            if fourps.get('priorities'):
                print("  Priorities:")
                for i, p in enumerate(fourps['priorities'][:3], 1):
                    print(f"    {i}. {p}")

            if fourps.get('plans'):
                print("  Plans:")
                for i, p in enumerate(fourps['plans'][:3], 1):
                    print(f"    {i}. {p}")
        else:
            print("\n⚠ Could not find this week's 4Ps section")

        # Show today summary context
        if self.context.get('today_summary'):
            today = self.context['today_summary']
            completed_count = len(today.get('tasks_completed', []))
            active_count = len(today.get('tasks_due_today', []))

            print("\n✓ Today's summary:")
            print(f"  - Tasks completed: {completed_count}")
            print(f"  - Tasks in progress: {active_count}")
        else:
            print("\n⚠ Could not find today's summary")

        # Show session log context
        if self.context.get('session_log'):
            session_count = len(self.context['session_log'])
            print(f"\n✓ Claude sessions logged: {session_count}")
        else:
            print("\n  No Claude sessions logged today (run './pos \"session: [what you worked on]\"' to log)")

        # Show observations - DISABLED
        # if self.context.get('observations'):
        #     print(f"\n✓ Team observations: {len(self.context['observations'])}")

        # Show errors
        if self.context.get('errors'):
            print("\n⚠ Warnings:")
            for error in self.context['errors']:
                print(f"  - {error}")

    def _check_cancel(self, response):
        """Check if user wants to cancel."""
        if response and response.lower() in ['cancel', 'exit', 'quit']:
            confirm = input("   Cancel interview? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                raise InterviewCancelled()

    def _ask_meetings(self):
        """Ask about meetings."""
        print("\n1. MEETINGS AND DISCUSSIONS")
        print("   What meetings did you have today? List the key ones.")
        print("   (or type 'none' to skip)")
        meetings_input = input("   Your response: ").strip()
        self._check_cancel(meetings_input)

        if not meetings_input or meetings_input.lower() in ['none', 'no', 'n/a', 'skip']:
            return None

        # For each meeting mentioned, ask for takeaways
        meeting_details = []
        meeting_list = [m.strip() for m in meetings_input.split(',')]

        for meeting in meeting_list:
            if meeting:
                print(f"\n   Any key decisions or takeaways from '{meeting}'?")
                takeaway = input("   Takeaway: ").strip()
                self._check_cancel(takeaway)

                meeting_details.append({
                    'name': meeting,
                    'takeaway': takeaway if takeaway else None
                })

        return meeting_details

    def _ask_progress(self):
        """Ask about progress on weekly plans."""
        print("\n2. PROGRESS ON WEEKLY PLANS")

        if self.context.get('week_4ps') and self.context['week_4ps'].get('plans'):
            plans = self.context['week_4ps']['plans'][:3]  # Show top 3
            print("   Looking at your plans for this week:")
            for i, plan in enumerate(plans, 1):
                print(f"   {i}. {plan}")
            print("   What progress did you make today?")
        else:
            print("   What progress did you make on your weekly plans today?")

        print("   (or type 'none' to skip)")
        response = input("   Your response: ").strip()
        self._check_cancel(response)

        return response if response and response.lower() not in ['none', 'no', 'n/a', 'skip'] else None

    def _ask_decisions(self):
        """Ask about key decisions."""
        print("\n3. KEY DECISIONS")
        print("   What important decisions were made today?")
        print("   (By you, your team, or leadership)")
        print("   (or type 'none' to skip)")
        response = input("   Your response: ").strip()
        self._check_cancel(response)

        return response if response and response.lower() not in ['none', 'no', 'n/a', 'skip'] else None

    def _ask_slack(self):
        """Ask about Slack highlights."""
        print("\n4. COMMUNICATION HIGHLIGHTS")
        print("   Any important Slack discussions or messages worth noting?")
        print("   (or type 'none' to skip)")
        response = input("   Your response: ").strip()
        self._check_cancel(response)

        return response if response and response.lower() not in ['none', 'no', 'n/a', 'skip'] else None

    def _ask_surprises(self):
        """Ask about surprises or changes."""
        print("\n5. SURPRISES AND CHANGES")
        print("   Anything unexpected come up today? Changes to plans or new info?")
        print("   (or type 'none' to skip)")
        response = input("   Your response: ").strip()
        self._check_cancel(response)

        return response if response and response.lower() not in ['none', 'no', 'n/a', 'skip'] else None

    def _ask_other(self):
        """Catch-all question."""
        print("\n6. OTHER NOTES")
        print("   Anything else important I should capture for today's summary?")
        print("   (or type 'none' to skip)")
        response = input("   Your response: ").strip()
        self._check_cancel(response)

        return response if response and response.lower() not in ['none', 'no', 'n/a', 'skip'] else None

    def _generate_summary(self):
        """
        Generate summary document from responses.

        Returns:
            Path to saved summary file
        """
        print("\n" + "="*60)
        print("Generating summary...")
        print("="*60)

        today = datetime.now().date()
        summary_path = Path(get_vault_path()) / "Inbox" / "Today" / f"summary_{today.strftime('%Y-%m-%d')}.md"

        # Check if file already exists
        if summary_path.exists():
            print(f"\nSummary for {today} already exists: {summary_path}")
            overwrite = input("Overwrite existing summary? (yes/no): ").strip().lower()
            if overwrite not in ['yes', 'y']:
                print("Cancelled. Existing summary not modified.")
                return None

        # Generate markdown content
        content = self._build_summary_content()

        # Write to file
        summary_path.write_text(content, encoding='utf-8')

        print(f"\n✓ Daily summary saved: {summary_path}")

        # Automatically process actionable items
        try:
            process_actionable_items(summary_path)
        except Exception as e:
            print(f"\n⚠ Error processing actionable items: {e}")

        return summary_path

    def _build_summary_content(self):
        """Build the markdown content for the summary."""
        today = datetime.now().date()
        now = datetime.now()

        # Calculate week start for reference
        days_since_monday = today.weekday()
        week_start = today - timedelta(days=days_since_monday)

        # Build frontmatter
        content = f"""---
type: daily-summary
date: {today.strftime('%Y-%m-%d')}
created: {now.strftime('%Y-%m-%d %H:%M:%S')}
week-reference: Week beginning {week_start.strftime('%d %b %Y')}
---

# Daily Summary - {today.strftime('%B %d, %Y')}

## Context

"""

        # Add weekly priorities context
        if self.context.get('week_4ps') and self.context['week_4ps'].get('priorities'):
            content += "**Weekly priorities:**\n"
            for priority in self.context['week_4ps']['priorities'][:3]:
                content += f"- {priority}\n"
            content += "\n"

        # Add today's task context
        if self.context.get('today_summary'):
            today_summary = self.context['today_summary']
            completed_count = len(today_summary.get('tasks_completed', []))
            active_count = len(today_summary.get('tasks_due_today', []))
            content += f"**Today's tasks:**\n"
            content += f"- Completed: {completed_count} tasks\n"
            content += f"- In progress: {active_count} tasks\n\n"

        # Add Claude work sessions
        if self.context.get('session_log'):
            content += "## Claude Work Sessions\n\n"
            for session in self.context['session_log']:
                content += f"**Session {self.context['session_log'].index(session) + 1} ({session['time']}):**\n"
                content += session['summary'] + "\n\n"

        # Add meetings
        meetings = self.responses.get('meetings')
        if meetings:
            content += "## Meetings and Discussions\n\n"
            for meeting in meetings:
                content += f"**{meeting['name']}**\n"
                if meeting.get('takeaway'):
                    content += f"- {meeting['takeaway']}\n"
                content += "\n"

        # Add progress
        progress = self.responses.get('progress')
        if progress:
            content += "## Progress on Weekly Plans\n\n"
            content += f"- {progress}\n\n"

        # Add decisions
        decisions = self.responses.get('decisions')
        if decisions:
            content += "## Key Decisions\n\n"
            content += f"- {decisions}\n\n"

        # Add slack/communication
        slack = self.responses.get('slack')
        if slack:
            content += "## Communication Highlights\n\n"
            content += f"- Slack: {slack}\n\n"

        # Add surprises
        surprises = self.responses.get('surprises')
        if surprises:
            content += "## Surprises and Changes\n\n"
            content += f"- {surprises}\n\n"

        # Add other notes
        other = self.responses.get('other')
        if other:
            content += "## Other Notes\n\n"
            content += f"- {other}\n\n"

        # Add observations - DISABLED
        # if self.context.get('observations'):
        #     content += "## Observations\n\n"
        #     for obs in self.context['observations']:
        #         content += f"- {obs['title']} ([{obs['file']}](../Team/Observations/{obs['file']}))\n"
        #     content += "\n"

        # Footer
        content += "---\n\n*Generated by Chief of Staff Personal OS*\n"

        return content


def conduct_interview():
    """
    Entry point for daily summary interview command.

    Returns:
        Path to summary file if successful, None if cancelled
    """
    interview = DailySummaryInterview()
    return interview.start()


if __name__ == '__main__':
    # Test the interview
    result = conduct_interview()
    if result:
        print(f"\nSuccess! Summary saved to: {result}")
    else:
        print("\nInterview was cancelled.")
