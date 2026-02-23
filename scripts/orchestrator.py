#!/usr/bin/env python3
"""
Orchestrator for Julie Agent System

Coordinates multi-domain queries that need context from multiple specialized agents.
Handles cross-agent context gathering for complex workflows like:
- 121 prep (observations + past meetings + actions + memory)
- MFM review (strategy + OKRs + pre-read)
- Daily summary (tasks + observations + meetings + sessions)

Usage:
    from orchestrator import orchestrate_121_prep, orchestrate_mfm_review

Integration:
    Called by parse_command.py for commands that need cross-domain context.
    Claude Code uses the gathered context to generate comprehensive outputs.
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils import get_vault_path, similarity_ratio


def get_observations_path() -> Path:
    """Get the observations folder path."""
    return get_vault_path() / "People" / "Observations"


def get_people_path() -> Path:
    """Get the people folder path."""
    return get_vault_path() / "People"


def gather_observations(person_name: str, days: int = 90) -> List[Dict[str, Any]]:
    """
    Gather observations about a person from People Agent domain.

    Args:
        person_name: Name of the person
        days: How many days back to search (default 90)

    Returns:
        List of observation dicts with date, content, file
    """
    observations = []
    cutoff_date = datetime.now() - timedelta(days=days)

    # Search in People/Observations/
    obs_path = get_observations_path()
    if obs_path.exists():
        observations.extend(_search_observations_folder(obs_path, person_name, cutoff_date))

    # Also search in Team/Observations/ (legacy location)
    team_obs_path = get_vault_path() / "Team" / "Observations"
    if team_obs_path.exists():
        observations.extend(_search_observations_folder(team_obs_path, person_name, cutoff_date))

    # Sort by date descending and return top 10
    observations.sort(key=lambda x: x['date'], reverse=True)
    return observations[:10]


def _search_observations_folder(folder: Path, person_name: str, cutoff_date: datetime) -> List[Dict]:
    """Search a folder for observations about a person."""
    results = []
    name_lower = person_name.lower().replace(' ', '_')

    for obs_file in folder.glob("observation_*.md"):
        try:
            filename_lower = obs_file.name.lower()

            # Check if filename contains person's name
            if name_lower in filename_lower or person_name.lower() in filename_lower:
                # Extract date from filename
                parts = obs_file.stem.split('_')
                if len(parts) >= 3:
                    date_str = parts[-1]
                    try:
                        obs_date = datetime.strptime(date_str, "%Y-%m-%d")
                        if obs_date >= cutoff_date:
                            content = obs_file.read_text()
                            results.append({
                                'date': date_str,
                                'file': str(obs_file),
                                'content': content[:500],
                                'source': 'observations'
                            })
                    except ValueError:
                        pass
        except Exception as e:
            print(f"Warning: Could not read {obs_file}: {e}")

    return results


def gather_past_121s(person_name: str, days: int = 180) -> List[Dict[str, Any]]:
    """
    Gather past 121 meeting notes for a person.

    Args:
        person_name: Name of the person
        days: How many days back to search (default 180)

    Returns:
        List of meeting dicts with date, summary, file
    """
    meetings = []
    cutoff_date = datetime.now() - timedelta(days=days)
    name_lower = person_name.lower().replace(' ', '_')

    # Search in People/121s/[name]/
    person_121_path = get_people_path() / "121s" / name_lower
    if person_121_path.exists():
        for meeting_file in person_121_path.glob("*.md"):
            try:
                # Extract date from filename
                date_str = meeting_file.name[:10]
                meeting_date = datetime.strptime(date_str, "%Y-%m-%d")

                if meeting_date >= cutoff_date:
                    content = meeting_file.read_text()
                    meetings.append({
                        'date': date_str,
                        'title': meeting_file.stem,
                        'file': str(meeting_file),
                        'summary': content[:400],
                        'source': 'past_121s'
                    })
            except (ValueError, Exception):
                pass

    # Also search in Meetings/ folder
    meetings_path = get_vault_path() / "Meetings"
    if meetings_path.exists():
        for meeting_file in meetings_path.glob("*.md"):
            try:
                filename_lower = meeting_file.name.lower()

                # Check if meeting involves this person
                if name_lower in filename_lower or person_name.lower() in filename_lower:
                    date_str = meeting_file.name[:10]
                    meeting_date = datetime.strptime(date_str, "%Y-%m-%d")

                    if meeting_date >= cutoff_date:
                        content = meeting_file.read_text()
                        meetings.append({
                            'date': date_str,
                            'title': meeting_file.stem[11:].replace('_', ' '),
                            'file': str(meeting_file),
                            'summary': content[:400],
                            'source': 'meetings'
                        })
            except (ValueError, Exception):
                pass

    # Sort by date descending
    meetings.sort(key=lambda x: x['date'], reverse=True)
    return meetings[:5]


def gather_person_actions(person_name: str) -> List[Dict[str, Any]]:
    """
    Gather open actions for/from a person.

    Args:
        person_name: Name of the person

    Returns:
        List of action dicts with title, status, file
    """
    actions = []
    name_lower = person_name.lower()

    actions_path = get_vault_path() / "Inbox" / "Actions"
    if not actions_path.exists():
        return []

    for action_file in actions_path.glob("action_*.md"):
        try:
            content = action_file.read_text().lower()

            # Skip completed/archived
            if 'status: completed' in content or 'status: archived' in content:
                continue

            # Check if action involves this person
            if name_lower in content:
                title = action_file.stem.replace('action_', '').replace('_', ' ')
                actions.append({
                    'title': title,
                    'file': str(action_file),
                    'preview': action_file.read_text()[:200],
                    'source': 'actions'
                })
        except Exception:
            pass

    return actions[:5]


def gather_person_tasks(person_name: str) -> List[Dict[str, Any]]:
    """
    Gather tasks related to a person.

    Args:
        person_name: Name of the person

    Returns:
        List of task dicts with title, due_date, file
    """
    tasks = []
    name_lower = person_name.lower()

    tasks_path = get_vault_path() / "Inbox" / "Tasks"
    if not tasks_path.exists():
        return []

    for task_file in tasks_path.glob("task_*.md"):
        try:
            content = task_file.read_text().lower()

            # Skip completed/archived
            if 'status: completed' in content or 'status: archived' in content:
                continue

            # Check if task involves this person
            if name_lower in content:
                title = task_file.stem.replace('task_', '').replace('_', ' ')
                tasks.append({
                    'title': title,
                    'file': str(task_file),
                    'preview': task_file.read_text()[:200],
                    'source': 'tasks'
                })
        except Exception:
            pass

    return tasks[:5]


def orchestrate_121_prep(person_name: str) -> Dict[str, Any]:
    """
    Orchestrate 121 preparation by gathering context from multiple agents.

    Gathers:
    - Recent observations (People Agent)
    - Past 121 notes (Meetings Agent)
    - Open actions for/from person (Tasks Agent)
    - Related tasks (Tasks Agent)
    - Memory context hint (for Claude Code to query claude-mem)

    Args:
        person_name: Name of the person to prepare 121 for

    Returns:
        Dict with gathered context from all agents
    """
    print(f"\n{'='*60}")
    print(f"Orchestrating 121 Prep for: {person_name}")
    print(f"{'='*60}\n")

    result = {
        'person': person_name,
        'timestamp': datetime.now().isoformat(),
        'observations': [],
        'past_121s': [],
        'actions': [],
        'tasks': [],
        'memory_query': None,
        'sources_checked': []
    }

    # Gather from People Agent domain
    print("Gathering observations...")
    result['observations'] = gather_observations(person_name)
    result['sources_checked'].append('observations')
    print(f"  Found {len(result['observations'])} observations")

    # Gather from Meetings Agent domain
    print("Gathering past 121s...")
    result['past_121s'] = gather_past_121s(person_name)
    result['sources_checked'].append('past_121s')
    print(f"  Found {len(result['past_121s'])} past 121s")

    # Gather from Tasks Agent domain
    print("Gathering open actions...")
    result['actions'] = gather_person_actions(person_name)
    result['sources_checked'].append('actions')
    print(f"  Found {len(result['actions'])} open actions")

    print("Gathering related tasks...")
    result['tasks'] = gather_person_tasks(person_name)
    result['sources_checked'].append('tasks')
    print(f"  Found {len(result['tasks'])} related tasks")

    # Memory query hint for Claude Code
    result['memory_query'] = {
        'note': f"Query claude-mem for additional context about {person_name}",
        'suggested_query': f"search: {person_name} feedback observations decisions",
        'project': 'Chief_of_staff'
    }

    # Summary
    total_items = (
        len(result['observations']) +
        len(result['past_121s']) +
        len(result['actions']) +
        len(result['tasks'])
    )

    print(f"\nTotal context items gathered: {total_items}")
    result['total_items'] = total_items

    return result


def orchestrate_mfm_review(squad: str, month: str) -> Dict[str, Any]:
    """
    Orchestrate MFM review by gathering context from multiple agents.

    Gathers:
    - Strategy context (Strategy Agent - L1 overview)
    - OKR targets (Strategy Agent)
    - MFM pre-read file (MFM Agent)
    - Past MFM notes for squad (MFM Agent)

    Args:
        squad: Squad name (e.g., 'strategic accounts')
        month: Month (e.g., 'Feb')

    Returns:
        Dict with gathered context from strategy and MFM domains
    """
    from mfm_agent import find_mfm_file, normalize_month
    from strategy_query_helper import get_l1_overview, get_structure_summary

    print(f"\n{'='*60}")
    print(f"Orchestrating MFM Review: {squad} - {month}")
    print(f"{'='*60}\n")

    result = {
        'squad': squad,
        'month': month,
        'timestamp': datetime.now().isoformat(),
        'strategy_context': None,
        'okr_context': None,
        'pre_read': None,
        'past_mfms': [],
        'sources_checked': []
    }

    # Gather from Strategy Agent domain
    print("Loading strategy context (L1 overview)...")
    l1 = get_l1_overview()
    if l1.get('exists'):
        result['strategy_context'] = {
            'path': l1['path'],
            'content_length': len(l1['content']),
            'note': 'L1 overview loaded - use for OKR context'
        }
        result['sources_checked'].append('strategy_l1')
        print(f"  L1 overview loaded ({len(l1['content'])} chars)")
    else:
        print("  L1 overview not found")

    # Get structure summary for available domains
    structure = get_structure_summary()
    result['okr_context'] = {
        'available_domains': structure.get('l2_domains', []),
        'cross_cutting': structure.get('cross_cutting', []),
        'note': 'Load specific L2 domain for squad if needed'
    }
    print(f"  Available strategy domains: {len(structure.get('l2_domains', []))}")

    # Gather from MFM Agent domain
    print("Finding MFM pre-read file...")
    mfm_result = find_mfm_file(squad, month)

    if mfm_result.get('found'):
        result['pre_read'] = {
            'found': True,
            'path': mfm_result['path'],
            'filename': mfm_result['filename']
        }
        result['sources_checked'].append('mfm_preread')
        print(f"  Found: {mfm_result['filename']}")
    else:
        result['pre_read'] = {
            'found': False,
            'error': mfm_result.get('error'),
            'suggestions': mfm_result.get('suggestions', [])
        }
        print(f"  Not found: {mfm_result.get('error')}")

    # Look for past MFM summaries for this squad
    norm_month = normalize_month(month)
    mfm_base = get_vault_path() / "Process" / "MFM"

    if mfm_base.exists():
        for month_dir in mfm_base.iterdir():
            if month_dir.is_dir() and month_dir.name != norm_month:
                for mfm_file in month_dir.glob(f"*{squad.lower().replace(' ', '*')}*summary*.md"):
                    result['past_mfms'].append({
                        'month': month_dir.name,
                        'file': str(mfm_file),
                        'filename': mfm_file.name
                    })

    print(f"  Found {len(result['past_mfms'])} past MFM summaries")
    result['sources_checked'].append('past_mfms')

    return result


def orchestrate_daily_summary() -> Dict[str, Any]:
    """
    Orchestrate daily summary by gathering context from multiple agents.

    Gathers:
    - Today's completed tasks (Tasks Agent)
    - Today's observations created (People Agent)
    - Today's session logs (Reflection Agent)
    - 4Ps context (Reflection Agent)

    Returns:
        Dict with gathered context for daily summary generation
    """
    from session_log import read_session_log, parse_session_log

    print(f"\n{'='*60}")
    print("Orchestrating Daily Summary")
    print(f"{'='*60}\n")

    today = datetime.now().date()
    today_str = today.strftime('%Y-%m-%d')

    result = {
        'date': today_str,
        'timestamp': datetime.now().isoformat(),
        'completed_tasks': [],
        'observations_created': [],
        'session_logs': [],
        'fourps_context': None,
        'today_summary': None,
        'sources_checked': []
    }

    # Gather from Tasks Agent domain - completed tasks
    print("Gathering completed tasks...")
    tasks_path = get_vault_path() / "Inbox" / "Tasks"
    if tasks_path.exists():
        for task_file in tasks_path.glob("task_*.md"):
            try:
                content = task_file.read_text()
                # Check if completed today
                if 'status: completed' in content.lower():
                    # Check modification time
                    mtime = datetime.fromtimestamp(task_file.stat().st_mtime).date()
                    if mtime == today:
                        title = task_file.stem.replace('task_', '').replace('_', ' ')
                        result['completed_tasks'].append({
                            'title': title,
                            'file': str(task_file)
                        })
            except Exception:
                pass

    result['sources_checked'].append('tasks')
    print(f"  Found {len(result['completed_tasks'])} completed tasks")

    # Gather from People Agent domain - observations created today
    print("Gathering today's observations...")
    obs_paths = [
        get_vault_path() / "People" / "Observations",
        get_vault_path() / "Team" / "Observations"
    ]

    for obs_path in obs_paths:
        if obs_path.exists():
            for obs_file in obs_path.glob(f"observation_*_{today_str}*.md"):
                try:
                    result['observations_created'].append({
                        'file': str(obs_file),
                        'filename': obs_file.name
                    })
                except Exception:
                    pass

    result['sources_checked'].append('observations')
    print(f"  Found {len(result['observations_created'])} observations")

    # Gather from Reflection Agent domain - session logs
    print("Gathering session logs...")
    session_content = read_session_log(today)
    if session_content:
        sessions = parse_session_log(session_content)
        result['session_logs'] = sessions
        print(f"  Found {len(sessions)} session logs")
    else:
        print("  No session logs for today")

    result['sources_checked'].append('sessions')

    # Gather 4Ps context
    print("Loading 4Ps context...")
    fourps_path = get_vault_path() / "4Ps" / "4Ps_2026.md"
    if fourps_path.exists():
        result['fourps_context'] = {
            'path': str(fourps_path),
            'exists': True
        }
        print("  4Ps file found")
    else:
        result['fourps_context'] = {'exists': False}
        print("  4Ps file not found")

    result['sources_checked'].append('fourps')

    # Check for existing today summary
    today_path = get_vault_path() / "Inbox" / "Today" / f"today_{today_str}.md"
    if today_path.exists():
        result['today_summary'] = {
            'path': str(today_path),
            'exists': True
        }

    return result


def handle_ambiguous_query(query: str) -> Dict[str, Any]:
    """
    Handle queries that don't clearly route to a single agent.

    Analyzes the query and suggests which agents might be relevant.

    Args:
        query: The ambiguous query text

    Returns:
        Dict with suggested agents and confidence scores
    """
    from detect_agent import detect_agent

    query_lower = query.lower()

    # Get primary detection
    primary_agent, primary_confidence = detect_agent(query)

    # Check for multi-domain indicators
    multi_domain_indicators = {
        'people_strategy': ['team strategy', 'people okr', 'feedback strategy'],
        'tasks_meetings': ['meeting action', 'follow up meeting', 'task from meeting'],
        'all_domains': ['summary', 'overview', 'status', 'update']
    }

    result = {
        'query': query,
        'primary_agent': primary_agent,
        'primary_confidence': primary_confidence,
        'secondary_agents': [],
        'is_multi_domain': False,
        'recommendation': None
    }

    # Check for multi-domain patterns
    for pattern_type, patterns in multi_domain_indicators.items():
        for pattern in patterns:
            if pattern in query_lower:
                result['is_multi_domain'] = True
                break

    # Suggest secondary agents based on keywords
    secondary_checks = [
        ('tasks', ['task', 'todo', 'action', 'due', 'deadline']),
        ('people', ['observation', 'feedback', '360', 'team member']),
        ('strategy', ['okr', 'strategy', 'goal', 'objective']),
        ('meetings', ['meeting', '121', 'sync', 'prep']),
        ('mfm', ['mfm', 'monthly focus', 'squad review']),
        ('reflection', ['summary', 'daily', 'session', 'reflect'])
    ]

    for agent, keywords in secondary_checks:
        if agent != primary_agent:
            for keyword in keywords:
                if keyword in query_lower:
                    result['secondary_agents'].append({
                        'agent': agent,
                        'matched_keyword': keyword
                    })
                    break

    # Generate recommendation
    if result['is_multi_domain'] or len(result['secondary_agents']) > 0:
        result['recommendation'] = (
            f"This query may need context from multiple agents. "
            f"Primary: {primary_agent} (confidence: {primary_confidence:.2f}). "
            f"Consider also: {', '.join([s['agent'] for s in result['secondary_agents']])}"
        )
    else:
        result['recommendation'] = (
            f"Route to {primary_agent} agent (confidence: {primary_confidence:.2f})"
        )

    return result


# Test function
if __name__ == '__main__':
    print("Orchestrator - Test Suite")
    print("=" * 60)

    # Test 1: 121 Prep
    print("\n1. Testing 121 Prep Orchestration:")
    result = orchestrate_121_prep("Sarah")
    print(f"   Sources checked: {result['sources_checked']}")
    print(f"   Total items: {result['total_items']}")

    # Test 2: Ambiguous Query
    print("\n2. Testing Ambiguous Query Handler:")
    result = handle_ambiguous_query("review Sarah's feedback and update her OKRs")
    print(f"   Primary agent: {result['primary_agent']}")
    print(f"   Secondary agents: {[s['agent'] for s in result['secondary_agents']]}")
    print(f"   Multi-domain: {result['is_multi_domain']}")

    # Test 3: Daily Summary
    print("\n3. Testing Daily Summary Orchestration:")
    result = orchestrate_daily_summary()
    print(f"   Sources checked: {result['sources_checked']}")
    print(f"   Completed tasks: {len(result['completed_tasks'])}")
    print(f"   Session logs: {len(result['session_logs'])}")

    print("\n✓ All tests complete")
