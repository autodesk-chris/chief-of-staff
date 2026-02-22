#!/usr/bin/env python3
"""
MFM (Monthly Focus Meeting) Agent for Julie (Chief of Staff agent system)

Provides MFM review and post-meeting summary workflows.
Uses five-dimensional analysis framework for pre-read reviews.

Usage:
    from mfm_agent import review_mfm, post_mfm_summary, find_mfm_file
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Tuple
import re

# Base paths
VAULT_PATH = Path(__file__).parent.parent / "Work"
MFM_PATH = VAULT_PATH / "Process" / "MFM"
FRAMEWORK_PATH = VAULT_PATH / "LLM_Context" / "MFM_review_framework.md"


def get_vault_path() -> Path:
    """Get the base vault path."""
    return VAULT_PATH


def normalize_month(month_input: str) -> str:
    """
    Normalize month input to title case folder name.

    Args:
        month_input: Month string (e.g., 'feb', 'February', 'FEB')

    Returns:
        Normalized month (e.g., 'Feb')
    """
    month_map = {
        'january': 'Jan', 'jan': 'Jan',
        'february': 'Feb', 'feb': 'Feb',
        'march': 'Mar', 'mar': 'Mar',
        'april': 'Apr', 'apr': 'Apr',
        'may': 'May',
        'june': 'Jun', 'jun': 'Jun',
        'july': 'Jul', 'jul': 'Jul',
        'august': 'Aug', 'aug': 'Aug',
        'september': 'Sep', 'sep': 'Sep', 'sept': 'Sep',
        'october': 'Oct', 'oct': 'Oct',
        'november': 'Nov', 'nov': 'Nov',
        'december': 'Dec', 'dec': 'Dec'
    }

    return month_map.get(month_input.lower(), month_input.title()[:3])


def normalize_squad_name(squad_input: str) -> str:
    """
    Normalize squad name for file searching.

    Args:
        squad_input: Squad name from user input

    Returns:
        Normalized search pattern
    """
    squad_lower = squad_input.lower().strip()

    # Known squad patterns
    squad_patterns = {
        'strategic accounts': 'strategic*accounts',
        'strategic-accounts': 'strategic*accounts',
        'first strike': 'first*strike',
        'first-strike': 'first*strike',
        'user engagement': 'user*engagement',
        'user-engagement': 'user*engagement',
        'marketing': 'marketing',
    }

    for pattern, normalized in squad_patterns.items():
        if pattern in squad_lower:
            return normalized

    # Default: replace spaces with wildcards
    return squad_lower.replace(' ', '*').replace('-', '*')


def list_available_months() -> List[str]:
    """
    List all available month folders.

    Returns:
        List of month folder names
    """
    if not MFM_PATH.exists():
        return []

    months = []
    for folder in MFM_PATH.iterdir():
        if folder.is_dir() and not folder.name.startswith('.'):
            months.append(folder.name)

    return sorted(months)


def list_files_in_month(month: str) -> List[str]:
    """
    List all MFM files in a specific month folder.

    Args:
        month: Month folder name (e.g., 'Feb')

    Returns:
        List of file names
    """
    month_path = MFM_PATH / month

    if not month_path.exists():
        return []

    files = []
    for file in month_path.glob("*.md"):
        files.append(file.name)

    return sorted(files)


def find_mfm_file(squad_name: str, month: str) -> Dict:
    """
    Find MFM pre-read file for a specific squad and month.

    Args:
        squad_name: Squad name (e.g., 'strategic accounts', 'marketing')
        month: Month (e.g., 'Feb', 'February')

    Returns:
        Dict with 'found', 'path', 'suggestions', 'error' keys
    """
    # Normalize inputs
    norm_month = normalize_month(month)
    norm_squad = normalize_squad_name(squad_name)

    month_path = MFM_PATH / norm_month

    # Check if month folder exists
    if not month_path.exists():
        available = list_available_months()
        return {
            'found': False,
            'path': None,
            'error': f"Month folder '{norm_month}' not found",
            'suggestions': available
        }

    # Search for matching files
    search_pattern = f"*{norm_squad}*mfm*.md"
    matches = list(month_path.glob(search_pattern))

    # Also try without 'mfm' requirement
    if not matches:
        search_pattern = f"*{norm_squad}*.md"
        matches = list(month_path.glob(search_pattern))

    if not matches:
        available = list_files_in_month(norm_month)
        return {
            'found': False,
            'path': None,
            'error': f"No MFM file found for '{squad_name}' in {norm_month}",
            'suggestions': available
        }

    if len(matches) == 1:
        return {
            'found': True,
            'path': str(matches[0]),
            'filename': matches[0].name
        }

    # Multiple matches - return all for disambiguation
    return {
        'found': False,
        'path': None,
        'error': f"Multiple files found for '{squad_name}' in {norm_month}",
        'suggestions': [m.name for m in matches]
    }


def load_framework() -> str:
    """
    Load the MFM review framework.

    Returns:
        Framework content or error message
    """
    if not FRAMEWORK_PATH.exists():
        return "MFM review framework not found"

    return FRAMEWORK_PATH.read_text()


def review_mfm(squad_name: str, month: str) -> Dict:
    """
    Create MFM review prep notes for a squad's pre-read.

    Args:
        squad_name: Squad name (e.g., 'strategic accounts')
        month: Month (e.g., 'Feb')

    Returns:
        Dict with review result including:
        - 'success': bool
        - 'file_found': path to pre-read file
        - 'framework_loaded': bool
        - 'output_path': path where review notes will be saved
        - 'pre_read_content': content of the pre-read document
        - 'message': status message
    """
    result = {
        'success': False,
        'squad': squad_name,
        'month': month
    }

    # Step 1: Find the MFM file
    file_result = find_mfm_file(squad_name, month)

    if not file_result['found']:
        result['error'] = file_result['error']
        result['suggestions'] = file_result.get('suggestions', [])
        return result

    result['file_found'] = file_result['path']
    result['filename'] = file_result['filename']

    # Step 2: Load framework
    framework = load_framework()
    result['framework_loaded'] = not framework.startswith("MFM review framework not found")

    # Step 3: Read pre-read content
    pre_read_path = Path(file_result['path'])
    result['pre_read_content'] = pre_read_path.read_text()

    # Step 4: Determine output path
    norm_month = normalize_month(month)
    norm_squad = normalize_squad_name(squad_name).replace('*', '_')
    output_filename = f"{norm_squad}_mfm_review.md"
    output_path = MFM_PATH / norm_month / output_filename
    result['output_path'] = str(output_path)

    # Step 5: Create stub review notes
    # Note: Full analysis is done by Claude Code using the framework
    result['success'] = True
    result['message'] = f"Ready to review {file_result['filename']} using five-dimensional framework"

    return result


def create_review_document(
    squad_name: str,
    month: str,
    analysis: Dict[str, str],
    questions: List[str],
    strengths: List[str]
) -> str:
    """
    Create the formatted review document.

    Args:
        squad_name: Squad name
        month: Month
        analysis: Dict with dimension scores and observations
        questions: List of questions to ask
        strengths: List of positive observations

    Returns:
        Formatted markdown content
    """
    today = datetime.now().strftime("%Y-%m-%d")

    content = f"""# MFM Review: {squad_name.title()} - {month}

