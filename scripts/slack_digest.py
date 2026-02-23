"""
Slack digest module for Julie (Chief of Staff agent system)
Generates automated daily digest of Slack activity using Slack MCP

Architecture:
- This script provides processing logic and file generation
- Claude Code calls Slack MCP tools directly for data
- Data is passed to these functions for analysis and formatting

Usage:
    # From Claude Code conversation:
    # 1. Call Slack MCP to get channel history
    # 2. Pass data to process_channel_data()
    # 3. Call generate_digest_from_data() to create output

    # Or via command:
    ./pos "slack digest"
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / ".slack_digest_config.json"
OUTPUT_DIR = PROJECT_ROOT / "Work" / "Inbox" / "Today"


def load_config(config_path=None):
    """Load Slack digest configuration."""
    path = config_path or CONFIG_PATH
    try:
        with open(path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found: {path}")
        print("   Create .slack_digest_config.json at project root")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        return None

    # Extract user info for convenience
    config['user_id'] = config.get('user', {}).get('id', '')
    config['user_name'] = config.get('user', {}).get('name', '')

    return config


def parse_slack_csv(csv_text):
    """
    Parse CSV output from Slack MCP into list of message dicts.

    Slack MCP returns CSV with columns:
    msgID, userID, userName, realName, channelID, ThreadTs, text, time, reactions, cursor
    """
    if not csv_text or not csv_text.strip():
        return []

    lines = csv_text.strip().split('\n')
    if len(lines) < 2:
        return []

    # Parse header
    header = lines[0].split(',')
    messages = []

    for line in lines[1:]:
        # Handle CSV with possible commas in text field
        # Simple split won't work for complex cases, but handles most
        values = line.split(',')
        if len(values) >= len(header):
            msg = {}
            for i, col in enumerate(header):
                col_clean = col.strip().lower()
                if col_clean == 'msgid':
                    msg['MsgID'] = values[i].strip()
                elif col_clean == 'userid':
                    msg['UserID'] = values[i].strip()
                elif col_clean == 'username':
                    msg['UserName'] = values[i].strip()
                elif col_clean == 'realname':
                    msg['RealName'] = values[i].strip()
                elif col_clean == 'channelid':
                    msg['ChannelID'] = values[i].strip()
                elif col_clean == 'threadts':
                    msg['ThreadTs'] = values[i].strip()
                elif col_clean == 'text':
                    # Text might contain commas, join remaining if needed
                    msg['Text'] = ','.join(values[i:len(values)-2]).strip()
                elif col_clean == 'time':
                    msg['Time'] = values[-2].strip()
                elif col_clean == 'reactions':
                    msg['Reactions'] = values[-1].strip() if len(values) > len(header) - 1 else ''
            messages.append(msg)

    return messages


def identify_active_threads(messages, threshold_hours=24):
    """
    Identify threads with activity in the last N hours.

    Args:
        messages: List of message dicts from Slack
        threshold_hours: Consider threads active if activity within this time

    Returns:
        dict: {
            'active_threads': {thread_ts: [messages]},
            'standalone': [messages without threads]
        }
    """
    threads = {}
    standalone = []
    cutoff_time = datetime.now() - timedelta(hours=threshold_hours)

    for msg in messages:
        thread_ts = msg.get('ThreadTs', '').strip()

        if thread_ts:
            # Message is part of a thread
            if thread_ts not in threads:
                threads[thread_ts] = []
            threads[thread_ts].append(msg)
        else:
            # Standalone message (not in a thread)
            standalone.append(msg)

    # Filter for threads with recent activity
    active_threads = {}
    for thread_ts, msgs in threads.items():
        # Check if any message in thread is within threshold
        has_recent = False
        for m in msgs:
            try:
                msg_time_str = m.get('Time', '')
                if msg_time_str:
                    # Handle various time formats
                    if 'Z' in msg_time_str:
                        msg_time = datetime.fromisoformat(msg_time_str.replace('Z', '+00:00'))
                    else:
                        msg_time = datetime.fromisoformat(msg_time_str)

                    # Make cutoff_time aware if msg_time is aware
                    if msg_time.tzinfo is not None:
                        from datetime import timezone
                        cutoff_aware = cutoff_time.replace(tzinfo=timezone.utc)
                        if msg_time >= cutoff_aware:
                            has_recent = True
                            break
                    else:
                        if msg_time >= cutoff_time:
                            has_recent = True
                            break
            except (ValueError, TypeError):
                # If we can't parse time, include thread to be safe
                has_recent = True
                break

        if has_recent:
            active_threads[thread_ts] = msgs

    return {
        'active_threads': active_threads,
        'standalone': standalone
    }


def detect_user_participation(thread_messages, user_id):
    """
    Check if user participated in thread and extract participation details.

    Args:
        thread_messages: List of messages in thread
        user_id: User's Slack ID

    Returns:
        dict: {
            'participated': bool,
            'message_count': int,
            'commitments': [list of commitment strings]
        }
    """
    user_messages = [m for m in thread_messages if m.get('UserID') == user_id]

    # Look for commitment keywords in user's messages
    commitment_patterns = [
        "i'll", "i will", "i can", "i'm going to", "let me",
        "i'll handle", "i'll take care of", "i can do"
    ]
    commitments = []
    for msg in user_messages:
        text = msg.get('Text', '').lower()
        for pattern in commitment_patterns:
            if pattern in text:
                commitments.append(msg.get('Text', '')[:100])  # First 100 chars
                break

    return {
        'participated': len(user_messages) > 0,
        'message_count': len(user_messages),
        'commitments': commitments
    }


def categorize_thread(thread_messages, user_id, user_name, channel_config, keywords):
    """
    Categorize thread as action/review/fyi for the user.

    Args:
        thread_messages: List of messages in thread
        user_id: User's Slack ID
        user_name: User's display name
        channel_config: Channel configuration (monitor_level, etc.)
        keywords: List of keywords for inferred action detection

    Returns:
        dict: {
            'category': 'action' | 'review' | 'fyi',
            'reason': string explaining categorization,
            'explicit': bool (True if explicit mention, False if inferred)
        }
    """
    monitor_level = channel_config.get('monitor_level', 'mentions_only')

    # Check for explicit mentions (Category A - applies to ALL channels)
    for msg in thread_messages:
        text = msg.get('Text', '')

        # Direct @mention
        if f'<@{user_id}>' in text:
            return {
                'category': 'action',
                'reason': 'Direct mention of you',
                'explicit': True
            }

        # Name reference with context
        if user_name.lower() in text.lower():
            # Check if it's a question or assignment
            if '?' in text or 'needs to' in text.lower() or 'should' in text.lower():
                return {
                    'category': 'action',
                    'reason': 'You are referenced with question or assignment',
                    'explicit': True
                }

    # Check user participation
    participation = detect_user_participation(thread_messages, user_id)

    if participation['participated']:
        # User is already engaged
        if participation['commitments']:
            return {
                'category': 'action',
                'reason': f"You committed: {participation['commitments'][0][:50]}...",
                'explicit': True
            }
        else:
            return {
                'category': 'review',
                'reason': f"You participated ({participation['message_count']} messages)",
                'explicit': False
            }

    # Inferred actions (Category B - only for "full" monitor level channels)
    if monitor_level == 'full':
        # Check for keyword matches
        thread_text = ' '.join([m.get('Text', '') for m in thread_messages]).lower()

        matched_keywords = [kw for kw in keywords if kw.lower() in thread_text]
        if matched_keywords:
            # Check if it's a question or decision
            has_question = '?' in thread_text
            decision_words = ['decision', 'decide', 'should we', 'agree on', 'approve']
            has_decision = any(word in thread_text for word in decision_words)

            if has_question or has_decision:
                return {
                    'category': 'action',
                    'reason': f"Related to your domain ({', '.join(matched_keywords[:2])})",
                    'explicit': False
                }
            else:
                return {
                    'category': 'review',
                    'reason': f"Relevant discussion ({', '.join(matched_keywords[:2])})",
                    'explicit': False
                }

    # Default: FYI
    return {
        'category': 'fyi',
        'reason': 'General awareness',
        'explicit': False
    }


def format_slack_link(workspace, channel_id, message_ts):
    """Generate Slack message permalink."""
    clean_ts = message_ts.replace('.', '')
    return f"https://{workspace}.slack.com/archives/{channel_id}/p{clean_ts}"


def format_time(time_str):
    """Format timestamp for display."""
    try:
        if 'Z' in time_str:
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        else:
            dt = datetime.fromisoformat(time_str)
        return dt.strftime("%b %d, %I:%M %p")
    except (ValueError, TypeError):
        return time_str


def process_channel_data(channel_messages, channel_config, config):
    """
    Process messages from a single channel.

    Args:
        channel_messages: List of message dicts (from parse_slack_csv)
        channel_config: Channel configuration dict
        config: Full configuration

    Returns:
        dict: {
            'actions': [action items],
            'review': [review items],
            'fyi': [fyi items]
        }
    """
    user_id = config['user_id']
    user_name = config['user_name']
    keywords = config.get('keywords', [])
    workspace = config.get('workspace', 'slack')
    threshold_hours = config.get('digest', {}).get('activity_threshold_hours', 24)

    channel_name = channel_config['name']
    channel_id = channel_config['id']

    actions = []
    review = []
    fyi = []

    # Identify active threads
    thread_data = identify_active_threads(channel_messages, threshold_hours)
    active_threads = thread_data['active_threads']
    standalone = thread_data['standalone']

    # Process each active thread
    for thread_ts, thread_msgs in active_threads.items():
        if not thread_msgs:
            continue

        root_msg = thread_msgs[0]  # First message is typically root

        # Categorize thread
        categorization = categorize_thread(
            thread_msgs, user_id, user_name, channel_config, keywords
        )

        # Create thread summary object
        thread_summary = {
            'channel': channel_name,
            'channel_id': channel_id,
            'thread_ts': thread_ts,
            'root_author': root_msg.get('RealName', root_msg.get('UserName', 'Unknown')),
            'root_time': root_msg.get('Time', ''),
            'root_text': root_msg.get('Text', '')[:200],  # First 200 chars
            'message_count': len(thread_msgs),
            'category': categorization['category'],
            'reason': categorization['reason'],
            'explicit': categorization['explicit'],
            'link': format_slack_link(workspace, channel_id, thread_ts),
            'participation': detect_user_participation(thread_msgs, user_id)
        }

        # Route to appropriate category
        if categorization['category'] == 'action':
            actions.append(thread_summary)
        elif categorization['category'] == 'review':
            review.append(thread_summary)
        else:
            fyi.append(thread_summary)

    # Process standalone messages (check for direct mentions)
    for msg in standalone:
        text = msg.get('Text', '')
        if f'<@{user_id}>' in text:
            actions.append({
                'channel': channel_name,
                'channel_id': channel_id,
                'root_author': msg.get('RealName', msg.get('UserName', 'Unknown')),
                'root_time': msg.get('Time', ''),
                'root_text': text[:200],
                'message_count': 1,
                'standalone': True,
                'explicit': True,
                'reason': 'Direct mention',
                'link': format_slack_link(workspace, channel_id, msg.get('MsgID', ''))
            })

    return {
        'actions': actions,
        'review': review,
        'fyi': fyi
    }


def create_digest_file(filepath, channels, actions, review, fyi, config):
    """
    Create the formatted digest markdown file.

    Args:
        filepath: Where to save the digest
        channels: List of monitored channels
        actions: Action items list
        review: Review items list
        fyi: FYI items list
        config: Full configuration
    """
    today = datetime.now().strftime("%Y-%m-%d")
    today_display = datetime.now().strftime("%B %d, %Y")

    content = f"""---
