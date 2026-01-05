# Slack Conversation Summarization Agent for Claude Code

This document provides a comprehensive system prompt and workflow for building a conversation summarization agent in Claude Code that leverages the Slack MCP server to automatically analyze and summarize your Slack conversations.

## System Prompt for the Summarization Agent

Use the following system prompt when creating a new agent in Claude Code. This prompt defines the agent's behavior, capabilities, and instructions for summarizing Slack conversations.

```
You are a Slack Conversation Summarization Agent. Your role is to help users understand and extract insights from their Slack conversations by providing concise, well-structured summaries of messages, threads, and channels.

## Your Capabilities

You have access to the Slack MCP server, which allows you to:
- List all conversations (channels and direct messages) in the workspace
- Fetch message history from specific conversations
- Search for messages by keyword or timestamp
- Retrieve user information and channel details
- Add reactions to messages
- Post messages to channels (if enabled)

## Your Responsibilities

1. **Summarize Conversations**: When asked to summarize a channel or thread, fetch the relevant messages and create a clear, concise summary that captures the key points, decisions, and action items.

2. **Extract Action Items**: Identify and list any tasks, decisions, or follow-ups mentioned in the conversation.

3. **Identify Key Participants**: Note who the main contributors to the conversation are.

4. **Highlight Important Decisions**: Flag any decisions made during the conversation that may impact the team or project.

5. **Provide Context**: When summarizing, provide context about the conversation's purpose and any relevant background information.

## Workflow

When a user asks you to summarize a conversation:

1. **Clarify the Scope**: Ask the user which channel, thread, or time period they want summarized if not specified.
2. **Fetch Messages**: Use the Slack MCP tools to retrieve the relevant messages.
3. **Analyze Content**: Read through the messages and identify key themes, decisions, and action items.
4. **Structure the Summary**: Organize the summary into clear sections:
   - **Overview**: Brief description of the conversation topic
   - **Key Points**: Main topics discussed
   - **Decisions Made**: Any decisions or conclusions
   - **Action Items**: Tasks or follow-ups with assigned owners if mentioned
   - **Participants**: Key people involved
5. **Deliver the Summary**: Present the summary in a clear, readable format.

## Summary Format

Use the following structure for all summaries:

### Conversation Summary: [Channel/Thread Name]
**Date Range**: [Start Date] - [End Date]
**Participants**: [List of key participants]

#### Overview
[2-3 sentence description of the conversation]

#### Key Points
- [Point 1]
- [Point 2]
- [Point 3]

#### Decisions Made
- [Decision 1]
- [Decision 2]

#### Action Items
- [ ] [Task 1] - Owner: [Person], Due: [Date if mentioned]
- [ ] [Task 2] - Owner: [Person], Due: [Date if mentioned]

#### Additional Notes
[Any other relevant information]

## Best Practices

- **Be Concise**: Aim for summaries that capture the essential information without unnecessary details.
- **Preserve Context**: Don't lose important context when condensing information.
- **Highlight Urgency**: Flag any time-sensitive items or urgent decisions.
- **Use Clear Language**: Avoid jargon and use language that's easy to understand.
- **Respect Privacy**: Only summarize conversations the user has access to.

## Example Usage

**User**: "Can you summarize the #product-roadmap channel from this week?"

**Agent Response**:
1. Lists the #product-roadmap channel
2. Fetches messages from the past 7 days
3. Analyzes the conversation
4. Provides a structured summary following the format above

---

Remember: Your goal is to save users time by distilling lengthy conversations into actionable insights.
```

## Enterprise Slack Configuration

**Important for Enterprise Slack Users:** If you're using an Enterprise Slack workspace (like Autodesk Enterprise Slack), you may encounter the `enterprise_is_restricted` error when trying to list channels or access certain API endpoints. This is due to enterprise security policies that restrict standard user token access.

### Solution: Enterprise-Specific Parameters

The slack-mcp-server supports two environment variables specifically designed for Enterprise Slack environments:

**SLACK_MCP_CUSTOM_TLS:**
- Enables custom TLS handshake to Slack servers
- Works with the User-Agent to make requests appear as legitimate browser traffic
- Set to `true` for enterprise environments

**SLACK_MCP_USER_AGENT:**
- Custom User-Agent header that mimics a real browser
- Helps bypass enterprise security restrictions
- Example: `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36`

### Configuration Example

When adding the MCP server to Claude Code, include these parameters:

```bash
claude mcp add SlackMCPServer --transport stdio \
  --env SLACK_MCP_XOXC_TOKEN=your-xoxc-token \
  --env SLACK_MCP_XOXD_TOKEN=your-xoxd-token \
  --env SLACK_MCP_CUSTOM_TLS=true \
  --env SLACK_MCP_USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36" \
  --env SLACK_MCP_USERS_CACHE=/path/to/.users_cache.json \
  --env SLACK_MCP_CHANNELS_CACHE=/path/to/.channels_cache.json \
  -- /path/to/slack-mcp-server -transport stdio
```

### Docker Configuration (Alternative)

If you prefer using Docker, configure like this in your Claude Code MCP settings:

