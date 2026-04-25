---
type: feature
status: completed
completed-date: 2026-03-29
tags:
  - slack
  - reporting
due-date: null
---
# Feature: Slack report

## Details

Comprehensive Slack report combining multiple views into a single actionable document. Replaces the simpler `slack digest` with a richer, structured report.

## Sections

1. **Actions for you (last 48h)** - messages requiring action from monitored channels, with short thread context summaries
2. **Saved messages (last 7 days)** - messages user has saved, with short thread summaries for context
3. **Thread activity** - summaries of new threads and existing threads with new activity across monitored channels
4. **Leadership FY27 summary** - dedicated section with summaries for each leadership channel:
   - #priv-forma-design-leadership-fy27 (main leadership)
   - #priv-forma-design-leadership-people-allocation-fy27 (people/hiring)
   - #priv-forma-design-leadership-budget-fy27 (budget)

## Trigger

- `slack report` or `/slack-report`

## Output

- Written to `Work/Inbox/Today/slack_report_YYYY-MM-DD.md`
- Displayed in conversation
