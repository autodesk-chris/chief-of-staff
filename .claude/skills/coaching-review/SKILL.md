---
name: coaching-review
description: >
  Process a weekly coaching review meeting into three outputs: shared tracker
  update, manager observations for the day-to-day manager, and private reference
  update. Reads coaching plan for assessment criteria and meeting transcript from
  Granola. Use when "coaching review: [name]" or after a coaching call.
  NOT for pre-call prep (use coaching-prep).
---

# Coaching plan weekly review

Process a weekly coaching review meeting and produce three outputs: a shared tracker update, manager observations for the day-to-day manager, and a private reference update. Reads the coaching plan document for assessment criteria and the meeting transcript from Granola.

## Trigger phrases

- `coaching review: [person name]`
- `coaching review: [person name] week [N]`

## Arguments

- **person**: Name of the person on the coaching plan (required)
- **week**: Week number (optional - auto-detect from tracker if not provided)

## Configuration

Each person on a coaching plan needs a memory reference file containing Confluence page IDs, local file paths, day-to-day manager name, and Slack channel.

**Memory reference naming:** `reference_[firstname]_coaching_confluence.md` in project memory

**Current configurations:**
- Simon Irgens: `reference_simon_coaching_confluence.md`

### Setting up a new coaching plan

When `coaching review:` is used for a person without a memory reference:
1. Ask for: coaching plan document path, day-to-day manager name, Confluence page IDs (tracker, weekly feedback), Slack channel
2. Create the memory reference file
3. Create the tracker document (local + Confluence) from the format below
4. Create the private reference document from the format below
5. Then proceed with the review

## Process

### Step 1: Load context (automatic)

1. **Read memory reference** for the person (search project memory for `reference_[firstname]_coaching_confluence`)
2. **Read the coaching plan document** (the role expectations and coaching plan - path from memory reference)
3. **Read the current tracker** (local markdown - to see previous weeks and outstanding actions)
4. **Read the private reference document** (to review signals to watch and previous observations)

Present a brief summary: "Loaded context for [person], week [N] of [total]. Previous week's actions: [list]. Behaviour areas being tracked: [list from coaching plan]."

### Step 2: Get the meeting transcript

1. Search Granola for the most recent coaching/review meeting with the person
   - Use `mcp__granola__list_meetings` for this week, search for the person's name in meeting titles
   - If multiple matches, show options and ask which one
2. Read the full transcript with `mcp__granola__get_meeting_transcript`
3. Confirm with user: "Found meeting '[title]' from [date]. Use this transcript?"

### Step 3: Extract facts from transcript

Parse the meeting transcript and extract:

