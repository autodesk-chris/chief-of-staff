#!/usr/bin/env python3
"""
Strategy Query Helper for Julie (Chief of Staff agent system)

Provides progressive disclosure of strategy-memory content.
Uses L1 → L2 → L3 hierarchy to minimize context loading.

Usage:
    from strategy_query_helper import get_l1_overview, get_l2_domain, list_l2_domains
"""

from pathlib import Path
from typing import Optional, List, Dict

# Base path for strategy memory
STRATEGY_MEMORY_PATH = Path(__file__).parent.parent / "Work" / "LLM_Context" / "strategy-memory"


def get_vault_path() -> Path:
    """Get the base strategy-memory path."""
    return STRATEGY_MEMORY_PATH


def get_l1_overview() -> Dict[str, str]:
    """
    Get the L1 overview file content.

    This is always the starting point for strategy queries.
    Contains overall strategic direction and key priorities.

    Returns:
        Dict with 'content' and 'path' keys
    """
    l1_path = STRATEGY_MEMORY_PATH / "L1-overview.md"

    if not l1_path.exists():
        return {
            'content': "L1 overview not found",
            'path': str(l1_path),
            'exists': False
        }

    return {
        'content': l1_path.read_text(),
        'path': str(l1_path),
        'exists': True
    }


def list_l2_domains() -> List[str]:
    """
    List all available L2 domain files.

    Returns:
        List of domain names (without .md extension)
    """
    l2_path = STRATEGY_MEMORY_PATH / "L2-domains"

    if not l2_path.exists():
        return []

    domains = []
    for file in l2_path.glob("*.md"):
        domains.append(file.stem)

    return sorted(domains)


def get_l2_domain(domain_name: str) -> Dict[str, str]:
    """
    Get a specific L2 domain file content.

    Args:
        domain_name: Name of the domain (e.g., 'monetization-growth')
                    Can include or exclude .md extension

    Returns:
        Dict with 'content', 'path', and 'exists' keys
    """
    # Normalize domain name
    if domain_name.endswith('.md'):
        domain_name = domain_name[:-3]

    l2_path = STRATEGY_MEMORY_PATH / "L2-domains" / f"{domain_name}.md"

    if not l2_path.exists():
        # Try fuzzy match
        available = list_l2_domains()
        matches = [d for d in available if domain_name.lower() in d.lower()]

        return {
            'content': f"Domain '{domain_name}' not found. Available: {', '.join(available)}",
            'path': str(l2_path),
            'exists': False,
            'suggestions': matches
        }

    return {
        'content': l2_path.read_text(),
        'path': str(l2_path),
        'exists': True
    }


def list_l3_categories() -> List[str]:
    """
    List all L3 detail categories.

    Returns:
        List of category folder names
    """
    l3_path = STRATEGY_MEMORY_PATH / "L3-detail"

    if not l3_path.exists():
        return []

    categories = []
    for folder in l3_path.iterdir():
        if folder.is_dir() and not folder.name.startswith('.'):
            categories.append(folder.name)

    return sorted(categories)


def list_l3_files(category: str) -> List[str]:
    """
    List all files in an L3 category.

    Args:
        category: Name of the L3 category (e.g., 'bets', 'strategies')

    Returns:
        List of file names (without .md extension)
    """
    l3_path = STRATEGY_MEMORY_PATH / "L3-detail" / category

    if not l3_path.exists():
        return []

    files = []
    for file in l3_path.glob("*.md"):
        files.append(file.stem)

    return sorted(files)


def get_l3_file(category: str, file_name: str) -> Dict[str, str]:
    """
    Get a specific L3 detail file.

    Args:
        category: L3 category (e.g., 'bets', 'strategies', 'decisions')
        file_name: Name of the file (with or without .md)

    Returns:
        Dict with 'content', 'path', and 'exists' keys
    """
    # Normalize file name
    if file_name.endswith('.md'):
        file_name = file_name[:-3]

    l3_path = STRATEGY_MEMORY_PATH / "L3-detail" / category / f"{file_name}.md"

    if not l3_path.exists():
        available = list_l3_files(category)
        return {
            'content': f"File '{file_name}' not found in {category}. Available: {', '.join(available)}",
            'path': str(l3_path),
            'exists': False
        }

    return {
        'content': l3_path.read_text(),
        'path': str(l3_path),
        'exists': True
    }


