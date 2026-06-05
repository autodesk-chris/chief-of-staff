---
name: mfm-review
description: >
  Prepare for a Monthly Focus Meeting by reviewing the squad's pre-read against
  the user's current priorities and the previous month's commitments. Fetches the
  pre-read from Confluence, pulls the prior month's MFM and the Granola notes
  from the last MFM to ground action carry-forward, reads the user's latest
  weekly 4Ps for priority lens, and produces a concise prep doc with 4-5 topics,
  a 'walk out with' list, and notes-to-self. Use when "mfm review: [squad] [month]",
  "review mfm: [squad]", or "run [month] mfm for [squad]". NOT for post-meeting
  processing (use mfm-summary).
---

# MFM review

Prepare a focused, conversation-ready prep doc for a Monthly Focus Meeting. The aim is a tight, scannable brief the user can lead from: priorities lens at the top, accountability on last month's commitments, 4-5 topics for the meeting, light-touch metrics, and a clear set of outcomes to leave with.

## Trigger phrases

- `mfm review: [squad] [month]`
- `review mfm: [squad] [month]`
- `run [month] monthly focus meeting for [squad]`
- `run [month] mfm for [squad]`

## Process

### Step 1: Load framework and domain context

1. Read `Work/LLM_Context/MFM_review_framework.md` for evaluation criteria and red flags.
2. Read `.claude/personas/AGENT_MFM.md` for squad-to-Confluence mappings.

### Step 2: Find the pre-read in Confluence

1. Parse the command to extract squad name and month.
2. Look up the squad's CQL query in the agent persona.
3. Identify the target month's pre-read and the previous month's pre-read.
4. Fetch both with `getConfluencePage` using `contentFormat: markdown`.
5. If the squad publishes multiple drafts in a month, prefer the most recently edited.
6. If no match, list available pages and ask the user to clarify.

### Step 3: Pull the previous MFM's Granola notes

1. Search Granola for the prior MFM by squad/title around the expected date.
2. Confirm the match with the user.
3. Extract decisions and agreed actions from that meeting. These are the real commitments to track, not just what the prior pre-read planned.

### Step 4: Load the user's latest weekly 4Ps

1. Look for the most recent file in `Work/Inbox/4Ps/{Month}/` (e.g. `4ps_YYYY-MM-DD.md`).
2. Extract: Priorities, Plans, Problems. These drive the '4Ps lens' section.
3. If the 4Ps for this week is missing, fall back to the most recent available.

### Step 5: Build action carry-forward

Reconcile what the squad committed to at the last MFM (from Granola) and what they said in the prior pre-read against what landed in the current pre-read.

For each prior commitment, produce a row with:
- Agreed action (from last MFM)
- Status (Holding, Drifted, Done, Carried forward, Silently dropped, Not done)
- Notes - what the current pre-read says, plus any drift to flag

Specifically flag:
- Items silently dropped between pre-reads
- Items 'awaiting results' across two or more months
- Items where the squad has quietly weakened a prior commitment (e.g. one experiment per month becomes discovery only)

### Step 6: Choose 4-5 topics for the meeting

The topics should be the focal areas the user actually wants to land the conversation. They are not the full evaluation. Default principles:

- Lead with the user's #1 4Ps priority and the squad's primary focus area.
- Each topic should drive a decision or unblock work, not just review status.
- Include at least one trade-off / 'what is the squad not doing' question.
- If the prep surfaces a partner-squad delivery risk, that earns its own topic.
- Use the user's notes-to-self to remove or reweight topics they've explicitly said to drop.

### Step 7: Generate the prep file

Create file at: `Work/Process/MFM/{Month}/{squad}_mfm_review.md`

Use this structure exactly. Sentence case headings. No em dashes. No bold inside bullets or prose.

```markdown
# MFM Prep: [Squad] - [Month] [Year]

Source: [pre-read URL] | Previous: [Granola notes URL]

Main focus this meeting: [one sentence stating the dominant topic].

## Your 4Ps lens (week of [date])

| Your priority | What it means for this MFM |
| --- | --- |
| [Priority from 4Ps] | [How it shapes the meeting] |
| ... | ... |

---

## 1. Actions agreed [date of last MFM] - status check

| Agreed action | Status | Notes |
| --- | --- | --- |
| [Action] | [Status] | [What the pre-read says, flags] |

---

## 2. [N] topics for this meeting

### Topic 1. [Headline]

[Why this topic, what to probe, and the specific data points or commitments to reference. Keep to 4-6 bullets max.]

### Topic 2. ...

---

## 3. Metrics - light touch

- [KR or metric]: [number vs target], [trend], [implication].
- [...]

Do not get drawn into a long metrics debate. Note the gap, accept the data caveats, move on.

---

## 4. What I want to walk out with

1. [Concrete outcome 1]
2. ...

## Notes to self

- [Any side notes from the user about angles to lean on or avoid]
```

### Step 8: Reflect user direction

If the user adds further direction after the first draft (e.g. 'drop Home', 'lean towards stopping profiling', 'do not mention AI strategy'), update the doc and reflect their notes in the 'Notes to self' section.

## Style rules

- Sentence case for headings and titles.
- No em dashes. Use a regular hyphen or restructure.
- Bold is only for headings. Do not use bold inside bullets or prose paragraphs.
- Quotes: double quotes only when quoting what someone actually said; single quotes for emphasis, referenced terms, or hypothetical phrasing.
- Continuous single-line paragraphs and bullets (no hard breaks within prose).
- Aim for a one-page, scannable doc. Trim ruthlessly. The user prefers tightness over completeness.

## Guidelines

- Surface drift and silent drops loudly. These are usually the most valuable signals in the prep.
- The 4Ps lens is the framing device. If a topic is not connected to a 4Ps priority, problem, or plan, justify it explicitly or drop it.
- The 'walk out with' list is the single most useful section. Make it concrete and decision-shaped.
- If the user has notes saying to ignore a topic ('ignore Home for now'), respect it. Do not re-introduce.

## Error handling

- Confluence MCP not available: ask the user to reconnect via `/mcp`.
- Multiple pre-read drafts in a month: use the most recently edited; flag the others.
- No prior Granola notes: continue with carry-forward from the prior pre-read only, and note the gap in the prep doc.
- No recent 4Ps file: continue without the lens section; flag to the user that priorities were not loaded.
