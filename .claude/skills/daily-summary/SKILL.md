---
name: daily-summary
description: >
  End-of-day interview to capture a summary of daily work for weekly 4Ps writing.
  Gathers context from files, conducts a 5-6 question interview, checks for
  growth signals, then saves a structured summary. Use when "daily summary",
  "create daily summary", or similar. Takes 3-5 minutes.
---

# Daily summary interview

End-of-day interview conducted by Claude to capture a summary of daily work for weekly 4Ps writing.

## Trigger

When user says "daily summary", "create daily summary", or similar.

## When to use

At end of work day (takes 3-5 minutes).

## Process

### Step 1: Gather context (automatic, no permission needed)

- Read this week's 4Ps from `Work/Weekly_4Ps/` (priorities and plans)
- Read to-do list from `Work/Inbox/Today/todo_YYYY-MM-DD.md` (completed/in-progress tasks)
- Read Claude session logs from `Work/Daily_Logs/claude_sessions_YYYY-MM-DD.md`
- Read any observations created today from `Work/People/Observations/`

### Step 2: Conduct interview in the conversation

Use gathered context to inform questions. Ask 5-6 questions to supplement file contents:
- What meetings did you have today, and what were the key takeaways?
- What progress did you make on this week's plans?
- What key decisions were made?
- Any important Slack discussions or messages?
- Any surprises or unexpected changes?
- Anything else important to capture?

Let user answer each question in the conversation.

### Step 3: Review for personal growth signals

- Read `Work/LLM_Context/Personal/growth_patterns.md`
- Review meeting notes, Slack context, and user answers for moments matching known patterns or new growth signals
- If anything is spotted, flag it before finalizing the summary
- If confirmed, append to the growth patterns file

### Step 4: Collate and summarize

- Combine file contents + user answers
- Generate structured bullet-point summary
- Include meetings, decisions, progress, Claude sessions, completed tasks

### Step 5: Save summary

- Write to `Work/Daily_Logs/daily_summary_YYYY-MM-DD.md`
- Confirm to user that summary was saved

## Key principle

Files provide baseline context, interview fills in gaps (meetings, Slack discussions, decisions not captured elsewhere).

## Output format

- Bullet-point format
- Enough detail for team member to understand
- Key decisions highlighted
- Meetings summarized with takeaways
- Claude work sessions automatically included
- Links to related observations
- Progress on weekly plans noted

## Best practice workflow

1. Throughout day: Type "session" in Claude conversations to auto-log work
2. End of day: Type "daily summary" to conduct interview and generate summary
3. End of week: Use daily summaries to write 4Ps

## File locations

- Session logs: `Work/Daily_Logs/claude_sessions_YYYY-MM-DD.md`
- Daily summaries: `Work/Daily_Logs/daily_summary_YYYY-MM-DD.md`
- To-do lists: `Work/Inbox/Today/todo_YYYY-MM-DD.md`
