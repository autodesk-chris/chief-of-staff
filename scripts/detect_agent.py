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

    # Task patterns (includes reminders, actions, decisions, ideas, features, notepad processing)
    task_patterns = [
        'new task:', 'new reminder:', 'new action:', 'new idea:',
        'new feature:', 'new decision:', 'update:', 'change due date:', '/today',
        'process notepad', 'notepad process', '/notepad', 'notepad confirm', 'notepad'
    ]
    if any(p in command_lower for p in task_patterns):
        return ('tasks', 1.0)

    # People patterns
    people_patterns = ['observation:', '360 review:', '360:', 'feedback:', '121:']
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

    # Reflection patterns
    reflection_patterns = ['daily summary', '/summary', '/daily', 'sync meetings']
    if any(p in command_lower for p in reflection_patterns):
        return ('reflection', 1.0)

    # Meetings patterns
    meetings_patterns = ['prep meeting:', '121:', 'post meeting:', 'process meeting:']
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
        'mfm': '.claude/personas/AGENT_MFM.md'
    }

    return agent_files.get(agent_name)


# Test function
if __name__ == '__main__':
    test_commands = [
        'new task: Review budget',
        'observation: Sarah - great presentation',
        'daily summary',
        'mfm review: strategic accounts Feb',
        'what are the current OKRs?',
        'prep meeting: Budget Review',
    ]

    print("Testing agent detection:")
    for cmd in test_commands:
        agent, confidence = detect_agent(cmd)
        print(f"  '{cmd}' -> {agent} (confidence: {confidence})")
