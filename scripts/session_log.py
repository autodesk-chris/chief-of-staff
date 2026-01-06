#!/usr/bin/env python3
"""
Session Logging System

Manages logging of Claude work sessions to daily log files.
Supports multiple sessions per day with timestamps.
"""

from datetime import datetime
from pathlib import Path
from utils import get_vault_path


def log_session(summary_text):
    """
    Append session summary to today's log file.

    Args:
        summary_text: User-provided summary of what was worked on (can be multiline)

    Returns:
        Path to the log file

    Example:
        log_session("- Designed daily summary feature\\n- Fixed bug in status updates")
    """
    date = datetime.now().date()
    time = datetime.now().strftime("%H:%M")

    # Ensure Daily_Logs directory exists
    log_dir = Path(get_vault_path()) / "Daily_Logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"claude_sessions_{date.strftime('%Y-%m-%d')}.md"

    # Create file with header if doesn't exist
    if not log_file.exists():
        header = f"# Claude Sessions - {date.strftime('%B %d, %Y')}\n\n"
        log_file.write_text(header, encoding='utf-8')

    # Count existing sessions to number this one
    content = log_file.read_text(encoding='utf-8')
    session_count = content.count("## Session") + 1

    # Format summary text - ensure it starts with bullets if not already
    formatted_summary = format_summary_text(summary_text)

    # Append new session
    entry = f"## Session {session_count} ({time})\n{formatted_summary}\n\n"

    with log_file.open('a', encoding='utf-8') as f:
        f.write(entry)

    return log_file


def read_session_log(date):
    """
    Read all session entries for a given date.

    Args:
        date: datetime.date object for the day to read

    Returns:
        String containing full log file content, or None if file doesn't exist

    Example:
        today = datetime.now().date()
        sessions = read_session_log(today)
    """
    log_file = Path(get_vault_path()) / "Daily_Logs" / f"claude_sessions_{date.strftime('%Y-%m-%d')}.md"

    if not log_file.exists():
        return None

    return log_file.read_text(encoding='utf-8')


def parse_session_log(log_content):
    """
    Parse session log content into structured data.

    Args:
        log_content: String content of session log file

    Returns:
        List of dicts with session data: [{'time': '09:30', 'summary': '...'}]
    """
    if not log_content:
        return []

    sessions = []
    lines = log_content.split('\n')
    current_session = None

    for line in lines:
        # Detect session headers: ## Session 1 (09:30)
        if line.startswith('## Session'):
            if current_session:
                # Save previous session
                sessions.append(current_session)

            # Extract time from header
            time_start = line.find('(')
            time_end = line.find(')')
            time = line[time_start+1:time_end] if time_start != -1 else 'Unknown'

            current_session = {
                'time': time,
                'summary': []
            }
        elif current_session and line.strip():
            # Skip the main header
            if not line.startswith('# Claude Sessions'):
                current_session['summary'].append(line)

    # Don't forget the last session
    if current_session:
        sessions.append(current_session)

    # Join summary lines
    for session in sessions:
        session['summary'] = '\n'.join(session['summary'])

    return sessions


def format_summary_text(text):
    """
    Format summary text to ensure consistent bullet-point format.

    Args:
        text: Raw user input (may or may not have bullets)

    Returns:
        Formatted text with bullet points
    """
    if not text:
        return "- (No details provided)"

    lines = text.strip().split('\n')
    formatted_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # If line already starts with bullet, keep it
        if line.startswith('- ') or line.startswith('* '):
            formatted_lines.append(line)
        # If line starts with number, convert to bullet
        elif line[0].isdigit() and '. ' in line:
            # Remove number prefix
            formatted_lines.append('- ' + line.split('. ', 1)[1])
        # Otherwise, add bullet
        else:
            formatted_lines.append('- ' + line)

    return '\n'.join(formatted_lines)


if __name__ == '__main__':
    # Test the session logging
    import sys

    if len(sys.argv) < 2:
        print("Usage: python session_log.py 'Your session summary here'")
        print("Example: python session_log.py 'Worked on daily summary feature'")
        sys.exit(1)

    summary = sys.argv[1]
    log_file = log_session(summary)
    print(f"✓ Session logged to: {log_file}")

    # Read and display current sessions
    today = datetime.now().date()
    content = read_session_log(today)
    if content:
        print(f"\nToday's sessions:")
        print(content)
