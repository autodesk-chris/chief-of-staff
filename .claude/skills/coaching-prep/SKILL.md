---
name: coaching-prep
description: >
  Prepare for a coaching plan check-in by gathering evidence from Slack,
  Confluence, Granola, and local files. Assesses against coaching plan behaviour
  areas and produces a structured prep document. Use when "coaching prep: [name]",
  "prepare for my check-in with [name]", "I have a coaching meeting with [name]".
  Also triggers automatically for 121: [name] when person is on a coaching plan.
  NOT for post-call processing (use coaching-review).
---

# Coaching plan check-in prep

Prepare for a coaching plan check-in by gathering evidence from all sources, assessing against behaviour areas, and producing a structured prep document. This is the pre-call counterpart to `coaching-review.md` (post-call).

## Trigger phrases

- `coaching prep: [person name]`
- `coaching prep: [person name] week [N]`
- Natural language equivalents: "prepare for my check-in with [person]", "prep for [person] coaching", "I have a coaching meeting with [person]"

**Also triggers when:** `121: [person name]` is used and the person is on an active coaching plan (detected via memory reference file). In this case, the coaching-prep workflow runs instead of the generic 121 prep.

## Arguments

- **person**: Name of the person on the coaching plan (required)
- **week**: Week number (optional - auto-detect from tracker if not provided)

## Configuration

Uses the same memory reference files as `coaching-review`. Each person on a coaching plan has a reference file in project memory.

**Memory reference naming:** `reference_[firstname]_coaching_confluence.md` in project memory

**Current configurations:**
- Simon Irgens: `reference_simon_coaching_confluence.md`

## Process

### Step 1: Load context (automatic)

1. **Read memory reference** for the person (search project memory for `reference_[firstname]_coaching_confluence`)
2. **Read the coaching plan document** (role expectations - path from memory reference)
3. **Read the current tracker** (local markdown - previous weeks, outstanding actions, behaviour assessments)
4. **Read the private reference document** (signals to watch, previous observations, call guidance)

Present a brief status: "Preparing for [person] coaching check-in, week [N] of [total]."

### Step 2: Gather evidence (automatic, no permission needed)

Check all sources for activity since the last check-in. Do these in parallel where possible:

**Slack - coaching channel:**
- Read the coaching Slack channel (channel ID from memory reference)
- Check: Did the person deliver their Monday plan and Friday summary proactively?
- Check: Any messages or updates shared between check-ins?
- Note exact dates and times of deliveries (or non-deliveries)

**Confluence - execution plan:**
- Read the person's execution plan (page ID from memory reference)
- Check: Has it been updated since the last check-in?
- Note when it was last modified
- Identify what's new or changed

**Slack - broader activity:**
- Search for messages from the person across channels since the last check-in
- Note any relevant activity (or absence of activity)

**Granola - recent meetings:**
- Check for any meetings involving the person since the last check-in
- If a Mairead (or day-to-day manager) check-in happened, note it for context

**Local files:**
- Check for any new observations in `Work/People/Observations/`
- Check for any actions assigned to the person in `Work/Inbox/Actions/`

### Step 3: Assess against behaviour areas

