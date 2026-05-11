---
name: mfm-review
description: >
  Review an MFM pre-read document before the Monthly Focus Meeting. Fetches the
  squad's pre-read from Confluence, evaluates it against the five-dimensional
  framework (progress, strategic clarity, monthly focus, target confidence, issue
  identification), performs action carry-forward analysis from the previous month,
  and generates a structured review with scored dimensions, key questions to ask,
  and strengths to acknowledge. Use when "mfm review: [squad] [month]",
  "review mfm: [squad]", or "run [month] mfm for [squad]". NOT for post-meeting
  processing (use mfm-summary).
---

# MFM review

Review an MFM pre-read document before the Monthly Focus Meeting. Produces a scored dimensional analysis, action carry-forward table, and key questions for the meeting.

## Trigger phrases

- `mfm review: [squad] [month]`
- `review mfm: [squad] [month]`
- `run [month] monthly focus meeting for [squad]`
- `run [month] mfm for [squad]`

## Process

### Step 1: Load framework and domain context

1. Read `Work/LLM_Context/MFM_review_framework.md` for detailed criteria
2. Read the MFM agent persona (`.claude/personas/AGENT_MFM.md`) for squad-to-Confluence mappings and domain knowledge

### Step 2: Find document in Confluence

Use the squad-to-Confluence mapping from the agent persona:

1. Parse the command to extract squad name and month
2. Look up the squad's CQL query and run it
3. From results, identify the **target month page** and the **previous month page** (needed for action carry-forward)
4. Fetch both pages with `getConfluencePage` using `contentFormat: markdown`
5. If no match: list available pages and ask user to clarify

### Step 3: Action carry-forward analysis

1. From the **previous month's MFM**, extract the "Next Month" / "Focus Next Month" / "Prioritized Bets" section
2. From the **current month's MFM**, extract the "Progress Last Month" section
3. Match each planned action to its outcome

Produce an action carry-forward table:

| Planned action | Status | Update from current MFM | Learning |
|----------------|--------|-------------------------|----------|
| {Initiative} | Done / Partial / Not done / Carried forward / Dropped | {What current MFM says} | {Why} |

Flag:
- Actions that appear in neither progress nor next month's plan (silently dropped)
- Actions carried forward 2+ months without progress
- New priorities that appeared without explanation of what they displaced

### Step 4: Five-dimensional analysis

Evaluate against the framework's five dimensions, scoring each:
- Examine progress (retrospective quality)
- Decide what to do next (strategic clarity)
- Clear monthly focus
- Confidence in quarterly targets
- Early identification of issues

For each: score (Strong / Adequate / Needs Work), key observations with specific examples from the document.

### Step 5: Generate output

Create prep notes at: `Work/Process/MFM/{Month}/{squad}_mfm_review.md`

**Output structure:**

```markdown
# MFM Review: [Squad] - [Month]

## Executive summary
[Overall grade A-F, 2-3 sentence assessment with top concerns]

## Action carry-forward from [previous month]
[Table from Step 3]

## Content overview

### Metrics update
- Table of each KR: target, result, status, one-line explanation
- Support metrics if applicable

### Progress last month
- Status of each priority with key numbers
- Key learnings from experiments/interviews

### Focus next month
- Each priority with target metrics and key initiatives

### Blockers and asks
- Each blocker with severity tag [Critical/Risk]
- Each ask of leadership

---

## Dimensional analysis

### 1. Examine progress
**Score:** [Strong/Adequate/Needs Work]
- [Key observations with examples]

### 2. Strategic clarity
**Score:** [Strong/Adequate/Needs Work]
- [Key observations with examples]

### 3. Monthly focus
**Score:** [Strong/Adequate/Needs Work]
- [Key observations with examples]

### 4. Target confidence
**Score:** [Strong/Adequate/Needs Work]
- [Key observations with examples]

### 5. Issue identification
**Score:** [Strong/Adequate/Needs Work]
- [Key observations with examples]

## Key questions to ask
1. [Question - why it matters]
2. [Question - why it matters]
3. [Question - why it matters]

## Strengths to acknowledge
- [Positive observation 1]
- [Positive observation 2]
```

## Guidelines

- Follow the conciseness feedback: ~115 lines, use tables for dimensional analysis, include content overview
- Be balanced - note strengths, not just gaps
- Be specific - quote examples from the document
- Questions should be actionable and drive discussion
