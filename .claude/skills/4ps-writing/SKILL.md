---
name: 4ps-writing
description: >
  Write or help draft the weekly 4Ps (Priorities, Progress, Plans, Problems)
  update. Follows specific week boundaries, audience awareness, and style rules.
  Use when "write 4Ps", "draft my 4Ps", "help with this week's 4Ps", or similar.
  Reads daily summaries and session logs as input.
---

# 4Ps writing guidance

Write the weekly 4Ps update for Chris's organisation.

## Trigger

When user says "write 4Ps", "draft 4Ps", "help with this week's 4Ps", or similar.

## Week boundaries

- **Progress** covers the previous calendar week (Monday to Friday) only.
- **Plans** covers the current/upcoming calendar week (Monday to Friday).
- **Problems** are current regardless of week.
- **Priorities** are ongoing and usually don't change week to week.

## Dating rules

- Always use the **Monday** of the current working week for the title and filename, regardless of which day the 4Ps is written.
- Title format: `## 4Ps - Week of {Month} {DD}, {YYYY}` where DD is Monday's date.
- Filename format: `4ps_YYYY-MM-DD.md` where YYYY-MM-DD is Monday's date.
- Progress range: explicit Mon-Fri of the previous week (e.g. "Progress (week of May 25-29)").
- Plans range: explicit Mon-Fri of the current week (e.g. "Plans (week of June 1-5)").
- **Verify before saving:** confirm today's day of week, compute the Monday, and double-check the title, filename, Progress range, and Plans range all line up. Date mistakes are easy to make and corrode trust.

## Audience

The 4Ps are read by Chris's organisation - squad leads, their reports, and cross-functional partners. See `Work/LLM_Context/Squads/Squads_overview.md` for team context. Write as a leadership update for this audience, not as a personal task tracker. The 4Ps are shared in Slack - write for scanning, not reading. Readers spend 60 seconds on this.

## Style rules

1. **Priorities:** 3-5 strategic themes. Short descriptor after the bold title, not full sentences.
2. **Progress:** One sentence per bullet, two sentences maximum. State what happened and the outcome - no background context, no metrics detail, no attendee lists. The audience knows the context; just tell them what moved. 5-8 bullets.
3. **Plans:** One line per item. Action and intended outcome only. 4-6 bullets.
4. **Problems:** Frame the issue in one sentence. No full explanation of how it arose. 3-5 bullets.
5. **Leadership discussions:** One line per topic. Group related items (e.g. multiple docs from the same person = one bullet). 3-6 bullets.
6. **Target length:** The entire 4Ps should fit in a single Slack message (~35-40 lines of content, excluding headers). If your draft is longer, cut. Brevity is a feature.
7. **Exclude:**
   - All people-sensitive matters: coaching plans, performance situations, severance, comp, HR conversations, relocation discussions. If it relates to managing a specific person's performance, career, or employment status, it doesn't belong here.
   - Informational updates where Chris was informed but didn't drive or deliver. The test: "Did I produce an output, make a decision, or take an action - or was I just in the room?"
   - Detailed metrics, attendee lists, numbered sub-lists within bullets. These belong in supporting documents, not the 4Ps.
8. **Tone:** Confident peer update. Direct, scannable, outcome-focused.

## Input sources

- Daily summaries: `Work/Daily_Logs/daily_summary_YYYY-MM-DD.md`
- Session logs: `Work/Daily_Logs/claude_sessions_YYYY-MM-DD.md`
- To-do lists: `Work/Inbox/Today/todo_YYYY-MM-DD.md`
- Previous 4Ps: `Work/4Ps/{Month}/`
- Leadership channel: `#priv-forma-design-leadership-fy27` (C0A0W3R2K42)
- Engineering hiring channel: `C0B2JSG4LDT` - scan for hiring updates to include under Operations priority

## Priority alignment filter

Before drafting Progress, run this filter on every candidate item:

### Step 1: Check against previous priorities

Read the most recent 4Ps from `Work/4Ps/{Month}/` to find the previous week's Priorities (or Plans if no prior 4Ps exists).

For each candidate progress item:
- **Aligns to a stated priority** - include it
- **Significant but doesn't align to any priority** - flag for user: "This doesn't map to your stated priorities - include?"
- **A priority had no visible progress** - flag: "No progress found against [priority]. Intentional?"

### Step 2: OKR relevance check

If a deliverable or significant decision relates to Growth OKRs (from `Work/LLM_Context/Squads/Squads_overview.md`) but wasn't in the priorities, flag it separately: "This relates to [KR] but wasn't a stated priority - include?"

### Step 3: Decision surfacing

Significant decisions made during the week should be flagged as candidate progress items, even if they emerged from meetings rather than dedicated work. The test: "Was a direction set that changes what happens next?"

## Output location

Save to `Work/Inbox/4Ps/{Month}/4ps_YYYY-MM-DD.md` where YYYY-MM-DD is the **Monday** of the current working week (e.g. `Work/Inbox/4Ps/June/4ps_2026-06-01.md`).

## Slack draft formatting

When pushing the 4Ps as a Slack draft via `slack_send_message_draft`, the tool interprets content as **standard markdown**, not Slack-native mrkdwn. This means:

- Use `**text**` for bold (single `*text*` renders as italic - do NOT use it for emphasis).
- Italics, underline, and other rich styles are not supported by the draft tool. Bold is the only emphasis available.

Slack draft conversion rules:

1. **Title:** wrap in `**...**` (bold). Example: `**4Ps - Week of June 8, 2026**`.
2. **Subheads** (Priorities, Progress, Plans, Problems, Key leadership discussions): wrap in `**...**` (bold). Underline is not supported in markdown-rendered drafts.
3. **Bullet leads** (the short bold phrase that opens each bullet): wrap in `**...**`.
4. **Body text:** plain text, no italics. Do not wrap body sentences in single asterisks.
5. **Bullets:** use `•` (Unicode bullet) instead of `-` for cleaner Slack rendering.
6. **Numbered Priorities:** keep `1.`, `2.`, etc. - Slack renders these natively.
7. **Footer:** append the Claude disclaimer on a new line wrapped in `_..._` (italics is appropriate here as a disclaimer).

The Markdown file saved locally keeps standard `##` headings and `-` bullets - the conversion above is only for the Slack draft body.
