"""
Utility functions for the Personal OS command system.
"""

import re
from datetime import datetime
from pathlib import Path


def sanitize_filename(title):
    """
    Convert a title to a safe filename by replacing spaces with underscores
    and removing special characters.

    Args:
        title: The original title string

    Returns:
        A sanitized filename string
    """
    # Replace spaces with underscores
    filename = title.replace(' ', '_')

    # Remove special characters, keep only alphanumeric, hyphens, and underscores
    filename = re.sub(r'[^a-zA-Z0-9_-]', '', filename)

    return filename


def parse_tags(tags_string):
    """
    Parse comma-separated tags string into a list.

    Args:
        tags_string: Comma-separated tags (e.g., "work, urgent, project")

    Returns:
        List of cleaned tag strings
    """
    if not tags_string or tags_string.strip() == '':
        return []

    # Split by comma and strip whitespace
    tags = [tag.strip() for tag in tags_string.split(',')]

    # Remove empty tags
    tags = [tag for tag in tags if tag]

    return tags


def format_tags_yaml(tags):
    """
    Format tags list as YAML array format.

    Args:
        tags: List of tag strings

    Returns:
        YAML formatted string (e.g., "[tag1, tag2]")
    """
    if not tags:
        return "[]"

    return f"[{', '.join(tags)}]"


def validate_date(date_string):
    """
    Validate that a date string is in YYYY-MM-DD format.

    Args:
        date_string: Date string to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


def get_vault_path():
    """
    Get the path to the Obsidian vault.

    Returns:
        Path object pointing to the Work vault
    """
    # Get the project root (parent of scripts folder)
    project_root = Path(__file__).parent.parent
    vault_path = project_root / "Work"

    return vault_path


def get_inbox_path(item_type):
    """
    Get the path to the appropriate Inbox subfolder.

    Args:
        item_type: Type of item ('task', 'idea', 'feature', or 'action')

    Returns:
        Path object to the appropriate subfolder
    """
    vault_path = get_vault_path()

    folder_map = {
        'task': 'Tasks',
        'idea': 'Ideas',
        'feature': 'Features',
        'action': 'Actions'
    }

    folder_name = folder_map.get(item_type)
    if not folder_name:
        raise ValueError(f"Invalid item type: {item_type}")

    return vault_path / "Inbox" / folder_name


def get_team_path():
    """
    Get the path to the Team folder.

    Returns:
        Path object pointing to Work/Team
    """
    vault_path = get_vault_path()
    return vault_path / "Team"


def get_observations_path():
    """
    Get the path to the Team/Observations folder.

    Returns:
        Path object pointing to Work/Team/Observations
    """
    return get_team_path() / "Observations"


def extract_team_member_name(title):
    """
    Extract team member name from observation title.

    Expects format: "Name - observation text"

    Args:
        title: The observation title

    Returns:
        Tuple of (name, observation) or (None, title) if no dash found
    """
    if " - " not in title:
        return None, title

    parts = title.split(" - ", 1)
    name = parts[0].strip()
    observation = parts[1].strip() if len(parts) > 1 else title

    return name, observation
