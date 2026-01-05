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
    get_360_reviews_path,
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


def create_360_review(team_member):
    """
    Create or get 360 review file for team member.

    Args:
        team_member: Team member name

    Returns:
        Tuple of (file_path, is_new) where is_new indicates if file was created
    """
    if not team_member or not team_member.strip():
        raise ValueError(
            "Team member name is required for 360 review. "
            "Please use format: '360 review: Name' "
            "(e.g., '360 review: Sarah Johnson')"
        )

    team_member = team_member.strip()

    # Get 360 reviews folder path
    reviews_path = get_360_reviews_path()

    # Create filename: 360_<name>_FY26.md
    safe_name = sanitize_filename(team_member)
    filename = f"360_{safe_name}_FY26.md"
    file_path = reviews_path / filename

    # Check if file already exists
    if file_path.exists():
        return file_path, False

    # Create new 360 review file with template
    today = datetime.now().strftime('%Y-%m-%d')

    content = f"""---
type: 360-review
team-member: {team_member}
fiscal-year: FY26
created: {today}
status: in-progress
---

# 360 Review: {team_member} - FY26

## Overview

Performance review and 360 feedback for {team_member}.

## Reference

See [[performance_assessment_guide]] for evaluation criteria.

## Key Observations

<!-- Link to observation files here -->

## Strengths

<!-- Document key strengths -->

## Areas for Growth

<!-- Document development opportunities -->

## Goals & Commitments

<!-- Document goals and commitments -->

## Summary

<!-- Final assessment summary -->
"""

    file_path.write_text(content)
    return file_path, True
