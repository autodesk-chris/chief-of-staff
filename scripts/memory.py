#!/usr/bin/env python3
"""
Memory Utilities for Julie Agent System

Provides helper functions for working with claude-mem integration.

NOTE: These helpers format data and manage Obsidian sync. Actual MCP tool calls
(search, save_memory, get_observations) happen at the Claude Code level, not in Python.

Usage:
    from memory import format_memory_request, sync_memory_to_obsidian, should_query_memory

    # Format a memory storage request
    request = format_memory_request('tasks', 'Created budget review task', {'type': 'task'})
    # (Claude Code then calls mcp__plugin_claude-mem_mcp-search__save_memory with this data)

    # Check if memory query would be helpful
    if should_query_memory('Review Q2 budget'):
        # (Claude Code calls mcp__plugin_claude-mem_mcp-search__search)
        pass

    # Sync results to Obsidian
    sync_memory_to_obsidian('tasks', memory_results)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_vault_path() -> Path:
    """Get the Obsidian vault path."""
    return Path(__file__).parent.parent / "Work"


def get_memory_path(domain: str) -> Path:
    """
    Get the memory folder path for a specific domain.

    Args:
        domain: Memory domain (tasks, people, strategy, reflection, meetings)

    Returns:
        Path to domain memory folder
    """
    vault = get_vault_path()
    memory_path = vault / "Memory" / domain
    memory_path.mkdir(parents=True, exist_ok=True)
    return memory_path


def format_memory_request(
    domain: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
    title: Optional[str] = None
) -> Dict[str, Any]:
    """
    Format a memory storage request for claude-mem.

    NOTE: This prepares the data. Claude Code must call the actual MCP tool:
    mcp__plugin_claude-mem_mcp-search__save_memory(params)

    Args:
        domain: Memory domain (tasks, people, strategy, reflection, meetings)
        content: Memory content/narrative
        metadata: Optional metadata (type, tags, related items, etc.)
        title: Optional title

    Returns:
        Parameters dictionary ready for save_memory MCP tool

    Example:
        params = format_memory_request(
            'tasks',
            'Created budget review task for Q2 planning',
            {'type': 'task', 'tags': ['finance', 'planning']},
            title='Budget Review Task'
        )
        # Claude Code then calls: mcp__plugin_claude-mem_mcp-search__save_memory(params)
    """
    # Prepare text with domain context
    text = f"[{domain}] {content}"

    # Add metadata to text if provided
    if metadata:
        metadata_str = json.dumps(metadata, indent=2)
        text = f"{text}\n\nMetadata:\n{metadata_str}"

    params = {
        'text': text,
        'project': 'Chief_of_staff'
    }

    if title:
        params['title'] = title

    return params


def format_search_query(
    domain: str,
    query: str,
    limit: int = 5
) -> Dict[str, Any]:
    """
    Format a memory search request for claude-mem.

    NOTE: Claude Code must call the actual MCP tool:
    mcp__plugin_claude-mem_mcp-search__search(params)

    Args:
        domain: Memory domain (tasks, people, strategy, reflection, meetings)
        query: Search query
        limit: Maximum results

    Returns:
        Parameters dictionary ready for search MCP tool
    """
    return {
        'query': f"{domain} {query}",
        'limit': limit,
        'project': 'Chief_of_staff'
    }


def should_query_memory(task_title: str, task_type: str = 'task') -> bool:
    """
    Determine if memory query would be helpful for a task.

    Args:
        task_title: Title of the task/item being created
        task_type: Type of item (task, idea, feature)

    Returns:
        True if memory query is recommended
    """
    # Query memory for non-trivial items
    min_words = 2
    words = task_title.split()

    # Skip very short titles
    if len(words) < min_words:
        return False

    # Always query for ideas and features (higher value in finding duplicates)
    if task_type in ['idea', 'feature']:
        return True

    # Query for tasks with specific keywords
    keywords = ['review', 'analyze', 'plan', 'create', 'update', 'implement', 'design']
    if any(keyword in task_title.lower() for keyword in keywords):
        return True

    return False


def sync_memory_to_obsidian(
    domain: str,
    memories: List[Dict[str, Any]],
    append: bool = True
) -> Optional[Path]:
    """
    Sync memories to Obsidian for human-readable access.

    Creates/updates a markdown file in Work/Memory/{domain}/.

    Args:
        domain: Memory domain (tasks, people, strategy, reflection, meetings)
        memories: List of memory records from MCP search results
        append: If True, append to existing file. If False, overwrite.

    Returns:
        Path to created/updated markdown file, or None if no memories

    Example:
        # After Claude Code calls mcp__plugin_claude-mem_mcp-search__search:
        sync_memory_to_obsidian('tasks', search_results)
    """
    if not memories:
        logger.warning(f"No memories to sync for domain '{domain}'")
        return None

    memory_path = get_memory_path(domain)
    timestamp = datetime.now().strftime('%Y-%m-%d')
    filepath = memory_path / f"memory_{timestamp}.md"

    try:
        existing_content = ""
        if append and filepath.exists():
            existing_content = filepath.read_text()

        # Build new content
        content = ""
        if not existing_content:
            content = f"# Memory Log - {domain.title()}\n"
            content += f"**Date:** {timestamp}\n"
            content += f"**Domain:** {domain}\n\n"
            content += "---\n\n"

        # Add timestamp for this sync
        content += f"\n## Sync - {datetime.now().strftime('%H:%M:%S')}\n\n"

        for i, memory in enumerate(memories, 1):
            title = memory.get('title', f"Memory {i}")
            text = memory.get('text', memory.get('narrative', ''))

            content += f"### {title}\n\n"
            content += f"{text}\n\n"
            content += "---\n\n"

        # Write to file
        final_content = existing_content + content if append else content
        filepath.write_text(final_content)

        logger.info(f"Synced {len(memories)} memories to {filepath}")
        return filepath

    except Exception as e:
        logger.error(f"Failed to sync to Obsidian: {e}")
        return None


def extract_related_titles(search_results: List[Dict[str, Any]], limit: int = 3) -> List[str]:
    """
    Extract titles from search results for display.

    Args:
        search_results: Results from MCP search tool
        limit: Maximum titles to extract

    Returns:
        List of title strings
    """
    titles = []
    for result in search_results[:limit]:
        title = result.get('title', 'Untitled')
        titles.append(title)
    return titles


def log_memory_action(domain: str, action: str, details: str):
    """
    Log memory-related actions for debugging.

    Args:
        domain: Memory domain
        action: Action type (store, query, sync)
        details: Action details
    """
    logger.info(f"[{domain}] {action}: {details}")


# Test function
if __name__ == '__main__':
    print("Testing memory utilities...")
    print("Note: These are helper functions. Actual MCP calls happen in Claude Code.\n")

    # Test 1: Format memory request
    print("1. Testing format_memory_request()...")
    params = format_memory_request(
        'tasks',
        'Test memory for budget planning task',
        {'type': 'task', 'tags': ['finance', 'planning']},
        title='Budget Planning Test'
    )
    print(f"✓ Formatted request: {json.dumps(params, indent=2)}")

    # Test 2: Format search query
    print("\n2. Testing format_search_query()...")
    search_params = format_search_query('tasks', 'budget planning', limit=5)
    print(f"✓ Formatted query: {json.dumps(search_params, indent=2)}")

    # Test 3: Should query memory
    print("\n3. Testing should_query_memory()...")
    test_cases = [
        ("Review Q2 budget", "task"),
        ("Fix bug", "task"),
        ("Add dark mode", "feature"),
        ("Hi", "task")
    ]
    for title, task_type in test_cases:
        should_query = should_query_memory(title, task_type)
        print(f"  - '{title}' ({task_type}): {'Query' if should_query else 'Skip'}")

    # Test 4: Sync to Obsidian
    print("\n4. Testing sync_memory_to_obsidian()...")
    test_memories = [
        {'title': 'Test Memory 1', 'text': 'This is a test memory'},
        {'title': 'Test Memory 2', 'text': 'Another test memory'}
    ]
    filepath = sync_memory_to_obsidian('tasks', test_memories, append=False)
    if filepath:
        print(f"✓ Synced to: {filepath}")
        print(f"  Content preview: {filepath.read_text()[:100]}...")
    else:
        print("✗ Sync failed")

    print("\n✓ Memory utilities test complete")
    print("\nNext: Integrate these helpers with Tasks Agent in create_item.py")
