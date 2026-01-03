#!/usr/bin/env python3
"""
Create observations about team members.

Usage:
    python create_observation.py "Sarah - Great presentation" --details "Excellent communication skills" --tags "leadership"
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import utils
sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    sanitize_filename,
    parse_tags,
    format_tags_yaml,
    get_observations_path,
    extract_team_member_name
)


def create_observation_frontmatter(team_member, date, tags=None):
    """
    Generate YAML frontmatter for observation file.

    Args:
        team_member: Team member name
        date: Date string (YYYY-MM-DD)
        tags: List of tag strings or None

    Returns:
        Formatted frontmatter string
    """
    tags_formatted = format_tags_yaml(tags) if tags else "[]"

    frontmatter = f"""---
type: observation
team-member: {team_member}
date: {date}
tags: {tags_formatted}
---"""

    return frontmatter


def create_observation_content(team_member, date, details):
    """
    Generate the main content for the observation file.

    Args:
        team_member: Team member name
        date: Date string (YYYY-MM-DD)
        details: Observation details

    Returns:
        Formatted content string
    """
    content = f"""
# Observation: {team_member} - {date}

## Details

{details}
"""

    return content


def create_observation(title, details="", tags=None):
    """
    Create a new observation file in Team/Observations/.

    Args:
        title: Observation title (format: "Name - observation")
        details: Detailed observation
        tags: List of tag strings

    Returns:
        Path to the created file
    """
    # Extract team member name from title
    team_member, observation_text = extract_team_member_name(title)

    if not team_member:
        raise ValueError(
            "Team member name is required. "
            "Please use format: 'Name - observation text' "
            "(e.g., 'Sarah Johnson - Great presentation')"
        )

    # Get current date
    today = datetime.now().strftime('%Y-%m-%d')

    # Create filename: observation_<name>_<date>.md
    safe_name = sanitize_filename(team_member)
    filename = f"observation_{safe_name}_{today}.md"

    # Get observations folder path
    observations_path = get_observations_path()
    file_path = observations_path / filename

    # If file already exists (same person, same day), append timestamp
    if file_path.exists():
        timestamp = datetime.now().strftime('%H%M%S')
        filename = f"observation_{safe_name}_{today}_{timestamp}.md"
        file_path = observations_path / filename

    # Use observation text from title if no details provided
    if not details:
        details = observation_text

    # Generate frontmatter and content
    frontmatter = create_observation_frontmatter(team_member, today, tags)
    content = create_observation_content(team_member, today, details)

    # Combine and write to file
    full_content = frontmatter + content

    file_path.write_text(full_content)

    return file_path