**Generated:** {today}

## Overall Assessment

{analysis.get('overall', '[Assessment to be added]')}

## Dimensional Analysis

### 1. Examine Progress
**Score:** {analysis.get('progress_score', 'TBD')}
{analysis.get('progress_notes', '- [Observations]')}

### 2. Strategic Clarity
**Score:** {analysis.get('clarity_score', 'TBD')}
{analysis.get('clarity_notes', '- [Observations]')}

### 3. Monthly Focus
**Score:** {analysis.get('focus_score', 'TBD')}
{analysis.get('focus_notes', '- [Observations]')}

### 4. Target Confidence
**Score:** {analysis.get('confidence_score', 'TBD')}
{analysis.get('confidence_notes', '- [Observations]')}

### 5. Issue Identification
**Score:** {analysis.get('issues_score', 'TBD')}
{analysis.get('issues_notes', '- [Observations]')}

## Key Questions to Ask

"""
    for i, q in enumerate(questions, 1):
        content += f"{i}. {q}\n"

    content += "\n## Strengths to Acknowledge\n\n"
    for s in strengths:
        content += f"- {s}\n"

    content += "\n---\nGenerated by MFM Agent\n"

    return content


def post_mfm_summary(squad_name: str, month: str, meeting_data: Optional[Dict] = None) -> Dict:
    """
    Create post-MFM summary document.

    Args:
        squad_name: Squad name
        month: Month
        meeting_data: Optional dict with meeting data from Granola

    Returns:
        Dict with result including output path and status
    """
    result = {
        'success': False,
        'squad': squad_name,
        'month': month
    }

    # Normalize inputs
    norm_month = normalize_month(month)
    norm_squad = normalize_squad_name(squad_name).replace('*', '_')

    # Create output path
    month_path = MFM_PATH / norm_month
    if not month_path.exists():
        month_path.mkdir(parents=True, exist_ok=True)

    output_filename = f"{norm_squad}_mfm_summary.md"
    output_path = month_path / output_filename
    result['output_path'] = str(output_path)

    # If no meeting data, create stub for Claude Code to populate
    if not meeting_data:
        result['success'] = True
        result['message'] = "Ready for post-MFM summary. Need meeting data from Granola."
        result['needs_granola_data'] = True
        return result

    # Create summary document from meeting data
    content = create_summary_document(
        squad_name=squad_name,
        month=month,
        meeting_data=meeting_data
    )

    output_path.write_text(content)
    result['success'] = True
    result['message'] = f"Created MFM summary: {output_path}"

    return result


def create_summary_document(
    squad_name: str,
    month: str,
    meeting_data: Dict
) -> str:
    """
    Create formatted post-MFM summary document.

    Args:
        squad_name: Squad name
        month: Month
        meeting_data: Dict with meeting details

    Returns:
        Formatted markdown content
    """
    today = datetime.now().strftime("%Y-%m-%d")

    decisions = meeting_data.get('decisions', [])
    actions = meeting_data.get('actions', [])
    changes = meeting_data.get('changes', [])
    followups = meeting_data.get('followups', [])
    attendees = meeting_data.get('attendees', [])
    date = meeting_data.get('date', today)

    content = f"""# MFM Summary: {squad_name.title()} - {month}

