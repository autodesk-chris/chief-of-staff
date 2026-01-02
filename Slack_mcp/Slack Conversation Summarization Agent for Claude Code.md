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

### Issue: Agent Cannot Access Channels
**Solution**: Ensure your `xoxc` and `xoxd` tokens are correctly configured and that your user account has access to the channels you're trying to summarize.

### Issue: Incomplete Message History
**Solution**: The Slack MCP server may have rate limits. Try narrowing the time range or searching for specific keywords instead of fetching all messages.

### Issue: Agent Provides Vague Summaries
**Solution**: Provide more specific instructions in your prompt. For example, instead of "summarize this channel," try "summarize this channel focusing on technical decisions and blockers."

## Next Steps

Once you have the agent set up and working, consider:

1. Creating templates for different types of summaries (e.g., daily standup, weekly review, incident post-mortem).
2. Building a library of prompts for common summarization tasks.
3. Integrating the agent with other tools in your workflow (e.g., generating reports, creating documentation).
4. Sharing the agent with your team for collaborative use.
