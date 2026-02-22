"""
Notepad processing system for extracting actionables and routing strategic content.

Three-stage workflow:
1. Capture (frictionless) → Write anything to central notepad
2. Process (command-triggered) → Extract actionables, route strategic content
3. Digest (contextual, future) → Domain agents refine their notepads
"""

import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher

# Import existing utilities and functions
from utils import (
    get_vault_path,
    sanitize_filename,
    similarity_ratio
)
from create_item import create_item


# Domain notepad paths
DOMAIN_NOTEPADS = {
    'strategy': 'Notes/Strategy/notepad.md',
    'people': 'People/notepad.md',
    'meetings': 'Meetings/Prep/notepad.md',
    'ideas': 'Inbox/Ideas/notepad.md'
}


def split_notepad_sections(content: str) -> List[str]:
    """
    Split notepad content into logical sections.

    Splits primarily by:
    - Double blank lines (strong section boundary)
    - Triple-dash separators (---)
    - Top-level markdown headers (## heading)

    Preserves:
    - Headers with their following content
    - Bullet points grouped together
    - Single blank lines within sections

    Args:
        content: Raw notepad content

    Returns:
        List of section strings with formatting preserved
    """
    if not content.strip():
        return []

    # First split by triple-dash separators
    parts = content.split('\n---\n')

    sections = []

    for part in parts:
        if not part.strip():
            continue

        # Further split by double blank lines within each part
        subsections = re.split(r'\n\n+', part)

        for subsection in subsections:
            if subsection.strip() and len(subsection.strip()) > 10:
                sections.append(subsection.strip())

    return sections


