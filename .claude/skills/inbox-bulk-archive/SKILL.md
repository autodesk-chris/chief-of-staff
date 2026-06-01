---
name: inbox-bulk-archive
description: One-time bulk archive of old emails from the Outlook inbox to the built-in Archive folder. Pulls all emails received before a specified cutoff date and moves them in batches via the M365 MCP. Use when "bulk archive: pre-YYYY", "archive emails before YYYY-MM-DD", or "bulk archive inbox". Designed as a removable one-off cleanup tool - delete the skill directory once the inbox is cleaned up. NOT for daily triage (use email-triage instead).
---

# Inbox bulk archive

One-shot bulk cleanup tool. Moves all emails received before a specified date to Outlook's built-in Archive folder. Designed to be deleted from the skills directory once the historical cleanup is complete.

## Usage

Trigger with a date target:
- "bulk archive: pre-2026" (archives anything received before 2026-01-01)
- "archive emails before 2026-01-01"
- "bulk archive: pre-2025"

If no date is given, ask for one. Default to the most recent full year ago if user can't specify.

## Workflow

1. **Parse the cutoff date** from the trigger phrase. "pre-YYYY" means before YYYY-01-01T00:00:00Z.
2. **Sample count**: call `list_emails` with `folder=inbox`, `before=<cutoff>`, `top=1` to confirm there is mail to archive and surface the oldest visible date. Report the sample.
3. **Confirm scope once** with the user before starting: "Archive everything received before <date>? This is irreversible from the skill (you can manually move back from Archive if needed)."
4. **Loop in batches of 100** until empty:
   - `list_emails` with `folder=inbox`, `before=<cutoff>`, `top=100`
   - Extract IDs. If the response is large, save to a temp file and use Bash:
     `grep -o '"id": "[^"]*"' <file> | sed 's/"id": "//; s/"$//'`
   - Move each in parallel using `update_email` with `moveToFolder="archive"` (the well-known folder name, no folder ID lookup needed).
   - Continue until `count=0` or `hasMore=false` and the latest count is 0.
5. **Report** total moved and any failures.

## Behavior notes

- Parallel `update_email` calls work well in batches of 50-100 per message. Cap at ~100 to avoid token bloat.
- For backlogs of 500+ emails, **delegate the loop to a subagent** (general-purpose) to keep the main conversation context clean. The subagent does the iteration and returns a single success count.
- Uses Outlook's built-in `archive` well-known folder name. Don't use a Triage sub-folder.
- Email IDs change when items move between folders. Each batch must re-query for fresh IDs - don't reuse IDs from a previous list.
- Skip the "proceed?" check per batch - only confirm once at the start.

## Subagent delegation pattern

For large runs, spawn a general-purpose subagent with a prompt like:

```
Move N emails (received before <cutoff>) from Outlook Inbox to Archive using the M365 MCP.

Setup: load tools via ToolSearch with query "select:mcp__plugin_m365_m365__list_emails,mcp__plugin_m365_m365__update_email"

Loop ceil(N/100) times:
1. list_emails (folder=inbox, before=<cutoff>, top=100)
2. Extract IDs from large output via Bash grep on the saved file
3. Move each in parallel with update_email (moveToFolder="archive"), cap at 50-100 calls per message
4. Count successes and failures

Return a single concise report: total moved, failures, done.
```

## Removal

When the inbox is cleaned up to a date you're comfortable with, delete this skill:

```bash
rm -rf .claude/skills/inbox-bulk-archive
```

Or leave it in place for occasional re-runs. It is harmless when idle (only activates on explicit trigger).

## Why separate from email-triage

This is one-time historical cleanup, not a daily classification workflow. Keeping it isolated:
- Avoids cluttering email-triage's tier-based logic
- Makes future removal trivial
- Different mental model: bulk-move-many vs classify-and-route
