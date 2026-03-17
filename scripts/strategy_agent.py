"""
Strategy Agent handler for Julie.

Handles strategy-related queries using progressive disclosure pattern:
- L1: Overview (broad questions)
- L2: Domain-specific (domain questions)
- L3: Detail (specific initiatives, bets, experiments)
"""

from pathlib import Path
import re

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
STRATEGY_MEMORY_PATH = PROJECT_ROOT / 'Work' / 'LLM_Context' / 'strategy-memory'


def classify_query(query_text):
    """
    Classify the query scope to determine which level of context to load.

    Returns:
        dict with:
            - scope: 'broad', 'domain', or 'detail'
            - domain: specific domain if detected (None otherwise)
            - detail_type: specific detail folder if detected (None otherwise)
    """
    query_lower = query_text.lower()

    # Domain keywords mapping
    domains = {
        'monetization': 'monetization-growth',
        'growth': 'monetization-growth',
        'pricing': 'monetization-growth',
        'analysis': 'analysis-platform',
        'platform': 'platform-infrastructure',
        'infrastructure': 'platform-infrastructure',
        'automation': 'automation-intelligence',
        'ai': 'automation-intelligence',
        'intelligence': 'automation-intelligence',
        'board': 'board-collaboration',
        'collaboration': 'board-collaboration',
        'building': 'building-design',
        'site': 'site-design',
        'street': 'street-design',
        'visualization': 'visualization',
        'rendering': 'visualization',
        'ecosystem': 'ecosystem-extensions',
        'extensions': 'ecosystem-extensions',
        'plugins': 'ecosystem-extensions',
        'connected': 'connected-design',
        'contextual': 'contextual-data',
        'data': 'contextual-data',
    }

    # Detail keywords
    detail_types = {
        'bet': 'bets',
        'bets': 'bets',
        'experiment': 'experiments',
        'experiments': 'experiments',
        'decision': 'decisions',
        'decisions': 'decisions',
        'objective': 'objectives',
        'objectives': 'objectives',
        'press release': 'press-releases',
        'prfaq': 'press-releases',
    }

    # Check for detail-level queries
    for keyword, detail_folder in detail_types.items():
        if keyword in query_lower:
            # Check if also domain-specific
            for domain_kw, domain_folder in domains.items():
                if domain_kw in query_lower:
                    return {
                        'scope': 'detail',
                        'domain': domain_folder,
                        'detail_type': detail_folder
                    }
            return {
                'scope': 'detail',
                'domain': None,
                'detail_type': detail_folder
            }

    # Check for domain-specific queries
    for keyword, domain_folder in domains.items():
        if keyword in query_lower:
            return {
                'scope': 'domain',
                'domain': domain_folder,
                'detail_type': None
            }

    # Default to broad
    return {
        'scope': 'broad',
        'domain': None,
        'detail_type': None
    }


def get_available_files():
    """
    Get list of available strategy files organized by level.

    Returns:
        dict with L1, L2, L3, and cross-cutting file lists
    """
    files = {
        'L1': [],
        'L2_domains': [],
        'L3_detail': {},
        'cross_cutting': []
    }

    # L1 overview
    l1_file = STRATEGY_MEMORY_PATH / 'L1-overview.md'
    if l1_file.exists():
        files['L1'].append(str(l1_file))

    # L2 domains
    l2_path = STRATEGY_MEMORY_PATH / 'L2-domains'
    if l2_path.exists():
        files['L2_domains'] = [str(f) for f in sorted(l2_path.glob('*.md'))]

    # L3 detail subfolders
    l3_path = STRATEGY_MEMORY_PATH / 'L3-detail'
    if l3_path.exists():
        for subfolder in l3_path.iterdir():
            if subfolder.is_dir():
                files['L3_detail'][subfolder.name] = [str(f) for f in sorted(subfolder.glob('*.md'))]

    # Cross-cutting
    cross_path = STRATEGY_MEMORY_PATH / 'cross-cutting'
    if cross_path.exists():
        files['cross_cutting'] = [str(f) for f in sorted(cross_path.glob('*.md'))]

    return files


