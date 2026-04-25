---
type: feature
status: completed
completed-date: 2026-03-29
tags:
  - slack
  - leadership
due-date: null
---
# Feature: Leadership update from Slack

## Details

Generate a leadership update by combining Slack channel reviews with strategic/tactical meeting notes. Identifies key topics worth sharing with the broader team.

## How it works

- Review FY27 leadership Slack channel for recent discussions
- Review architecture group Slack channel
- Review tactical and strategic meeting notes (from Granola/meeting transcripts)
- Synthesize into candidate topics for the leadership update
- Present candidates to user for selection and editing
- Confirm final content before any sharing

## Workflow

1. **Gather**: Pull Slack messages from leadership channels (last week or configurable period)
2. **Enrich**: Cross-reference with meeting transcripts from the same period
3. **Synthesize**: Identify themes - decisions made, direction changes, key discussions
4. **Draft**: Create structured update with bullet points per topic
5. **Review**: Present to user for confirmation and edits
6. **Share**: Post to designated Slack channel (only after explicit confirmation)

## Output format

- Short intro line
- Bullet points grouped by theme
- Each bullet: what happened, why it matters, any actions/next steps
- Concise enough to read in 2 minutes

## Trigger

- `./pos "leadership update"` or `./pos "prep leadership update"`
