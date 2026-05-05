---
name: call-reflection
description: >
  Analyse meeting transcripts against personal communication patterns and a
  broader best practice framework. Provides honest feedback on how you showed up.
  Use when "reflect: [person]", "call reflection: [person]", "reflect on today's
  calls", "reflect on this week's calls". Single call or batch mode. Also runs
  automatically after coaching-review.
---

# Call reflection

Analyse Granola meeting transcripts against Chris's known communication patterns and a broader best practice framework. Provides honest feedback on how he showed up. Tracks improvement over time. Can run on a single call or batch-reflect on all calls from a period.

## Trigger phrases

- `reflect: [meeting name or person]` - single call reflection
- `call reflection: [person]` - single call reflection
- `reflect on my last call with [person]` - single call reflection
- `reflect on today's calls` - batch: all calls from today
- `reflect on this week's calls` - batch: all calls from the current week
- `reflect on last week's calls` - batch: all calls from last week
- `add pattern: [description]` - add a new personal pattern to growth_patterns.md
- `add practice: [description]` - add a new best practice to communication_framework.md

## Process

### Step 1: Load reference files

1. Read `Work/LLM_Context/Personal/growth_patterns.md` - active personal patterns being tracked
2. Read `Work/LLM_Context/Personal/communication_framework.md` - broader best practice library
3. Read `Work/LLM_Context/Personal/call_reflections.md` - scan the most recent 2-3 entries to understand the current trajectory (improving, plateauing, or regressing)

### Step 2: Find the meeting(s)

**Single call mode:**
1. Search Granola for the meeting using `mcp__granola__list_meetings` (this week first, then last week)
2. Match by person name or meeting title
3. If multiple matches, show options and ask which one
4. Pull full transcript with `mcp__granola__get_meeting_transcript`
5. Confirm: "Found '[title]' from [date]. Analyse this one?"

**Batch mode** (today/this week/last week):
1. List all meetings for the period using `mcp__granola__list_meetings`
2. Filter to 1:1s and small meetings (skip large group meetings, all-hands, presentations where Chris is audience only)
3. Show the list: "Found N calls to reflect on: [list]. Proceed with all?"
4. Pull transcripts sequentially and analyse each one
5. Present a combined summary at the end with per-call details

### Step 3: Analyse the transcript

For each pattern in growth_patterns.md, scan the transcript for instances. Be specific - quote or closely paraphrase what was said.

**Pattern 3 - Over-explaining:**
- Look for extended monologues (more than 3-4 sentences on a single point)
- Metaphors or analogies that run long
- Repeating the same point in different words
- For each instance: note what was said, how long it ran, and suggest a shorter alternative

**Pattern 4 - Giving answers vs asking questions:**
- Look for moments where Chris suggests specific tools, people, approaches, or solutions
- Look for moments where the other person invites guidance and Chris provides it fully
- Look for moments where Chris could have asked a question instead
- For each instance: note what was said, what the question alternative would have been
- Also note when Chris does this well - asks instead of tells

**Pattern 5 - Airtime imbalance:**
- Estimate the rough talk ratio (Chris vs other person) based on transcript length of "Me:" vs "Them:" segments
- Flag if Chris's share exceeds ~40% in a coaching/1:1 context
- Note the longest uninterrupted Chris segments

**Framework scan (communication_framework.md):**

After checking active patterns, scan the transcript against the broader framework. Don't try to score every practice - focus on the 2-3 most notable observations from the framework that aren't already covered by active patterns. Look for:

- **Strong positive examples** worth reinforcing (e.g., a great perspective-shifting question maps to framework 7.2)
- **Repeated gaps** that might warrant promotion to active tracking (e.g., consistently asking closed questions maps to framework 1.1)
- **Context-specific insights** (e.g., great at challenging through questions with direct reports but less so with peers)

When flagging a framework practice, reference it by number (e.g., "Framework 2.1 - Silence as a tool") so Chris can look it up if interested.

**Promotion logic:** If a framework practice has been flagged in 3+ reflections, suggest promoting it to a personal pattern in growth_patterns.md with real examples from Chris's calls.

**Also look for:**
- New observations not covered by either active patterns or the framework
- Positive moments worth reinforcing - things Chris did well
- Context-specific observations (e.g., different behaviour with different people)

### Step 4: Present feedback

**Single call format:**

```
## Call reflection: [person] - [date]

### Active patterns

**[Pattern name] (Pattern N):**
- [Specific instance with quote/paraphrase]
- [Suggested alternative]

### Framework observations
- [Framework reference, e.g., "Framework 2.1 - Silence as a tool"]: [specific observation]
- [Consider promoting?] [If flagged 3+ times across reflections]

### What you did well
- [Specific positive moments with examples, referencing framework where applicable]

### Progress
[1-2 sentences comparing to recent reflections - is the pattern improving?]

### One thing to try next time
[Single, concrete, actionable suggestion for the next call with this person]
```

**Batch format (multiple calls):**

Present each call individually using the format above, then add a summary:

```
## Weekly reflection summary - [date range]

### Across [N] calls:
- **Most frequent pattern:** [which pattern showed up most, with count]
- **Strongest area:** [what Chris consistently does well]
- **Framework practice to consider tracking:** [if any practice flagged in 3+ calls]
- **One focus for next week:** [single actionable theme]
```

Keep it direct. Don't soften the feedback. Chris values intellectual honesty.

### Step 5: Save

Ask: "Save this to your reflections log?"

If yes, append to `Work/LLM_Context/Personal/call_reflections.md` under a new date/meeting header. For batch mode, save the individual reflections and the summary.

### Step 6: Pattern promotion (if applicable)

If a framework practice has been flagged in 3+ reflections:
1. Note it: "Framework [X.Y] has come up [N] times now. Promote to active tracking?"
2. If Chris confirms, add it to `growth_patterns.md` as a new numbered pattern, populated with real examples from his calls (not the generic framework description)

## Contextual awareness

### Different people, different dynamics

The patterns may show up differently depending on who Chris is talking to:
- **Direct reports on coaching plans** (e.g., Simon): Pattern 4 is most critical - giving answers undermines the assessment
- **Peers:** Pattern 3 (over-explaining) may be more relevant
- **Senior stakeholders:** Airtime and conciseness matter most
- Note these contextual differences in the feedback

### Relationship to other skills

- **coaching-review skill:** When processing a coaching call, the coaching-review skill should trigger a call reflection automatically (see integration notes below)
- **daily summary:** The daily summary flow already checks growth_patterns.md - call reflections feed the same system
- **session logging:** If a call reflection surfaces something notable, it should be flagged during session logging too

## Integration with coaching-review

When the coaching-review skill is running (processing a Simon or similar coaching call), it should:
1. Complete the normal coaching-review process (steps 1-8)
2. Then automatically run steps 3-5 of this skill against the same transcript
3. Frame the feedback with: "Here's how you showed up on this call:"

This ensures coaching calls always get reflected on without Chris having to remember to trigger it separately.

## Related files

- Active patterns: `Work/LLM_Context/Personal/growth_patterns.md`
- Best practice framework: `Work/LLM_Context/Personal/communication_framework.md`
- Reflections log: `Work/LLM_Context/Personal/call_reflections.md`
- Coaching review skill: `.claude/skills/coaching-review/SKILL.md`