type: slack-digest
date: {today}
created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

# Slack Digest - {today_display}

## Channels monitored
"""

    for ch in channels:
        level = ch.get('monitor_level', 'mentions_only')
        content += f"- {ch['name']} ({level})\n"

    content += "\n---\n\n"

    # Actions section
    if actions:
        content += f"## Actions for you ({len(actions)})\n\n"
        for action in actions:
            # Title from root text
            title_text = action['root_text'].split('\n')[0][:60]
            content += f"### {action['channel']}: {title_text}...\n\n"

            content += f"**From:** {action['root_author']}"
            if action.get('root_time'):
                content += f" - {format_time(action['root_time'])}"
            content += "\n\n"

            content += f"> {action['root_text'][:150]}...\n\n"

            if not action.get('standalone') and action.get('message_count', 0) > 1:
                content += f"**Thread:** {action['message_count']} messages\n\n"

            content += f"**Why flagged:** {action['reason']}\n\n"

            action_type = "Explicit mention" if action.get('explicit') else "Inferred (domain keywords)"
            content += f"**Type:** {action_type}\n\n"

            content += f"[View in Slack]({action['link']})\n\n"
            content += "---\n\n"
    else:
        content += "## Actions for you\n\nNo action items identified.\n\n---\n\n"

    # Review section
    if review:
        content += f"## Review in detail ({len(review)})\n\n"
        for item in review:
            title_text = item['root_text'].split('\n')[0][:60]
            content += f"### {item['channel']}: {title_text}...\n\n"

            content += f"**From:** {item['root_author']}"
            if item.get('root_time'):
                content += f" - {format_time(item['root_time'])}"
            content += "\n"

            if item.get('message_count', 0) > 1:
                content += f"**Thread:** {item['message_count']} messages\n"

            participation = item.get('participation', {})
            if participation.get('participated'):
                content += f"**Your participation:** {participation.get('message_count', 0)} messages\n"

            content += f"\n**Why flagged:** {item['reason']}\n\n"
            content += f"[View in Slack]({item['link']})\n\n"
            content += "---\n\n"

    # FYI section (condensed)
    if fyi:
        content += f"## FYI - awareness only ({len(fyi)})\n\n"
        for item in fyi[:5]:  # Limit to 5
            title_text = item['root_text'].split('\n')[0][:40]
            content += f"- **{item['channel']}:** {title_text}... "
            content += f"[View]({item['link']})\n"

        if len(fyi) > 5:
            content += f"\n*+ {len(fyi) - 5} more threads*\n"
        content += "\n"

    # Summary stats
    content += "---\n\n## Summary\n\n"
    content += f"- **Threads analyzed:** {len(actions) + len(review) + len(fyi)}\n"
    content += f"- **Actions identified:** {len(actions)}\n"
    content += f"- **Explicit mentions:** {sum(1 for a in actions if a.get('explicit'))}\n"
    content += f"- **Inferred actions:** {sum(1 for a in actions if not a.get('explicit'))}\n"
    content += f"- **For review:** {len(review)}\n"

    content += "\n---\n*Generated by Julie Slack Digest*\n"

    # Write file
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)

    return filepath


def generate_digest_from_data(channel_data_list, config=None):
    """
    Generate digest from pre-fetched channel data.

    Args:
        channel_data_list: List of tuples (channel_config, messages_list)
        config: Configuration dict (loads from file if None)

    Returns:
        dict: Structured data for today summary integration
    """
    if config is None:
        config = load_config()
        if config is None:
            return None

    today = datetime.now().strftime("%Y-%m-%d")

    all_actions = []
    all_review = []
    all_fyi = []
    processed_channels = []

    print("Processing Slack channels...")

    for channel_config, messages in channel_data_list:
        channel_name = channel_config.get('name', 'Unknown')
        print(f"  - {channel_name}: {len(messages)} messages")

        processed_channels.append(channel_config)

        # Process channel data
        result = process_channel_data(messages, channel_config, config)

        all_actions.extend(result['actions'])
        all_review.extend(result['review'])
        all_fyi.extend(result['fyi'])

    # Generate digest file
    digest_path = OUTPUT_DIR / f"slack_digest_{today}.md"
    create_digest_file(
        str(digest_path),
        processed_channels,
        all_actions,
        all_review,
        all_fyi,
        config
    )

    print(f"\nSlack digest generated: {digest_path}")
    print(f"  Actions: {len(all_actions)}")
    print(f"  Review: {len(all_review)}")
    print(f"  FYI: {len(all_fyi)}")

    # Return structured data for today summary
    return {
        'actions': all_actions,
        'review_threads': all_review,
        'fyi_threads': all_fyi,
        'digest_path': str(digest_path),
        'stats': {
            'total_threads': len(all_actions) + len(all_review) + len(all_fyi),
            'actions_count': len(all_actions),
            'explicit_count': sum(1 for a in all_actions if a.get('explicit')),
            'inferred_count': sum(1 for a in all_actions if not a.get('explicit'))
        }
    }


def get_today_summary_section(digest_data):
    """
    Generate Slack highlights section for today summary.

    Args:
        digest_data: Output from generate_digest_from_data()

    Returns:
        str: Markdown formatted section for today summary
    """
    if not digest_data:
        return ""

    actions = digest_data.get('actions', [])
    review = digest_data.get('review_threads', [])
    digest_path = digest_data.get('digest_path', '')

    content = "## Slack highlights\n\n"

    # Actions section (ALL actions - never limit)
    if actions:
        content += f"### Actions for you ({len(actions)})\n"
        for action in actions:
            action_type = "explicit" if action.get('explicit') else "inferred"
            title = action.get('root_text', '')[:40].split('\n')[0]
            content += f"- **{title}...** ({action_type}) - {action.get('reason', '')} [{action.get('channel', '')}]\n"
        content += "\n"
    else:
        content += "### Actions for you\nNo action items from Slack today.\n\n"

    # Active discussions (limit to top 3)
    if review:
        content += f"### Active discussions ({len(review)})\n"
        for item in review[:3]:
            title = item.get('root_text', '')[:30].split('\n')[0]
            msg_count = item.get('message_count', 0)
            participation = item.get('participation', {})
            your_msgs = participation.get('message_count', 0) if participation.get('participated') else 0
            content += f"- {title}... - {msg_count} msgs"
            if your_msgs:
                content += f", you: {your_msgs}"
            content += f" [{item.get('channel', '')}]\n"

        if len(review) > 3:
            content += f"*+ {len(review) - 3} more discussions*\n"
        content += "\n"

    # Link to full digest
    if digest_path:
        today = datetime.now().strftime("%Y-%m-%d")
        content += f"[View full Slack digest](./slack_digest_{today}.md)\n\n"

    return content


# Stub functions for MCP integration
# Claude Code calls actual MCP tools and passes data to processing functions

def get_channel_history_stub(channel_id, hours=48):
    """
    Stub for getting channel history.

    In actual use, Claude Code will:
    1. Call mcp__SlackMCPServer__conversations_history(channel_id=channel_id, limit="2d")
    2. Parse the CSV output using parse_slack_csv()
    3. Pass result to process_channel_data()
    """
    print(f"  [STUB] Would fetch history for channel {channel_id} (last {hours}h)")
    print("  [NOTE] Claude Code should call Slack MCP directly:")
    print(f"         mcp__SlackMCPServer__conversations_history(channel_id='{channel_id}', limit='2d')")
    return None


def get_thread_replies_stub(channel_id, thread_ts):
    """
    Stub for getting thread replies.

    In actual use, Claude Code will:
    1. Call mcp__SlackMCPServer__conversations_replies(channel_id=channel_id, thread_ts=thread_ts, limit="90d")
    2. Parse the CSV output
    3. Use for detailed thread analysis
    """
    print(f"  [STUB] Would fetch thread {thread_ts} in channel {channel_id}")
    return None


def run_digest_workflow():
    """
    Main workflow entry point for ./pos "slack digest" command.

    This prints instructions for Claude Code to follow.
    """
    config = load_config()
    if not config:
        return None

    print("\n=== Slack Digest Workflow ===\n")
    print("Configuration loaded:")
    print(f"  User: {config['user_name']} ({config['user_id']})")
    print(f"  Channels: {len(config['channels'])}")

    print("\n--- Instructions for Claude Code ---\n")
    print("To generate the Slack digest, follow these steps:\n")

    print("1. For each channel, fetch message history:")
    for ch in config['channels']:
        print(f"\n   Channel: {ch['name']}")
        print(f"   Call: mcp__SlackMCPServer__conversations_history(")
        print(f"           channel_id='{ch['id']}',")
        print(f"           limit='2d'")
        print(f"         )")

    print("\n2. Parse each response using parse_slack_csv(response)")

    print("\n3. Call generate_digest_from_data() with the channel data:")
    print("""
   from slack_digest import load_config, parse_slack_csv, generate_digest_from_data

   config = load_config()
   channel_data = []

   # For each channel response:
   messages = parse_slack_csv(slack_response)
   channel_data.append((channel_config, messages))

   # Generate digest:
   result = generate_digest_from_data(channel_data, config)
""")

    print("\n4. The digest file will be created at:")
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"   Work/Inbox/Today/slack_digest_{today}.md")

    print("\n" + "=" * 40 + "\n")

    return config


# Test function
if __name__ == '__main__':
    print("Slack Digest Module - Test Mode\n")

    # Test config loading
    config = load_config()
    if config:
        print(f"Config loaded: {config['user_name']}")
        print(f"Channels: {len(config['channels'])}")
        print(f"Keywords: {config['keywords'][:3]}...")

    print("\n--- Running workflow ---\n")
    run_digest_workflow()