def handle_strategy_query(query_text):
    """
    Handle a strategy query by providing guidance and context paths.

    Args:
        query_text: The user's strategy question

    Returns:
        dict with:
            - success: bool
            - classification: query classification
            - files_to_read: list of files to read in order
            - guidance: instructions for Claude Code
    """
    classification = classify_query(query_text)
    available = get_available_files()

    files_to_read = []
    guidance_parts = []

    # Always start with L1 for context
    if available['L1']:
        files_to_read.append(available['L1'][0])
        guidance_parts.append("1. Read L1-overview.md for strategic context")

    if classification['scope'] == 'broad':
        guidance_parts.append("2. Answer from L1 overview (broad query)")
        guidance_parts.append("3. If more detail needed, list available L2 domains")

    elif classification['scope'] == 'domain':
        domain = classification['domain']
        domain_file = STRATEGY_MEMORY_PATH / 'L2-domains' / f'{domain}.md'
        if domain_file.exists():
            files_to_read.append(str(domain_file))
            guidance_parts.append(f"2. Read L2-domains/{domain}.md for domain detail")
        else:
            # List available domains
            guidance_parts.append(f"2. Domain '{domain}' not found. Available domains:")
            for f in available['L2_domains']:
                guidance_parts.append(f"   - {Path(f).stem}")
        guidance_parts.append("3. Synthesize answer from L1 + L2 context")

    elif classification['scope'] == 'detail':
        detail_type = classification['detail_type']
        domain = classification['domain']

        # Add L3 detail folder
        if detail_type and detail_type in available['L3_detail']:
            detail_files = available['L3_detail'][detail_type]
            if domain:
                # Filter to domain-specific files if possible
                domain_files = [f for f in detail_files if domain in f.lower()]
                if domain_files:
                    files_to_read.extend(domain_files)
                    guidance_parts.append(f"2. Read domain-specific {detail_type} files")
                else:
                    files_to_read.extend(detail_files[:3])  # Limit to first 3
                    guidance_parts.append(f"2. Read {detail_type} files (no domain match)")
            else:
                files_to_read.extend(detail_files[:3])
                guidance_parts.append(f"2. Read {detail_type} files")

        guidance_parts.append("3. Synthesize answer with specific detail")

    # Build output
    result = {
        'success': True,
        'classification': classification,
        'files_to_read': files_to_read,
        'guidance': '\n'.join(guidance_parts),
        'available_structure': {
            'L1': len(available['L1']),
            'L2_domains': len(available['L2_domains']),
            'L3_folders': list(available['L3_detail'].keys()),
            'cross_cutting': len(available['cross_cutting'])
        }
    }

    return result


def format_strategy_response(query_text):
    """
    Format a strategy query response for display.

    Args:
        query_text: The user's query

    Returns:
        Formatted string response
    """
    result = handle_strategy_query(query_text)

    output = []
    output.append("=" * 60)
    output.append("STRATEGY QUERY")
    output.append("=" * 60)
    output.append(f"\nQuery: {query_text}")
    output.append(f"Classification: {result['classification']['scope']}")

    if result['classification']['domain']:
        output.append(f"Domain: {result['classification']['domain']}")
    if result['classification']['detail_type']:
        output.append(f"Detail type: {result['classification']['detail_type']}")

    output.append(f"\n**Recommended reading order:**")
    for i, f in enumerate(result['files_to_read'], 1):
        output.append(f"  {i}. {f}")

    output.append(f"\n**Workflow:**")
    output.append(result['guidance'])

    output.append(f"\n**Available structure:**")
    struct = result['available_structure']
    output.append(f"  - L1 overview: {struct['L1']} file(s)")
    output.append(f"  - L2 domains: {struct['L2_domains']} file(s)")
    output.append(f"  - L3 detail folders: {', '.join(struct['L3_folders']) or 'none'}")
    output.append(f"  - Cross-cutting: {struct['cross_cutting']} file(s)")

    output.append("\n" + "=" * 60)
    output.append("Read the files above to answer the query.")
    output.append("Follow progressive disclosure: start with L1, expand as needed.")
    output.append("=" * 60)

    return '\n'.join(output)


# Test
if __name__ == '__main__':
    test_queries = [
        "What are our strategic priorities?",
        "What's the monetization strategy?",
        "What bets are we making?",
        "What experiments are running for connected-clients?",
        "What are the current OKRs?",
    ]

    for q in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {q}")
        result = handle_strategy_query(q)
        print(f"Scope: {result['classification']['scope']}")
        print(f"Files: {result['files_to_read']}")
        print(f"Guidance:\n{result['guidance']}")