def classify_section(section_text: str) -> Dict[str, any]:
    """
    Classify a section as actionable or strategic.

    Args:
        section_text: The section content to classify

    Returns:
        Dict with 'type', 'subtype', and 'confidence' keys
    """
    text_lower = section_text.lower()
    stripped = section_text.strip()

    # Filter out non-actionable sections
    # Skip very short sections (headers, labels)
    if len(stripped) < 30:
        return {'type': 'strategic', 'subtype': 'ideas', 'confidence': 0.3}

    # Skip sections that are just markdown headers or bold labels
    if stripped.startswith('##') or (stripped.startswith('**') and stripped.endswith('**')):
        return {'type': 'strategic', 'subtype': 'ideas', 'confidence': 0.3}

    # Skip sections that are just separators or formatting
    if stripped in ['---', '***', '___']:
        return {'type': 'strategic', 'subtype': 'ideas', 'confidence': 0.2}

    # Get first line to check for header patterns
    first_line = stripped.split('\n')[0]

    # Skip bold headers with colons (like "**Actions for Maria:**" or "**Strategy development:**")
    # Pattern 1: "**Something:**" (bold text ending with colon)
    if re.match(r'^\*\*[^*]+:\*\*\s*$', first_line):
        return {'type': 'strategic', 'subtype': 'ideas', 'confidence': 0.3}

    # Pattern 2: "**Something:**" followed by minimal content (less than one line)
    if first_line.startswith('**') and first_line.endswith(':**'):
        lines = stripped.split('\n')
        # If only the header line, or header + one short line
        if len(lines) <= 2 and len(stripped) < 100:
            return {'type': 'strategic', 'subtype': 'ideas', 'confidence': 0.3}

    # Pattern 3: Numbered bold headers like "1. **Something:**" or "2. **User learning:**"
    if re.match(r'^\d+\.\s+\*\*[^*]+:\*\*', first_line):
        return {'type': 'strategic', 'subtype': 'ideas', 'confidence': 0.3}

    # Pattern 4: Sections that are ONLY a bold header with colon, nothing else substantive
    if ':**' in first_line and first_line.count('**') >= 2:
        # Check if rest of content is minimal
        rest = '\n'.join(stripped.split('\n')[1:]).strip()
        if len(rest) < 30:
            return {'type': 'strategic', 'subtype': 'ideas', 'confidence': 0.3}

    # Actionable patterns (tasks, actions, reminders, features, decisions)

    # Action patterns (with assignee)
    action_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:needs to|should|to)\s+'
    if re.search(action_pattern, section_text):
        return {'type': 'actionable', 'subtype': 'action', 'confidence': 0.9}

    # Reminder patterns
    reminder_keywords = ['remember', "don't forget", 'reminder']
    if any(kw in text_lower for kw in reminder_keywords):
        return {'type': 'actionable', 'subtype': 'reminder', 'confidence': 0.85}

    # Decision patterns
    decision_keywords = ['decided to', 'decision:', 'we will', 'agreed to']
    if any(kw in text_lower for kw in decision_keywords):
        return {'type': 'actionable', 'subtype': 'decision', 'confidence': 0.9}

    # Feature patterns (Julie improvements)
    feature_keywords = ['i want julie', 'julie should', 'add to julie', 'julie feature']
    if any(kw in text_lower for kw in feature_keywords):
        return {'type': 'actionable', 'subtype': 'feature', 'confidence': 0.9}

    # Task patterns (general actionables)
    task_verbs = [
        'need to', 'should', 'will', 'must', 'have to',
        'review', 'prepare', 'schedule', 'create', 'update',
        'write', 'send', 'complete', 'finalize', 'book'
    ]
    if any(verb in text_lower for verb in task_verbs):
        # Check if it has time-bound or deliverable indicators
        time_indicators = ['by', 'due', 'before', 'this week', 'next', 'friday', 'monday']
        has_time = any(ind in text_lower for ind in time_indicators)
        confidence = 0.85 if has_time else 0.75
        return {'type': 'actionable', 'subtype': 'task', 'confidence': confidence}

    # Strategic patterns (route to domain notepads)

    # Strategy indicators
    strategy_keywords = [
        'strategy', 'okr', 'kr', 'bet', 'monetisation', 'monetization',
        'consider', 'what if', 'approach', 'pillar', 'product area'
    ]
    if any(kw in text_lower for kw in strategy_keywords):
        return {'type': 'strategic', 'subtype': 'strategy', 'confidence': 0.8}

    # People indicators
    people_keywords = ['121', '1:1', 'feedback', 'observation', 'team', 'performance', 'role']
    has_person_name = bool(re.search(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', section_text))
    if any(kw in text_lower for kw in people_keywords) or has_person_name:
        return {'type': 'strategic', 'subtype': 'people', 'confidence': 0.75}

    # Meeting indicators
    meeting_keywords = ['meeting prep', 'agenda', 'topics', 'discuss', 'prep for', 'discussion']
    if any(kw in text_lower for kw in meeting_keywords):
        return {'type': 'strategic', 'subtype': 'meetings', 'confidence': 0.8}

    # Ideas (exploratory thoughts)
    idea_keywords = ['idea:', 'maybe', 'explore', 'could', 'might']
    if any(kw in text_lower for kw in idea_keywords):
        return {'type': 'strategic', 'subtype': 'ideas', 'confidence': 0.7}

    # Default: classify as strategic (safer than creating wrong items)
    return {'type': 'strategic', 'subtype': 'ideas', 'confidence': 0.5}


def extract_actionable_details(section_text: str, subtype: str) -> Dict[str, any]:
    """
    Extract structured details from an actionable section.

    Args:
        section_text: The section content
        subtype: The action subtype (task, action, reminder, feature, decision)

    Returns:
        Dict with title, details, due_date, assignee, tags fields
    """
    lines = section_text.strip().split('\n')
    first_line = lines[0].strip()

    # Initialize result
    result = {
        'title': '',
        'details': '',
        'due_date': None,
        'assignee': None,
        'tags': []
    }

    # Extract assignee for actions (from "Name needs to..." pattern)
    if subtype == 'action':
        assignee_match = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:needs to|should|to)\s+(.+)', first_line)
        if assignee_match:
            result['assignee'] = assignee_match.group(1).strip()
            title_text = assignee_match.group(2).strip()
        else:
            # If no clear assignee, extract from line and convert to task
            title_text = first_line
    else:
        title_text = first_line

    # Clean up title text
    # Remove common prefixes
    for prefix in ['need to ', 'should ', 'will ', 'must ', 'have to ',
                   'remember to ', "don't forget to ", 'decided to ',
                   'i want julie to ', 'julie should ']:
        if title_text.lower().startswith(prefix):
            title_text = title_text[len(prefix):]
            break

    # Extract due date from text
    date_patterns = [
        (r'by\s+(next\s+)?friday', 'next_friday'),
        (r'by\s+(next\s+)?monday', 'next_monday'),
        (r'by\s+(\d{4}-\d{2}-\d{2})', 'date'),
        (r'due\s+(\d{4}-\d{2}-\d{2})', 'date'),
        (r'before\s+(\d{4}-\d{2}-\d{2})', 'date'),
    ]

    for pattern, date_type in date_patterns:
        match = re.search(pattern, title_text.lower())
        if match:
            if date_type == 'date':
                result['due_date'] = match.group(1)
            elif date_type == 'next_friday':
                # Calculate next Friday from today
                today = datetime.now()
                days_ahead = 4 - today.weekday()  # Friday is 4
                if days_ahead <= 0:
                    days_ahead += 7
                from datetime import timedelta
                next_friday = today + timedelta(days=days_ahead)
                result['due_date'] = next_friday.strftime('%Y-%m-%d')
            elif date_type == 'next_monday':
                # Calculate next Monday
                today = datetime.now()
                days_ahead = 0 - today.weekday()  # Monday is 0
                if days_ahead <= 0:
                    days_ahead += 7
                from datetime import timedelta
                next_monday = today + timedelta(days=days_ahead)
                result['due_date'] = next_monday.strftime('%Y-%m-%d')

            # Remove date reference from title
            title_text = re.sub(pattern, '', title_text, flags=re.IGNORECASE).strip()
            break

    # Extract #hashtags as tags
    hashtags = re.findall(r'#(\w+)', title_text)
    if hashtags:
        result['tags'] = hashtags
        # Remove hashtags from title
        title_text = re.sub(r'#\w+', '', title_text).strip()

    # Clean up title (remove punctuation at end)
    title_text = title_text.rstrip('.,;:!?')

    # Create short title (3-8 words)
    words = title_text.split()
    if len(words) > 8:
        result['title'] = ' '.join(words[:8])
        result['details'] = title_text
    else:
        result['title'] = title_text

    # Add remaining lines as details
    if len(lines) > 1:
        additional_details = '\n'.join(lines[1:]).strip()
        if result['details']:
            result['details'] += '\n\n' + additional_details
        else:
            result['details'] = additional_details

    return result


def determine_domain(section_text: str) -> str:
    """
    Classify strategic content by domain for routing.

    Args:
        section_text: The section content

    Returns:
        Domain string: 'strategy' | 'people' | 'meetings' | 'ideas'
    """
    text_lower = section_text.lower()

    # Strategy indicators
    if any(kw in text_lower for kw in ['strategy', 'okr', 'kr', 'bet', 'monetisation', 'product area', 'pillar']):
        return 'strategy'

    # People indicators
    if any(kw in text_lower for kw in ['121', '1:1', 'feedback', 'observation', 'team', 'performance', 'role']):
        return 'people'

    # Check for person names
    if re.search(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', section_text):
        return 'people'

    # Meeting indicators
    if any(kw in text_lower for kw in ['meeting prep', 'agenda', 'topics', 'discuss', 'prep for']):
        return 'meetings'

    # Default to ideas for exploratory/ambiguous content
    return 'ideas'


def check_memory_for_duplicates(title: str, item_type: str) -> List[Dict[str, any]]:
    """
    Query claude-mem for similar items to detect duplicates.

    Args:
        title: The item title to check
        item_type: The type of item (task, action, etc.)

    Returns:
        List of similar items with similarity scores
    """
    try:
        # This function will be called by Claude Code which has access to MCP tools
        # For now, return empty list - Claude Code will intercept and call MCP
        # The actual MCP call will be:
        # mcp__plugin_claude-mem_mcp-search__search({
        #     query: f"tasks Similar tasks to {title}",
        #     limit: 3,
        #     project: "Chief_of_staff"
        # })
        return []
    except Exception as e:
        print(f"Warning: Memory check failed: {e}")
        return []


def append_to_domain_notepad(domain: str, section_text: str, source_archive: str):
    """
    Append strategic content to the appropriate domain notepad.

    Args:
        domain: The target domain (strategy, people, meetings, ideas)
        section_text: The content to append
        source_archive: The archive filename for reference
    """
    vault_path = get_vault_path()
    notepad_path = vault_path / DOMAIN_NOTEPADS[domain]

    # Create timestamp
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M')

    # Format content block
    content_block = f"""
---
**Captured:** {timestamp}
**Source:** {source_archive}

{section_text}

---
"""

    # Append to notepad
    if notepad_path.exists():
        existing = notepad_path.read_text()
        notepad_path.write_text(existing + content_block)
    else:
        # Create with header
        header = f"# {domain.title()} Notepad\n\nStrategic thoughts routed from central notepad for later digestion.\n\n---\n"
        notepad_path.write_text(header + content_block)


def display_classification_results(actionables: List[Tuple], strategic_content: List[Tuple],
                                   memory_checks: Dict, detailed: bool = False) -> str:
    """
    Pretty-print classification results for user review.

    Args:
        actionables: List of (section_text, classification, extracted_details) tuples
        strategic_content: List of (section_text, domain) tuples
        memory_checks: Dict mapping titles to list of similar items from memory
        detailed: If True, show full extracted details for each item

    Returns:
        Formatted string for display
    """
    output = ["\n" + "="*60]
    output.append("NOTEPAD PROCESSING RESULTS")
    output.append("="*60)

    # Actionables section
    if actionables:
        output.append(f"\n📋 ACTIONABLES ({len(actionables)} items):")
        output.append("-" * 60)

        # Group by subtype
        by_type = {}
        for section, classification, details in actionables:
            subtype = classification['subtype']
            if subtype not in by_type:
                by_type[subtype] = []
            by_type[subtype].append((section, details))

        for subtype, items in by_type.items():
            output.append(f"\n  {subtype.upper()}S ({len(items)}):")
            for i, (section, details) in enumerate(items, 1):
                if detailed:
                    output.append(f"\n    {i}. Title: \"{details['title']}\"")
                    if details.get('details'):
                        output.append(f"       Details: {details['details'][:100]}{'...' if len(details.get('details', '')) > 100 else ''}")
                    if details.get('assignee'):
                        output.append(f"       Assignee: {details['assignee']}")
                    if details.get('due_date'):
                        output.append(f"       Due Date: {details['due_date']}")
                    if details.get('tags'):
                        output.append(f"       Tags: {', '.join(details['tags'])}")
                    # Show actual file path based on item type
                    folder_map = {
                        'task': 'Inbox/Tasks',
                        'action': 'Inbox/Actions',
                        'reminder': 'Inbox/Reminders',
                        'feature': 'Inbox/Features',
                        'idea': 'Inbox/Ideas',
                        'decision': 'Decisions'
                    }
                    folder = folder_map.get(subtype, f'Inbox/{subtype.title()}s')
                    safe_title = details['title'].replace(' ', '_')
                    output.append(f"       → Will create: Work/{folder}/{subtype}_{safe_title}.md")
                else:
                    output.append(f"    {i}. {details['title']}")
                    if details.get('assignee'):
                        output.append(f"       Assignee: {details['assignee']}")
                    if details.get('due_date'):
                        output.append(f"       Due: {details['due_date']}")

                # Check for memory duplicates
                title = details['title']
                if title in memory_checks and memory_checks[title]:
                    output.append(f"       ⚠️  Similar items found in memory:")
                    for similar in memory_checks[title][:2]:  # Show top 2
                        output.append(f"          - {similar.get('title', 'Unknown')}")
    else:
        output.append("\n📋 ACTIONABLES: None found")

    # Strategic content section
    if strategic_content:
        output.append(f"\n\n🎯 STRATEGIC CONTENT ({len(strategic_content)} sections):")
        output.append("-" * 60)

        # Group by domain
        by_domain = {}
        for section, domain in strategic_content:
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append(section)

        for domain, sections in by_domain.items():
            output.append(f"\n  {domain.upper()} ({len(sections)} sections):")
            if detailed:
                domain_path = DOMAIN_NOTEPADS.get(domain, f'{domain}/notepad.md')
                output.append(f"       → Will append to: Work/{domain_path}")
            for i, section in enumerate(sections, 1):
                # Show first line as preview
                first_line = section.split('\n')[0][:60]
                if detailed and i <= 3:  # Show first 3 in detail
                    output.append(f"\n    {i}. Preview:")
                    lines = section.split('\n')[:3]
                    for line in lines:
                        output.append(f"       {line[:70]}{'...' if len(line) > 70 else ''}")
                else:
                    output.append(f"    {i}. {first_line}...")

            if detailed and len(sections) > 3:
                output.append(f"    ... and {len(sections) - 3} more sections")
    else:
        output.append("\n\n🎯 STRATEGIC CONTENT: None found")

    output.append("\n" + "="*60)
    if not detailed:
        output.append("\nReview the above classification.")
        output.append("Type 'yes' to proceed, 'edit' to modify, or 'cancel' to abort.")
    output.append("="*60 + "\n")

    return '\n'.join(output)


def process_notepad(mode='interactive'):
    """
    Main workflow to process the central notepad.

    Args:
        mode: 'interactive' (prompt user), 'preview' (show only), 'confirm' (execute without prompt)

    Returns:
        Summary message of what was processed, or classification results for preview mode
    """
    vault_path = get_vault_path()
    notepad_path = vault_path / "1-Notepad" / "Notepad.md"

    # Check if notepad exists
    if not notepad_path.exists():
        return "❌ Central notepad not found at Work/1-Notepad/Notepad.md"

    # Read notepad content
    content = notepad_path.read_text()

    if not content.strip():
        # Empty notepad - just archive
        if mode == 'preview':
            return "ℹ️  Notepad is empty. Nothing to process."
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
        archive_path = vault_path / "1-Notepad" / "Archive" / f"notepad_{timestamp}.md"
        archive_path.write_text(content)
        return "ℹ️  Notepad was empty. Archived and cleared."

    # Split into sections
    sections = split_notepad_sections(content)

    if not sections:
        return "ℹ️  No processable sections found in notepad."

    # Classify sections
    actionables = []
    strategic_content = []
    memory_checks = {}

    for section in sections:
        classification = classify_section(section)

        if classification['type'] == 'actionable':
            details = extract_actionable_details(section, classification['subtype'])
            actionables.append((section, classification, details))

            # Check memory for duplicates
            # NOTE: This is a placeholder - Claude Code will intercept and call MCP
            memory_results = check_memory_for_duplicates(details['title'], classification['subtype'])
            if memory_results:
                memory_checks[details['title']] = memory_results
        else:
            domain = determine_domain(section)
            strategic_content.append((section, domain))

    # Display classification results
    # Use detailed view for preview mode
    display_text = display_classification_results(actionables, strategic_content, memory_checks, detailed=(mode=='preview'))

    # Handle different modes
    if mode == 'preview':
        # Return results without prompting or processing (don't print, just return)
        summary = ["\n📊 PREVIEW MODE - No changes made to notepad\n"]
        summary.append(f"Found {len(actionables)} actionables and {len(strategic_content)} strategic sections.")
        summary.append("\n✅ Review the details above.")
        summary.append("If you approve, I'll run: ./pos \"process notepad confirm\"")
        return display_text + '\n'.join(summary)

    # For interactive and confirm modes, print the display
    print(display_text)

    if mode == 'interactive':
        # Get user confirmation
        user_response = input("Your choice: ").strip().lower()

        if user_response == 'cancel':
            return "❌ Processing cancelled. Notepad unchanged."

        if user_response == 'edit':
            return "✏️  Edit mode not yet implemented. Please run again or cancel."

        if user_response != 'yes':
            return "❌ Invalid response. Processing cancelled."

    # mode == 'confirm' or user said 'yes' in interactive mode
    # Proceed with processing
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    archive_filename = f"notepad_{timestamp}.md"

    # Create actionable items
    created_items = []
    for section, classification, details in actionables:
        subtype = classification['subtype']
        try:
            # Build kwargs for create_item
            kwargs = {}
            if details.get('assignee'):
                kwargs['assignee'] = details['assignee']
            if subtype == 'reminder' and details.get('due_date'):
                kwargs['reminder_date'] = details['due_date']
                due_date = None  # Reminders use reminder_date, not due_date
            else:
                due_date = details.get('due_date')

            # Create the item
            file_path = create_item(
                item_type=subtype,
                title=details['title'],
                due_date=due_date,
                details=details.get('details', ''),
                tags=details.get('tags'),
                **kwargs
            )
            created_items.append((subtype, details['title']))

            # Store in memory
            # NOTE: Claude Code will intercept and call MCP save_memory

        except Exception as e:
            print(f"⚠️  Warning: Could not create {subtype} '{details['title']}': {e}")

    # Route strategic content to domain notepads
    routed_content = {}
    for section, domain in strategic_content:
        try:
            append_to_domain_notepad(domain, section, archive_filename)
            routed_content[domain] = routed_content.get(domain, 0) + 1
        except Exception as e:
            print(f"⚠️  Warning: Could not route to {domain} notepad: {e}")

    # Archive original notepad
    archive_path = vault_path / "1-Notepad" / "Archive" / archive_filename
    archive_path.write_text(content)

    # Clear central notepad
    header = "# Notepad\n\nCapture anything here - process later with `./pos \"process notepad\"`\n\n---\n\n"
    notepad_path.write_text(header)

    # Build summary report
    summary = ["\n" + "="*60]
    summary.append("✅ NOTEPAD PROCESSING COMPLETE")
    summary.append("="*60)
    summary.append(f"\n📋 Created {len(created_items)} items:")

    # Group by type
    by_type = {}
    for item_type, title in created_items:
        if item_type not in by_type:
            by_type[item_type] = []
        by_type[item_type].append(title)

    for item_type, titles in by_type.items():
        summary.append(f"  {item_type}s: {len(titles)}")

    if routed_content:
        summary.append(f"\n🎯 Routed {sum(routed_content.values())} sections:")
        for domain, count in routed_content.items():
            summary.append(f"  {domain}: {count} sections")

    summary.append(f"\n📁 Archived to: {archive_filename}")
    summary.append(f"🆕 Central notepad cleared and ready for new capture")
    summary.append("="*60 + "\n")

    return '\n'.join(summary)


if __name__ == "__main__":
    # For testing
    result = process_notepad()
    print(result)
