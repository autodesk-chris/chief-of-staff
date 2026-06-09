---
name: lightning-rounds
description: >
  Draft Chris's weekly reply to the "Weekly Tactical - Lightning Rounds"
  bot post in #priv-forma-design-leadership-fy27. Forward-looking: 3-4
  bullets (max 6) describing what Chris is working on the coming week,
  synthesised from the Plans section of the latest 4Ps plus this week's
  significant calendar markers. Pushes the draft as a Slack draft reply
  in the existing thread - never auto-sends. Auto-invoked by /todo on
  Mondays after Focus today is saved. Manual triggers: "lightning rounds",
  "weekly leadership post", "post to leadership".
---

# Lightning Rounds weekly post

Draft Chris's reply to the weekly leadership "Lightning Rounds" thread and stage as a Slack draft. Never auto-send (per draft-never-send rule).

## Config

Stored in `Work/.state/lightning_rounds.json`:

- `channel_id`: C0A0W3R2K42 (#priv-forma-design-leadership-fy27)
- `bot_id`: B07933B11EC (Weekly Tactical - Lightning Rounds)
- `chris_user_id`: U082ASVFE9Y
- `last_run`, `last_thread_ts`: updated after each successful draft

If the file is missing, create it with the values above.

## Context

The bot posts every Friday ~13:00 BST with this prompt:

> Updates relevant for the Team? Please list in this :thread:
> 1. Top 2-3 things you accomplished or are focused on this week.
> 2. Top 2-3 things you are focused on or planning for next week.

Chris replies on Monday for the prior Friday's thread. His post is forward-looking - what he's working on the coming work week.

## Trigger

- Auto: invoked by `/todo` on Mondays, after `Focus today` is saved (Step 7 of the todo skill).
- Manual: "lightning rounds", "weekly leadership post", "post to leadership", "lightning rounds draft".

## Process

### Step 1: Load config

Read `Work/.state/lightning_rounds.json`. If missing, create with the values listed above.

### Step 2: Find the active thread

`slack_read_channel` on `channel_id`, limit 30. Scan for the most recent message from `bot_id` whose text contains "Top 2-3 things you accomplished".

- Capture its `ts` as `thread_ts`.
- If no such post exists in the last 7 days, abort with: "No lightning rounds post found in the last 7 days. Bot may be delayed - check channel manually."

### Step 3: Skip if already replied

`slack_read_thread` with the captured `thread_ts`. If any reply has `user == chris_user_id`, abort with: "Already replied to this week's lightning rounds. Thread: [permalink]."

### Step 4: Gather inputs (Plans-driven, forward-looking)

**Primary source - latest 4Ps Plans section:**

Find the latest file in `Work/Inbox/4Ps/[Month]/4ps_*.md`. Chris's convention: the Plans section describes the current/coming work week (e.g. "Plans (week of June 1-5)").

- If the latest 4Ps is dated within the last 3 days, use its `## Plans` section.
- If the latest 4Ps is older than 3 days, abort with: "This week's 4Ps not written yet (latest is from [date]). Run `./pos '4ps'` first, then re-run lightning-rounds."

The Plans bullets are the canonical source. Do NOT pull from today's `Focus today` section - that's a daily lens, not a weekly one.

**Supporting source - this week's calendar markers:**

`list_events` for Mon-Fri this week (local time per todo skill TZ rules). Use only to validate or sharpen the Plans bullets - e.g. if Plans says "All Hands prep" and the calendar shows All Hands on Wed, the bullet can mention the day. Do NOT introduce new bullets from the calendar that aren't anchored in Plans.

**Tone calibration - last week's reply:**

Read Chris's previous reply in the prior week's lightning rounds thread to anchor on his current vocabulary and phrasing.

### Step 5: Synthesise the draft

Generate **3-4 bullets by default, max 6** in Chris's style:

- Forward-looking: what he's working on the coming work week.
- Drawn directly from the 4Ps Plans section. One Plans item = one bullet (or merge two closely related items into one).
- Each bullet 4-10 words, noun phrase or present-progressive verb.
- Outputs, decisions, milestones, initiatives - not granular tasks.
- No "This week" / "Next week" headers. Single bulleted list.
- No filler ("continuing work on...", "ongoing..."). State the thing itself.
- Prefer fewer bullets when Plans items overlap or naturally combine.

**Style reference (Chris's June 8 reply):**

- Trig 1:1 build out support
- Community Design competition finalise
- Unified Home decisions and working approach for Amy (and staff)

### Step 6: Show draft in terminal for approval

Display the proposed bullets in terminal. Prompt:

> Approve to push as Slack draft? (y / edit / n)

- `y` - proceed to Step 7.
- `edit` - accept user edits, re-display, re-prompt.
- `n` - abort, no draft created.

### Step 7: Push as Slack draft

`slack_send_message_draft` with:

- `channel_id`: from config
- `thread_ts`: from Step 2
- `text`: the bulleted list, then a blank line, then the Claude disclaimer footer:

```
_Drafted with Claude. If the tone misses, that's the robot. Read for intent._
```

Update `last_run` (ISO timestamp) and `last_thread_ts` in `Work/.state/lightning_rounds.json`.

Confirm to user with thread permalink: "Draft staged in lightning rounds thread. Open Slack to review and send."

## Why no auto-send

Per `feedback_draft_never_send`: drafts are always staged for Chris to review and send himself. Slack drafts in the thread are the cleanest staging method - one click to send from Slack.

## Notes

- Disclaimer footer is included by default per `feedback_claude_disclaimer`. If the bullets feel too terse to carry it, strip in Slack before sending.
- The skill is Plans-driven by design. If the 4Ps isn't written for the week, the skill aborts rather than fabricating from other sources - the Plans section is the considered weekly view.
