---
name: todo
description: >
  Generate today's to-do list with an intelligently condensed yesterday
  overview, then offer an interactive bucketed menu of "Today's options"
  drawn from this week's 4Ps priorities, today's meetings, Slack DMs and
  @mentions from VIPs and direct reports (last 5 days), and tasks due
  today/overdue/next 3 days. User selects which items become the day's
  focus, which is then written into the file after Pinned. Runs the
  ./pos /todo command first. Use when "todo", "show todo", "what should
  I work on today", or similar.
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

### Step 5: Today's options (interactive)

After displaying the file, gather signals from five sources and present a bucketed menu in terminal. Do NOT write to the file at this stage - user selects first.

**Sources to read:**

1. **People sets** - parse `Work/LLM_Context/Contacts/people.md`:
   - **VIPs** = names in `## Leadership` section, excluding Chris Small
   - **Direct reports** = rows in any squad table where the role field contains `, direct report`

2. **This week's 4Ps** - find the latest file in `Work/Inbox/4Ps/[Month]/4ps_*.md`. If the latest file is dated within the last 7 days, use it; otherwise fall back to the most recent prior file. Extract Priorities and Plans sections.

3. **Today's meetings** - m365 calendar via `list_events`, scoped to today. Flag "prep needed" for: 1:1 with a VIP or direct report, MFM, leadership sync, or any meeting where Chris is the organiser and the topic is not routine.

   **Time zone conversion (required):** `list_events` returns each event's `start` time in the organiser's `startTz` (commonly `Europe/Oslo` = CEST/CET). Chris is in `Europe/Dublin` / `Europe/London` (IST/BST = UTC+1 in summer, GMT = UTC+0 in winter). Always convert event times to Chris's local clock before displaying or writing into the todo file. Run `date "+%z"` once at the start of the meeting block to confirm the current local offset, then subtract from each event's source TZ. Display only the local time - never the source TZ time. For Oslo-organised events in summer the offset is -1 hour (12:00 Oslo = 11:00 BST).

4. **Slack signals** - for each VIP and each direct report:
   - Scan DMs in the last 5 days. Surface threads where the last message is from them (i.e. unanswered by Chris).
   - Scan @mentions in shared channels in the last 5 days. Surface those where Chris has not replied or reacted.
   - Do NOT extend this scan to the wider Tier 2 (squad members, Autodesk stakeholders) - too noisy.

5. **Tasks** - from the todo file just generated by `./pos /todo`:
   - Overdue
   - Due today
   - Due in <=3 days

**Compute available focus time (display before the menu):**

- Baseline workday: 08:30-18:00 local = 9.5h.
- **Self-blocks count as work time** (strategic work, meeting prep, or lunch). Do NOT subtract them.
- Subtract real meetings only (not self-blocks).
- **On Mondays, subtract an additional 2h for the weekly prep block** (email triage, 4Ps writing, /todo run, week planning). Also surface this as a pinned item.
- Display the resulting number, e.g. "Available focus time today: 6.0h".

**Display format in terminal** (numbered globally so user can pick by number). Bucket options into Strategic (4Ps) and Tactical (tasks + Slack replies). Size each tactical pick:

```
## Today's options

**Available focus time today: 6.0h** (workday 9.5h - 1.5h meetings - 2h Monday prep)

### Strategic - this week's 4Ps priorities
1. [priority text]
2. ...

### Today's meetings
3. 09:00 - [title] (prep needed: [reason])
4. ...

### Tactical - from VIPs / direct reports (last 5 days)
5. **Carl** DM: "[subject/first line]" - 2d ago, unanswered (S, ~15min)
6. **Amy** @mention in #channel: "[context]" - yesterday (S, ~15min)
...

### Tactical - tasks due today / overdue / next 3 days
7. [task title] (overdue 5d, M ~60min)
8. [task title] (due today, L ~120min)
...
```

Size key: S = <30min, M = 30-90min, L = 90min+.

**Prompt user:** "Which items do you want to focus on today? (numbers, comma-separated, or `none`)"

### Step 5.5: Challenge before writing

After the user picks, run these checks. If any fire, surface the issue and ask the user to revise before writing the Focus today section. Do NOT save until challenges are resolved (either revised picks or explicit confirmation to override).

- **Over the cap.** If picks > 3: respond "That's [N] items, cap is 3. Which [N-3] drop?"
- **No strategic item.** If 0 strategic picked but 4Ps priorities exist: respond "No strategic item picked. Want to add [top 4Ps priority]?"
- **Over-commit.** If sum of sized minutes > available focus time: respond "[picked minutes] mins picked vs [available] mins free. Drop one, or move a meeting?"
- **Meeting-heavy day.** If meetings consume >60% of the 9.5h workday: list the meetings and ask "Meetings take [X]h of 9.5h today. Any of these movable? [list]"

Be direct. State the rule, state the gap, ask for the revision. Don't soften.

### Step 6: Write Focus today section

Once challenges are resolved, insert a `## Focus today` section into the todo file **immediately after `## Pinned`** (and before the condensed yesterday overview), containing only the selected items (max 3). Format each as a bullet with a source tag and size:

```
## Focus today
- [4Ps] Trig - one-to-one user monitoring (L, ~3h block)
- [Task] Fix capacity/strategy data (M, ~90min)
- [Task] Glint follow-up - Kaylin Glazer (S, ~30min)
```

Save the file and confirm to the user with a short line, e.g. "Focus today saved (3 items, ~5h)."

If the user picks `none`, skip writing the section.

**Monday pinned additions:** On Mondays, prepend two pinned items in this order:
```
- Weekly prep block (2h): email triage, 4Ps writing, /todo run, week planning.
- Write weekly 4Ps: review daily summaries from last week and draft update. Run `./pos "4ps"` to start.
```

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
