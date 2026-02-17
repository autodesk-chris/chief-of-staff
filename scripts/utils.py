"""
Utility functions for the Personal OS command system.
"""

import re
from datetime import datetime
from pathlib import Path
from difflib import SequenceMatcher


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
    Get the path to the appropriate folder for the item type.

    Args:
        item_type: Type of item ('task', 'idea', 'feature', 'action', 'reminder', 'decision')

    Returns:
        Path object to the appropriate subfolder
    """
    vault_path = get_vault_path()

    # Map item types to their folder paths (relative to vault)
    if item_type in ['task', 'idea', 'feature', 'action', 'reminder']:
        folder_map = {
            'task': 'Tasks',
            'idea': 'Ideas',
            'feature': 'Features',
            'action': 'Actions',
            'reminder': 'Reminders'
        }
        folder_name = folder_map.get(item_type)
        if not folder_name:
            raise ValueError(f"Invalid item type: {item_type}")
        return vault_path / "Inbox" / folder_name
    elif item_type == 'decision':
        return vault_path / "Decisions"
    else:
        raise ValueError(f"Invalid item type: {item_type}")


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


def get_360_reviews_path():
    """
    Get the path to the Team/360_reviews folder.

    Returns:
        Path object pointing to Work/Team/360_reviews
    """
    return get_team_path() / "360_reviews"


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


def extract_title_from_file(file_path):
    """
    Extract the title from a markdown file's H1 heading.

    Args:
        file_path: Path to the markdown file

    Returns:
        Title string or None if not found
    """
    try:
        content = file_path.read_text()
        # Look for the first # heading after frontmatter
        lines = content.split('\n')
        in_frontmatter = False

        for line in lines:
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue

            if not in_frontmatter and line.startswith('#'):
                # Extract title text (e.g., "# Task: Title" -> "Title")
                title = line.lstrip('#').strip()
                # Remove type prefix if present (e.g., "Task: " or "Idea: ")
                if ':' in title:
                    title = title.split(':', 1)[1].strip()
                return title

        return None
    except Exception:
        return None


def similarity_ratio(a, b):
    """
    Calculate similarity ratio between two strings.

    Args:
        a: First string
        b: Second string

    Returns:
        Float between 0 and 1 (1 = exact match)
    """
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_item_by_title(search_title, threshold=0.6):
    """
    Find items across all folders by title using fuzzy matching.

    Args:
        search_title: The title to search for
        threshold: Minimum similarity ratio (0-1) for matches (default 0.6)

    Returns:
        List of tuples: (item_type, file_path, title, similarity_score)
        Sorted by similarity score (highest first)
    """
    vault_path = get_vault_path()
    inbox_path = vault_path / "Inbox"

    matches = []
    item_types = {
        'Tasks': 'task',
        'Ideas': 'idea',
        'Features': 'feature',
        'Actions': 'action'
    }

    for folder_name, item_type in item_types.items():
        folder_path = inbox_path / folder_name
        if not folder_path.exists():
            continue

        for file_path in folder_path.glob('*.md'):
            # Skip summary files
            if file_path.name.startswith('today_') or file_path.name.startswith('weekly_'):
                continue

            # Extract title from file
            file_title = extract_title_from_file(file_path)
            if not file_title:
                continue

            # Calculate similarity
            score = similarity_ratio(search_title, file_title)

            # Also check similarity with filename (without prefix and extension)
            filename_base = file_path.stem.replace(f'{item_type}_', '', 1).replace('_', ' ')
            filename_score = similarity_ratio(search_title, filename_base)

            # Use the better score
            best_score = max(score, filename_score)

            if best_score >= threshold:
                matches.append((item_type, file_path, file_title, best_score))

    # Sort by similarity score (highest first)
    matches.sort(key=lambda x: x[3], reverse=True)

    return matches