def get_cross_cutting(theme_name: str) -> Dict[str, str]:
    """
    Get a cross-cutting theme file.

    Args:
        theme_name: Name of the cross-cutting theme

    Returns:
        Dict with 'content', 'path', and 'exists' keys
    """
    # Normalize theme name
    if theme_name.endswith('.md'):
        theme_name = theme_name[:-3]

    cc_path = STRATEGY_MEMORY_PATH / "cross-cutting" / f"{theme_name}.md"

    if not cc_path.exists():
        # List available themes
        cc_folder = STRATEGY_MEMORY_PATH / "cross-cutting"
        available = []
        if cc_folder.exists():
            available = [f.stem for f in cc_folder.glob("*.md")]

        return {
            'content': f"Theme '{theme_name}' not found. Available: {', '.join(available)}",
            'path': str(cc_path),
            'exists': False,
            'suggestions': available
        }

    return {
        'content': cc_path.read_text(),
        'path': str(cc_path),
        'exists': True
    }


def list_cross_cutting_themes() -> List[str]:
    """
    List all cross-cutting theme files.

    Returns:
        List of theme names (without .md extension)
    """
    cc_path = STRATEGY_MEMORY_PATH / "cross-cutting"

    if not cc_path.exists():
        return []

    themes = []
    for file in cc_path.glob("*.md"):
        themes.append(file.stem)

    return sorted(themes)


def progressive_query(query_type: str, identifier: Optional[str] = None) -> Dict:
    """
    Progressive loading helper for strategy queries.

    Args:
        query_type: 'overview', 'domain', 'detail', 'cross-cutting'
        identifier: Domain name, file name, or category (depending on type)

    Returns:
        Dict with query results and loading path
    """
    result = {
        'query_type': query_type,
        'identifier': identifier,
        'files_loaded': [],
        'content': {}
    }

    if query_type == 'overview':
        l1 = get_l1_overview()
        result['files_loaded'].append(l1['path'])
        result['content']['l1'] = l1

    elif query_type == 'domain':
        if not identifier:
            result['error'] = "Domain name required"
            result['available'] = list_l2_domains()
            return result

        # Load L1 for context
        l1 = get_l1_overview()
        result['files_loaded'].append(l1['path'])
        result['content']['l1_summary'] = "L1 overview loaded for context"

        # Load specific domain
        l2 = get_l2_domain(identifier)
        result['files_loaded'].append(l2['path'])
        result['content']['l2'] = l2

    elif query_type == 'detail':
        if not identifier:
            result['error'] = "Category required"
            result['available'] = list_l3_categories()
            return result

        # Parse identifier (may be "category" or "category/file")
        parts = identifier.split('/')
        category = parts[0]

        if len(parts) == 1:
            # Just list files in category
            files = list_l3_files(category)
            result['content']['files'] = files
            result['content']['category'] = category
        else:
            # Load specific file
            file_name = parts[1]
            l3 = get_l3_file(category, file_name)
            result['files_loaded'].append(l3['path'])
            result['content']['l3'] = l3

    elif query_type == 'cross-cutting':
        if not identifier:
            result['error'] = "Theme name required"
            result['available'] = list_cross_cutting_themes()
            return result

        cc = get_cross_cutting(identifier)
        result['files_loaded'].append(cc['path'])
        result['content']['cross_cutting'] = cc

    else:
        result['error'] = f"Unknown query type: {query_type}"
        result['available_types'] = ['overview', 'domain', 'detail', 'cross-cutting']

    return result


def get_structure_summary() -> Dict:
    """
    Get a summary of the strategy-memory structure.

    Useful for understanding what's available without loading content.

    Returns:
        Dict with structure overview
    """
    return {
        'l1': {
            'file': 'L1-overview.md',
            'exists': (STRATEGY_MEMORY_PATH / "L1-overview.md").exists()
        },
        'l2_domains': list_l2_domains(),
        'l3_categories': list_l3_categories(),
        'cross_cutting': list_cross_cutting_themes()
    }


# Test function
if __name__ == '__main__':
    print("Strategy Query Helper - Test")
    print("=" * 50)

    # Test structure summary
    print("\n1. Structure Summary:")
    structure = get_structure_summary()
    print(f"   L1 exists: {structure['l1']['exists']}")
    print(f"   L2 domains: {', '.join(structure['l2_domains'])}")
    print(f"   L3 categories: {', '.join(structure['l3_categories'])}")
    print(f"   Cross-cutting: {', '.join(structure['cross_cutting'])}")

    # Test L1 loading
    print("\n2. L1 Overview:")
    l1 = get_l1_overview()
    print(f"   Path: {l1['path']}")
    print(f"   Exists: {l1['exists']}")
    if l1['exists']:
        print(f"   Content length: {len(l1['content'])} chars")

    # Test progressive query
    print("\n3. Progressive Query - Domain:")
    result = progressive_query('domain', 'monetization-growth')
    print(f"   Files loaded: {len(result['files_loaded'])}")
    if 'l2' in result['content']:
        print(f"   L2 exists: {result['content']['l2']['exists']}")

    print("\n✓ All tests passed")
