---
name: session-logging
description: >
  Log a Claude work session for inclusion in the daily summary. Automatically
  reviews the conversation, generates a structured summary, and saves it. Use
  when the user types "session" in the conversation. Also checks for personal
  growth signals. NOT for end-of-day summaries (use daily-summary).
---

# Session logging

Log Claude work sessions throughout the day for automatic inclusion in the daily summary.

## Trigger

When the user types **"session"** in the Claude conversation (not in terminal).

## Process

### Step 1: Review the conversation

Automatically review the entire conversation and generate a structured summary with:
- 1-2 sentence overview at the top
- Bullet points covering key topics, decisions, and outputs (as many as needed for clarity)
- Enough detail for someone else to understand what was worked on

### Step 2: Log it

Immediately run `./pos "session: [generated summary]"` via Bash tool. Confirm the session was logged.

### Step 3: Review for personal growth signals

Read `Work/LLM_Context/Personal/growth_patterns.md` and review the conversation for:
- Moments matching known patterns (e.g., sharing before aligning, communication struggles)
- New signals worth reflecting on (e.g., asking for help framing a message, reworking communications, expressing frustration about interactions)
- If anything is spotted, flag it concisely: *"Growth note: I noticed [specific observation]. Want to add this to your growth log?"*
- If Chris confirms, append to the growth patterns file
- If nothing relevant, say nothing - no noise

## Summary format guidelines

- Start with brief overview sentence
- Use bullet points for details
- Include: topics discussed, decisions made, outputs created, problems solved
- Write for an external reader, not just the user
- Be concise but complete

## Example

```
Discussed session logging workflow in the Chief of Staff system and clarified how the daily summary commands work. Decided to implement an automated conversation review feature.

- Clarified difference between 'project summary' and daily summary interview commands
- Explained session logging creates one daily file with all sessions timestamped
- Explored batch logging options - user wanted automated conversation review
- Agreed on approach: user types 'session', Claude auto-generates summary and logs via Bash
```

## Manual command (if needed)

```bash
./pos "session: [what you worked on]"
./pos "/session [summary]"
```

## Storage

- **File:** `Work/Daily_Logs/claude_sessions_YYYY-MM-DD.md`
- **Format:** Timestamped entries appended to daily log file (one file per day, multiple sessions per file)
