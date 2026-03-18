"""
Agent detection module for Julie (Chief of Staff agent system)
Routes commands to appropriate specialized agents based on pattern matching
"""

def detect_agent(command_text):
    """
    Detect which agent should handle a command based on pattern matching.

    Args:
        command_text (str): The command to analyze

    Returns:
        tuple: (agent_name, confidence_score)
            agent_name: 'tasks', 'people', 'strategy', 'reflection', 'meetings', 'mfm', or 'orchestrator'
            confidence_score: float between 0.0 and 1.0
    """
    command_lower = command_text.lower()

    # Task patterns (includes reminders, actions, decisions, ideas, features, notepad processing, archiving)
    task_patterns = [
        'new task:', 'new reminder:', 'new action:', 'new idea:',
        'new feature:', 'new decision:', 'update:', 'change due date:', '/today',
        'process notepad', 'notepad process', '/notepad', 'notepad confirm', 'notepad',
        'archive completed', 'archive',
        'actions', '/actions', 'list actions',
        'decisions', '/decisions', 'list decisions',
        'new_daily:', 'new daily:'
    ]
    if any(p in command_lower for p in task_patterns):
        return ('tasks', 1.0)

    # Hiring patterns (must be before people to avoid conflicts)
    hiring_patterns = [
        'setup role:', 'screen cvs:', 'review cv:', 'shortlist:',
        'interview prep:', 'interview eval:', 'candidate summary:'
    ]
    if any(p in command_lower for p in hiring_patterns):
        return ('hiring', 1.0)

    # People patterns (note: 121: is handled by meetings agent)
    people_patterns = [
        'observation:', '360 review:', '360:', 'feedback:',
        'performance conversation prep:', 'perf conversation prep:'
    ]
    if any(p in command_lower for p in people_patterns):
        return ('people', 1.0)

    # MFM patterns (specific MFM commands route to MFM Agent)
    mfm_patterns = ['mfm review:', 'review mfm:', 'mfm summary:', 'post mfm:']
    if any(p in command_lower for p in mfm_patterns):
        return ('mfm', 1.0)

    # Strategy patterns (general strategy work, not MFM-specific)
    strategy_keywords = ['okr', 'strategy', 'bet', 'kr1', 'kr2', 'kr3']
    if any(k in command_lower for k in strategy_keywords):
        return ('strategy', 0.8)

    # Reflection patterns (includes Slack digest/report, session logging, 4Ps, and leadership update)
    reflection_patterns = [
        'daily summary', '/summary', '/daily', 'sync meetings',
        'slack report', '/slack-report',
        'slack digest', '/slack-digest', 'slack summary',
        'scan slack', 'slack tasks', '/scan-slack',
        'session:', '/session',
        '4ps roundup', 'team 4ps',
        '4ps', '/4ps', 'generate 4ps', 'weekly 4ps', '/weekly', 'finalize 4ps',
        'leadership update', 'prep leadership update'
    ]
    if any(p in command_lower for p in reflection_patterns):
        return ('reflection', 1.0)

    # Meetings patterns
    meetings_patterns = ['prep meeting:', '121:', 'post meeting:', 'process meeting:', 'finalize meeting:']
    if any(p in command_lower for p in meetings_patterns):
        return ('meetings', 1.0)

    # Default to orchestrator with low confidence
    return ('orchestrator', 0.5)


def load_agent_context(agent_name):
    """
    Load the appropriate agent context file.

    Args:
        agent_name (str): Name of the agent

    Returns:
        str: Path to the agent context file, or None if orchestrator
    """
    if agent_name == 'orchestrator':
        return None  # Use main CLAUDE.md

    agent_files = {
        'tasks': '.claude/personas/AGENT_TASKS.md',
        'people': '.claude/personas/AGENT_PEOPLE.md',
        'strategy': '.claude/personas/AGENT_STRATEGY.md',
        'reflection': '.claude/personas/AGENT_REFLECTION.md',
        'meetings': '.claude/personas/AGENT_MEETINGS.md',
        'mfm': '.claude/personas/AGENT_MFM.md',
        'hiring': '.claude/personas/AGENT_HIRING.md'
    }

    return agent_files.get(agent_name)


# Test function
if __name__ == '__main__':
    test_commands = [
        'new task: Review budget',
        'observation: Sarah - great presentation',
        'performance conversation prep: Sarah',
        'daily summary',
        'session: worked on feature X',
        'slack report',
        'slack digest',
        'scan slack',
        'slack tasks',
        '4ps roundup',
        'team 4ps',
        'leadership update',
        'prep leadership update',
        'mfm review: strategic accounts Feb',
        'what are the current OKRs?',
        'prep meeting: Budget Review',
        'setup role: Community Programme Manager',
        'screen CVs: Community Programme Manager',
        'interview eval: Tom Hamilton for Community Programme Manager',
    ]

    print("Testing agent detection:")
    for cmd in test_commands:
        agent, confidence = detect_agent(cmd)
        print(f"  '{cmd}' -> {agent} (confidence: {confidence})")