**Date:** {date}
**Attendees:** {', '.join(attendees) if attendees else 'TBD'}

## Decisions Made

"""
    if decisions:
        for d in decisions:
            content += f"- {d}\n"
    else:
        content += "- [No decisions recorded]\n"

    content += "\n## Actions\n\n"
    if actions:
        for a in actions:
            owner = a.get('owner', 'TBD')
            action = a.get('action', a) if isinstance(a, dict) else a
            due = a.get('due', '') if isinstance(a, dict) else ''
            due_str = f" (by {due})" if due else ""
            content += f"- [ ] **{owner}**: {action}{due_str}\n"
    else:
        content += "- [ ] [No actions recorded]\n"

    content += "\n## Changes to Plan\n\n"
    if changes:
        for c in changes:
            content += f"- {c}\n"
    else:
        content += "- [No changes to plan]\n"

    content += "\n## Follow-Up Required\n\n"
    if followups:
        for f in followups:
            content += f"- {f}\n"
    else:
        content += "- [No follow-ups]\n"

    # Slack-ready summary
    content += "\n---\n**Slack-ready summary:**\n\n"
    content += f"MFM Summary - {squad_name.title()} {month}:\n"
    if decisions:
        for d in decisions[:3]:  # Top 3 decisions
            content += f"* {d}\n"
    if actions:
        for a in actions[:3]:  # Top 3 actions
            owner = a.get('owner', 'TBD') if isinstance(a, dict) else 'TBD'
            action = a.get('action', a) if isinstance(a, dict) else a
            content += f"* {owner} to {action}\n"

    content += "\n---\nGenerated by MFM Agent\n"

    return content


def extract_mfm_actions(transcript: str) -> List[Dict]:
    """
    Extract action items from MFM meeting transcript.

    This is a stub function - Claude Code should use LLM
    to extract actions from the actual transcript.

    Args:
        transcript: Meeting transcript text

    Returns:
        List of action dicts with 'owner', 'action', 'due' keys
    """
    # Stub implementation - Claude Code will provide actual extraction
    print("[MFM Agent] Action extraction requires Claude Code LLM analysis")
    return []


def search_granola_for_mfm(squad_name: str, month: str) -> Dict:
    """
    Search Granola for MFM meeting.

    This is a stub function - Claude Code should call
    mcp__granola__ tools to find the meeting.

    Args:
        squad_name: Squad name to search for
        month: Month to search in

    Returns:
        Dict with meeting info or empty if not found
    """
    # Stub implementation - Claude Code calls Granola MCP
    print(f"[MFM Agent] Searching Granola for {squad_name} MFM in {month}...")
    print("[MFM Agent] Claude Code should call mcp__granola__query_granola_meetings")

    return {
        'found': False,
        'message': "Use mcp__granola__query_granola_meetings to find meeting"
    }


# Test function
if __name__ == '__main__':
    print("MFM Agent - Test")
    print("=" * 50)

    # Test month normalization
    print("\n1. Month Normalization:")
    test_months = ['feb', 'February', 'FEB', 'Mar', 'september']
    for m in test_months:
        print(f"   '{m}' -> '{normalize_month(m)}'")

    # Test squad normalization
    print("\n2. Squad Normalization:")
    test_squads = ['strategic accounts', 'first strike', 'marketing', 'User Engagement']
    for s in test_squads:
        print(f"   '{s}' -> '{normalize_squad_name(s)}'")

    # Test available months
    print("\n3. Available Months:")
    months = list_available_months()
    print(f"   {', '.join(months) if months else 'No months found'}")

    # Test file finding
    print("\n4. File Finding (strategic accounts, Feb):")
    result = find_mfm_file('strategic accounts', 'Feb')
    if result['found']:
        print(f"   Found: {result['filename']}")
    else:
        print(f"   Not found: {result['error']}")
        if result.get('suggestions'):
            print(f"   Suggestions: {', '.join(result['suggestions'][:3])}")

    print("\n✓ Tests complete")