- **Deliverables discussed**: What was expected (from previous week's actions) vs what was delivered
- **Feedback given**: What was said directly to the person during the call
- **Expectations clarified**: Any new or refined expectations communicated
- **Actions agreed**: Who committed to what, with dates mentioned
- **Behaviour signals**: Specific observable moments mapped to the coaching plan's behaviour areas
- **Metrics or progress**: Any numbers, milestones, or status updates mentioned

**Critical: facts only.** Extract what was said and observed. Do not interpret, infer motivation, or embellish.
- Good: "Data was included in the plan. Sources were not referenced."
- Bad: "Simon pulled real data and showed analytical thinking."
- Good: "Friday summary was not delivered proactively - Chris had to request it."
- Bad: "Simon showed a lack of initiative with the Friday summary."

### Step 4: Draft the tracker update

Generate the week N section for the shared tracker. The structure must map to the coaching plan document's assessment criteria. Use this format:

```markdown
## Week [N] review ([date range])

**Phase:** [Plan development / Execution / Sustained performance]
**Meeting:** [Day] [Date]
**Next check-in:** [Day] [Date] [(scheduling context if relevant)]

### [Deliverable title if applicable]

[1-2 sentence context on what was due/submitted]

### What was delivered

- **[Item].** [Factual description. Reference specific evidence.]
- **[Item].** [Continue pattern]

### Additional expectations clarified during the call

[Only include this section if new expectations were set or existing ones clarified. Use bullet points with bold leads.]

### Feedback: what needs to change

**1. [Feedback area]**

[Direct, factual description. Quote the coaching plan where relevant. List specific gaps.]

**2. [Continue pattern]**

### Behaviour assessment

| Behaviour | Observation | Rating |
|---|---|---|
| [Area from coaching plan] | [Specific factual observation] | [Positive / Needs improvement / Not yet assessed] |

### Actions

**[Person] - due [day] [date] [(context)]:**
1. [Specific action with clear deliverable]

**[Person] - due [day] [date]:**
2. [Continue numbering sequentially across all people]

**[Person] - ongoing from week [N+1]:**
3. [Recurring expectations]

### Next review focus (week [N+1])

- [Specific questions to assess next week, derived from this week's actions]
```

**Important:** The behaviour areas in the assessment table come from the coaching plan document's "Behaviour changes" or "How progress will be assessed" section. Read those exact areas from the plan. Do not hardcode or assume them.

### Step 5: Confirmation checkpoint

Show the draft tracker update to the user. Ask:
- "Does this accurately capture what happened? Any corrections?"
- "Any actions I missed or dates to adjust?"

Iterate until confirmed. Apply corrections precisely - if the user says something is wrong, fix it without adding interpretation.

### Step 6: Ask for manager observations

**Do not generate these. Ask the user to provide them.**

Prompt: "What are your personal observations for [day-to-day manager name] this week? Short paragraph or bullet points - your honest read on how the week went. These go on the separate feedback page, not shared with [person]."

Wait for the user's input. These are their words, not a synthesis.

### Step 7: Draft the private reference update

Generate a new entry for the progress log in the private reference document:

```markdown
### Week [N] review - [Day] [Date]

**Full summary in shared tracker.** Key private observations below.

**[Topic]:** [Candid observation about what the meeting/week revealed about the person's trajectory]

**Behaviour observations:**
- [Specific private observation with evidence]
- [Pattern continuation or shift from previous weeks]
- [Anything not appropriate for the shared tracker]

**[Red flag / Positive signal - if notable]:** [Specific quote or incident]
```

After drafting, ask the user two questions:
1. "Anything to add or adjust for your private notes?"
2. "Did you notice yourself steering too much during this call - giving answers rather than asking questions?" (This is a self-coaching prompt based on the call guidance in the private reference.)

### Step 8: Write all outputs

After the user confirms all three outputs:

1. **Update local tracker**: Edit the tracker markdown file - replace the "To be completed after week N check-in" placeholder with the confirmed content

2. **Update Confluence tracker**:
   - Get current page content with `mcp__atlassian__getConfluencePage` (page ID from memory reference)
   - Update with `mcp__atlassian__updateConfluencePage` - replace the placeholder section with new content

3. **Update Confluence weekly feedback**:
   - Get current page content from the weekly feedback page (page ID from memory reference)
   - Append the manager observations under a new date header: `### Week [N] - [Date]`
   - Update the page

4. **Update private reference**: Append the progress log entry to the local private reference document (never on Confluence)

5. **Confirm**: "All outputs saved:
   - Tracker updated (local + Confluence)
   - Manager observations saved to [manager name]'s feedback page on Confluence
   - Private reference updated locally
   Week [N] complete."

### Step 9: Call reflection (automatic)

After completing steps 1-8, automatically run a call reflection on the same transcript. This uses the call-reflection skill process:

1. Read `Work/LLM_Context/Personal/growth_patterns.md` (patterns 3-5: over-explaining, giving answers, airtime)
2. Read `Work/LLM_Context/Personal/call_reflections.md` (recent entries for trajectory)
3. Analyse the transcript already loaded in step 2 - no need to re-fetch
4. Present feedback: "Here's how you showed up on this call:" followed by the reflection format from the call-reflection skill
5. Ask: "Save this to your reflections log?"
6. If yes, append to `Work/LLM_Context/Personal/call_reflections.md`

This step ensures coaching calls always get reflected on. See `.claude/skills/call-reflection/SKILL.md` for full analysis criteria.

## Key principles

### Facts, not interpretation
The tracker is a factual record. "Friday summary was not delivered proactively" is factual. "Simon showed a lack of initiative" is interpretation. Stick to what happened, what was said, what was observed.

### The coaching plan is the source of truth
Every assessment maps back to the coaching plan document. If the plan says "Monday plans and Friday summaries delivered consistently from week 1," check exactly that. Don't add criteria the plan doesn't specify.

### Behaviour areas are dynamic
Read the coaching plan document each time. Don't hardcode behaviour areas. The plan for person A might track five behaviours, person B might track three completely different ones.

### Three audiences, three documents
- **Tracker** (shared with person + day-to-day manager): Factual, structured, referenceable. The person should read this and know exactly where they stand.
- **Manager observations** (day-to-day manager only): User's candid read. Not shared with the person being coached.
- **Private reference** (user only): Full context including HR/legal, pattern tracking, evidence trail, self-coaching notes.

Never mix content between these audiences.

### Manager observations are the user's words
Never generate or synthesise the manager observations. Always ask the user to provide them. These are their personal impressions in their voice.

### Evidence trail matters
Every observation should be specific enough to reference later. Include dates, name specific deliverables, note what arrived when. If this moves to formal performance management, the tracker is the evidence base.

### Don't do the person's thinking for them
This applies to both the user during calls AND this skill when generating outputs. If the user fed the person answers during the call, note it in the private reference as a process observation. Surface the pattern, don't hide it.

### Progressive accumulation
The tracker is one document that grows. Each week builds on the previous. Actions from week N are reviewed in week N+1. Patterns across weeks matter more than individual weeks.

## Related files

- Memory references: Project memory `reference_[firstname]_coaching_confluence.md`
- Coaching plan documents: `Work/People/121s/[person]/Coaching plan/[coaching_plan].md`
- Trackers: `Work/People/121s/[person]/Coaching plan/Coaching_plan_tracker_[year].md`
- Private references: `Work/People/121s/[person]/Coaching plan/Coaching_plan_reference_PRIVATE.md`
- Meeting prep notes: `Work/People/121s/[person]/Coaching plan/meeting_prep_week[N]_[date].md`
- Meeting transcripts: Granola MCP
- Confluence: Atlassian MCP (cloudId: `0e31f281-3568-4559-ae88-153abcdead38`)