Using the behaviour areas from the coaching plan document (read them fresh each time, don't hardcode):

For each behaviour area:
- What evidence exists from step 2? (deliveries, non-deliveries, Slack activity, Confluence updates)
- Is the pattern shifting or persisting compared to previous weeks in the tracker?
- What specific questions would test this behaviour during the call?

### Step 4: Build the pre-call evidence table

Compile findings into a structured evidence check:

| What to check | Status | Notes |
|---|---|---|
| [Expected deliverable from last check-in's actions] | [Delivered / Not delivered / Partial / Unknown] | [Specifics - when, where, quality] |
| [Repeat for each committed action] | | |
| [Async cadence items - Monday plan, Friday summary] | | |
| [Confluence execution plan updated] | | |

### Step 5: Identify key signals

From the evidence, flag:
- **Follow-through gaps**: Anything committed but not delivered (the exact pattern being tracked)
- **Positive signals**: Proactive behaviour, independent work, self-directed adjustments
- **Concerning patterns**: Recurring issues from previous weeks
- **Data points**: Any metrics or progress indicators

### Step 6: Generate call approach

Structure the prep around the coaching plan's call guidance (from the private reference document). Include:

**Opening:** Always start with "Walk me through the week/last few days." Don't prompt with specifics.

**Questions to probe:** Only if the person doesn't cover them. Derived from:
- Outstanding actions from the last check-in
- Evidence gaps (things you couldn't verify from sources)
- Behaviour areas that need testing

**What not to raise:** Items to observe silently (e.g., if the person doesn't mention AI adoption, note the absence rather than prompting)

**Reminder - ask, don't tell:** Include the self-coaching prompt from the private reference. This is critical for coaching calls.

### Step 7: Write the prep file and present summary

**Save to:** `Work/People/121s/[person]/Coaching plan/meeting_prep_week[N]_[date].md`

**Format:**

```markdown
# [Person] coaching - week [N] check-in prep ([Day] [Date])

## Context

**Week [N] of [total].** [Brief context - what phase we're in, any scheduling notes, what the framework says about this stage of the coaching plan.]

## Pre-call evidence check

| What to check | Status | Notes |
|---|---|---|
| [Item] | [Status] | [Details] |

## Key signals

**[Signal type]:** [Description with specific evidence]

## Confluence plan - what's new since [last check-in date]

[Summary of changes to the execution plan, new sections, updated data, concerning or positive content]

## Call approach

### Opening

[Standard opening prompt]

### Key reminder: ask, don't tell

[Self-coaching prompt from private reference]

### Questions to probe (only if not covered)

- "[Question]" ([what it tests])

## Behaviour tracking focus

| Behaviour | What to look for |
|---|---|
| [Area from coaching plan] | [Specific observable for this call] |

## Actions to close the call

- [What to confirm before ending]
- [What to state clearly about next review]
```

**After saving,** present a concise summary to the user (not the full document). Focus on:
- Where we are in the coaching plan timeline
- The 2-3 most important signals from the evidence check
- What to watch for during the call

## Key principles

### Evidence-first, not assumption-first
Check every source before forming a view. "Not delivered" is only valid if you checked the right channel/page. "Unknown" is a valid status.

### The private reference has call guidance - use it
The private reference document contains specific coaching for how the user should conduct calls (e.g., "stop doing Simon's thinking for him"). Surface these reminders in every prep.

### Timeline awareness
The coaching plan has phases. Frame the prep around what matters at this stage:
- **Weeks 1-2:** Plan phase. Assess responsiveness to feedback and iteration speed.
- **Weeks 3-4:** Execution phase. Milestones should be hit. If not, that's a strong signal.
- **Weeks 5-6:** Momentum phase. Trajectory matters, not just activity.
- **Post-plan:** Decision point.

### Don't duplicate the tracker
The prep document is for the upcoming call. It references the tracker but doesn't repeat it. Keep it focused on what the user needs to know walking into the meeting.

### Patterns matter more than incidents
When flagging signals, connect to the pattern across weeks. "This is the third time the summary wasn't delivered proactively" is more useful than "summary not delivered."

## Related files

- Memory references: Project memory `reference_[firstname]_coaching_confluence.md`
- Coaching plan documents: `Work/People/121s/[person]/Coaching plan/[coaching_plan].md`
- Trackers: `Work/People/121s/[person]/Coaching plan/Coaching_plan_tracker_[year].md`
- Private references: `Work/People/121s/[person]/Coaching plan/Coaching_plan_reference_PRIVATE.md`
- Coaching review skill (post-call): `.claude/skills/coaching-review/SKILL.md`
- Confluence: Atlassian MCP (cloudId from memory reference)
