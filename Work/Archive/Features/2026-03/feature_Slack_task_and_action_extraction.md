---
type: feature
status: completed
completed-date: 2026-03-29
tags:
  - slack
  - tasks
  - actions
due-date: null
---
# Feature: Slack task and action extraction

## Details

Scan Slack messages to identify commitments made by the user and actions assigned to team members. Creates tasks and actions automatically.

## How it works

- Read Slack messages from configured channels and DMs
- Identify phrases that indicate commitments ("I'll do", "I'll send", "will follow up", "action on me")
- Identify actions assigned to others ("[Name] to...", "[Name] will...")
- Cross-check against existing tasks/actions to avoid duplicates
- Present extracted items to user for confirmation before creating
- Create tasks (user commitments) or actions (team member commitments) with:
  - Title extracted from context
  - Due date if mentioned
  - Person name for actions
  - Link back to original Slack message/thread for reference

## Trigger options

- Run as part of daily summary workflow (end of day)
- Run as part of today report (start of day, reviews previous day)
- Manual trigger: `./pos "scan slack"` or `./pos "slack tasks"`

## Key channels

- Direct messages and group DMs
- Team channels (forma-growth-leads, forma-growth-block-internal)
- Leadership channels
- Configurable channel list stored in settings