```json
{
  "slack": {
    "command": "docker",
    "args": [
      "run",
      "-e", "SLACK_MCP_XOXC_TOKEN",
      "-e", "SLACK_MCP_XOXD_TOKEN",
      "-e", "SLACK_MCP_CUSTOM_TLS",
      "-e", "SLACK_MCP_USER_AGENT",
      "--rm",
      "-i",
      "ghcr.io/korotovsky/slack-mcp-server:latest",
      "mcp-server",
      "--transport", "stdio"
    ],
    "env": {
      "SLACK_MCP_XOXC_TOKEN": "xoxc-your-token",
      "SLACK_MCP_XOXD_TOKEN": "xoxd-your-token",
      "SLACK_MCP_CUSTOM_TLS": "true",
      "SLACK_MCP_USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
  }
}
```

## Using the Agent in Claude Code

To use this agent in Claude Code:

1. Create a new chat or project in Claude Code
2. Copy the system prompt above
3. Paste it into the system prompt field or at the beginning of your conversation
4. Start by asking the agent to list available channels or summarize a specific conversation

## Example Prompts to Get Started

Here are some example prompts you can use to interact with your summarization agent:

### List Channels
```
List all the channels in my Slack workspace that I have access to.
```

### Summarize a Channel
```
Summarize the #engineering channel from the past 3 days. Include key decisions and action items.
```

### Summarize a Thread
```
Fetch the conversation in the #general channel about the Q1 planning and provide a summary with action items.
```

### Search and Summarize
```
Search for all messages in the past week that mention "deadline" and summarize the key points.
```

### Extract Action Items
```
Go through the #project-alpha channel and extract all action items mentioned. For each item, note who it's assigned to if mentioned.
```

### Daily Standup Summary
```
Summarize all messages from the #standups channel from today. Highlight any blockers or urgent items.
```

## Advanced Customization

You can further customize the agent by:

- **Adding Domain-Specific Logic**: Modify the summary format to include fields relevant to your specific use case (e.g., customer feedback, bug reports, feature requests).
- **Integrating with External Tools**: If Claude Code supports additional MCP servers, you could integrate them to cross-reference information (e.g., linking Slack messages to Jira tickets).
- **Scheduling Summaries**: Set up Claude Code to automatically generate summaries at regular intervals (e.g., daily, weekly).
- **Multi-Channel Analysis**: Create agents that analyze conversations across multiple channels to identify trends or recurring themes.

## Troubleshooting

### Issue: "enterprise_is_restricted" Error (Enterprise Slack)
**Problem**: When trying to list channels or use certain API endpoints, you receive an error: `{"ok":false,"error":"enterprise_is_restricted"}`

**Cause**: Enterprise Slack workspaces have security policies that restrict standard user token access to certain API endpoints, particularly channel listing.

**Solution**: Configure the enterprise-specific parameters (see "Enterprise Slack Configuration" section above):
1. Add `SLACK_MCP_CUSTOM_TLS=true` to your MCP server configuration
2. Add `SLACK_MCP_USER_AGENT` with a browser User-Agent string
3. Restart Claude Code to apply the changes
4. Test by asking Claude to list your Slack channels

These parameters make the MCP server's requests appear as legitimate browser traffic, bypassing the enterprise restrictions.

**Alternative Solution**: If the above doesn't work, you may need to request admin approval to install a Slack app with a bot token (xoxb), which bypasses these restrictions.

### Issue: Agent Cannot Access Channels
**Solution**: Ensure your `xoxc` and `xoxd` tokens are correctly configured and that your user account has access to the channels you're trying to summarize.

### Issue: Tokens Expired
**Problem**: Receiving `invalid_auth` errors or authentication failures

**Cause**: Browser session tokens (xoxc/xoxd) expire when you log out of Slack or after extended inactivity, especially in enterprise environments with automatic logout policies.

**Solution**:
1. Extract fresh tokens from your browser (see authentication setup guide)
2. Update your `.env` file or MCP configuration with the new tokens
3. Restart Claude Code

**Prevention**: Keep your Slack browser tab open and active while using the MCP server.

### Issue: Incomplete Message History
**Solution**: The Slack MCP server may have rate limits. Try narrowing the time range or searching for specific keywords instead of fetching all messages.

### Issue: Agent Provides Vague Summaries
**Solution**: Provide more specific instructions in your prompt. For example, instead of "summarize this channel," try "summarize this channel focusing on technical decisions and blockers."

### Issue: "Failed to connect" in `claude mcp list`
**Problem**: When running `claude mcp list`, the SlackMCPServer shows "Failed to connect"

**Solution**: This may be a false negative from the health check. Try using the MCP server anyway - it often works despite this status. Test by asking Claude to interact with Slack. If it truly doesn't work, check the Claude Code logs at `~/Library/Logs/Claude Code/main.log` for detailed error messages.

## Next Steps

Once you have the agent set up and working, consider:

1. Creating templates for different types of summaries (e.g., daily standup, weekly review, incident post-mortem).
2. Building a library of prompts for common summarization tasks.
3. Integrating the agent with other tools in your workflow (e.g., generating reports, creating documentation).
4. Sharing the agent with your team for collaborative use.
