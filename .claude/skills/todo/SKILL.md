---
name: todo
description: >
  Generate today's to-do list with an intelligently condensed yesterday overview.
  Runs the ./pos /todo command, then summarises verbose yesterday content into
  a scannable format. Use when "todo", "show todo", "what should I work on
  today", or similar.
---

# Today to-do list

Generate today's to-do list with an intelligently condensed yesterday overview.

## Trigger

When user says "todo", "show todo", "what should I work on today", or similar.

## Process

### Step 0: Determine today's day of week

Run `date "+%A %Y-%m-%d"` via Bash to get the actual current day and date. Do NOT guess the day of week from meeting data or other context. Use this confirmed day throughout the to-do presentation.

### Step 0.5: Weekly Planner sync check

Check if Microsoft Planner tasks need syncing. Read `Work/.state/planner_sync.json`:

- If the file is missing, run the `planner-sync` skill before continuing.
- If `last_run` is more than 6 days ago, run the `planner-sync` skill before continuing.
- Otherwise, skip.

This pulls tasks assigned to Chris in Planner that are due in the next 2 weeks so they appear in the to-do list. Skill handles dedupe via `planner-id` frontmatter.

### Step 1: Generate to-do list

Run `./pos "/todo"` via Bash tool.

### Step 2: Read and condense

Read the generated file: `Work/Inbox/Today/todo_YYYY-MM-DD.md`

Extract the yesterday overview section (content between "## Yesterday's overview" and "## Overdue Tasks" or next section).

Summarise the yesterday overview:
- Keep meeting names (bold headers) but condense to 1-2 sentences focusing on outputs/decisions/actions
- Condense other sections (decisions, actions, completed) to key highlights only
- Aim for ~5-10 lines total for yesterday overview
- Preserve the most actionable information

### Step 3: Add pinned section

Read `Work/.state/email_triage.json` to get the last triage run timestamp and counts. Prepend a **Pinned** section at the very top of the to-do list (before yesterday overview and tasks) with format:

```
## Pinned
- **Review email triage output**: last run {last_run timestamp formatted as "today HH:MM" or "yesterday HH:MM"}. {moved_action_required} items in Action required folder. Check and clear.
```

If the state file is missing or `last_run` is null, show:

```
## Pinned
- **Email triage not yet run today**: run "triage inbox" manually or wait for the 9am scheduled run.
```

If `last_run` is more than 36 hours ago, append a flag: "(stale, scheduled run may have failed; check log at Work/.state/email_triage.log)".

### Step 4: Update and display

Replace the yesterday overview section in the file with the condensed version. Display the updated to-do list to the user with the Pinned section at the top.

## Summarisation guidelines

- Focus on outputs, decisions, and action items
- Remove verbose details that don't affect today's work
- Keep what the user needs to remember or act on
- Each meeting should be 1-2 sentences maximum
- Preserve formatting (bold headers, bullet points)

## Why this approach

- Detailed summaries remain in `Work/Daily_Logs/daily_summary_YYYY-MM-DD.md` files for 4Ps writing
- To-do view stays concise and scannable
- No API costs (uses current Claude conversation)
- User gets context without information overload

## Example condensation

Before: 3 bullet points about budget meeting details
After: "Decided to allocate 70k across Community, Inbound, and Conferences, with focus on Community given resource constraints."
