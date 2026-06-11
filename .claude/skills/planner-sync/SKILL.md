---
name: planner-sync
description: >
  Sync Microsoft Planner tasks assigned to Chris into the local to-do list.
  Pulls tasks due within the next 2 weeks, dedupes against existing task files
  via planner-id, auto-creates solo-assigned tasks, and prompts for confirmation
  on group/team-assigned tasks. Use when "sync planner", "pull planner tasks",
  "planner sync", or "refresh planner tasks". Also auto-invoked daily by the
  /todo skill (when state is >20h old).
---

# Planner sync

Sync tasks from Microsoft Planner (https://planner.cloud.microsoft) into
`Work/Inbox/Tasks/` so they show up in `/todo`.

## Trigger

- "sync planner", "pull planner tasks", "planner sync", "refresh planner tasks"
- Auto-invoked from the `todo` skill when state file indicates >20 hours since last run

## Scope rules

- **Window**: tasks with `dueDateTime` between today (00:00) and today+14 days (23:59), inclusive
- **Solo bucket**: 1-3 assignees, auto-create
- **Group bucket**: 4+ assignees, present list, user picks which to add
- **Skip**: tasks with no due date, tasks already completed (`percentComplete == 100`)

Chris's M365 user ID: `cb56d796-6354-4290-a42b-20b1aca31beb` (used only if needed for verification; the API already filters to /me).

## Process

### Step 1: Pull tasks

Call `mcp__plugin_m365_m365__list_planner_tasks` with `status: "open"` and `top: 100`.

### Step 2: Filter to next 2 weeks

For each task:
- Skip if `dueDateTime` is null
- Parse `dueDateTime` (ISO 8601 UTC)
- Skip if before today or after today+14 days

Compute today's date with `date +%Y-%m-%d` via Bash.

### Step 3: Split into solo vs group

Count `assignees.length`:
- 1-3 = solo bucket
- 4+ = group bucket

### Step 4: Dedupe

For each candidate task, grep existing task files for the Planner task ID:

```bash
grep -l "planner-id: <task-id>" /Users/smallc/AI/Chief_of_staff/Work/Inbox/Tasks/*.md
```

If a match exists, skip. (Don't update existing files, the user owns local state.)

Also check the Archive in case the task was completed locally but is still open in Planner:

```bash
grep -rl "planner-id: <task-id>" /Users/smallc/AI/Chief_of_staff/Work/Archive/Tasks/ 2>/dev/null
```

If archived, skip and note it.

### Step 5: Fetch descriptions

For each new (non-duplicate) task in scope, call `mcp__plugin_m365_m365__get_planner_task` with the task ID to retrieve the description from `details.description`.

If `hasDescription: false` in the list response, skip the fetch and set description to empty.

### Step 6: Auto-create solo tasks

For each solo task, write a markdown file directly to `Work/Inbox/Tasks/`:

**Filename**: `task_<sanitized_title>.md`
- Sanitize: replace spaces with underscores, remove special chars except hyphens, truncate to ~80 chars
- If file already exists with same name, append `_planner` suffix

**Frontmatter**:
```yaml
---
type: task
status: active
due-date: YYYY-MM-DD
planner-id: <task ID>
source: planner
tags: [planner]
---
```

**Body**:
```markdown
# Task: <Planner title>

## Details

<description from Planner, or "From Microsoft Planner. No description.">

Source: Microsoft Planner
Synced: <today's date>
```

### Step 7: Group bucket, confirm with user

Show the group tasks as a numbered list with title, due date, and assignee count. Ask the user which (if any) to add. Format:

```
Group-assigned Planner tasks (4+ assignees), pick any to add:
  1. <title>, due YYYY-MM-DD, N assignees
  2. ...
Type numbers (e.g. "1, 3") or "none" or "all".
```

Then create the selected ones using the same format as Step 6.

### Step 8: Write state file

Write `Work/.state/planner_sync.json`:

```json
{
  "last_run": "<ISO timestamp>",
  "tasks_in_window": <total in 2-week window>,
  "solo_created": <count>,
  "group_added": <count>,
  "duplicates_skipped": <count>,
  "archived_skipped": <count>
}
```

### Step 9: Summarise

Show the user:
- N solo tasks added
- N group tasks added (out of M presented)
- Skipped N duplicates, N archived
- Next sync recommended in 7 days

List each newly-created task with title, due date, and file path.

## Notes

- The Planner web URL (https://planner.cloud.microsoft/...) is for human use only, there is no public Graph endpoint for it. We use the assigned-to-me Graph endpoint instead, which is what `list_planner_tasks` (no planId) returns.
- Title is used as-is from Planner. No `[Planner]` prefix needed since the tag and `source: planner` field surface it.
- If a task in Planner is updated (title/due date/description change), the local file is NOT updated. To resync a specific task, delete the local file and re-run.
