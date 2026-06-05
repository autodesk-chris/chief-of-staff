---
name: 121-prep
description: >
  Prepare for a 1-on-1 meeting with a named person by gathering context from observations,
  actions, Granola, Slack DMs, and previous 121 notes. Accepts inline focal topics and
  inline reference materials (specific Slack messages, documents, files, OKRs, expectations
  docs) and treats them as required anchors. Suggests additional topics for user selection,
  then generates a focused, outcome-driven prep document. Use for ANY 1:1 with a named
  person regardless of topic framing: "121: [name]", "121 prep: [name]", "prep my 121
  with [name]", "prepare for my 1:1 with [name]", "prep me for my call on [topic] with
  [name]", "I have a check-in with [name]", "prepare for my [meeting type] with [name]".
  NOT for coaching check-ins (use coaching-prep). NOT for general team/strategy meetings
  (use prep meeting via the Meetings agent). NOT for post-meeting (use post-meeting).
---

# 121 prep

Prepare for a 1-on-1 meeting with a direct report or colleague. Gathers context from all sources, suggests topics, waits for user selection, then generates a focused prep document.

## Trigger phrases

- `121: [name]`
- `121 prep: [name]`
- Natural language: any request to prepare for a 1:1 with a named person, regardless of topic framing. Examples:
  - "prep my 121 with [name]"
  - "prepare for my 1:1 with [name]"
  - "I have a check-in with [name]"
  - "prep me for my call on [topic] with [name]"
  - "prepare for my [topic] meeting with [name]"
  - "[name] and I have a [type] call today"

**Routing note:** The meetings agent handles coaching plan detection. If the person is on an active coaching plan, the meetings agent routes to coaching-prep instead of this skill. This skill assumes the person is NOT on a coaching plan.

## Arguments

- **person**: Name of the person (required)
- **inline focal topics**: The user may supply focal topics, desired outcomes, or specific research directions in their original message (e.g. "121: Even - focus on capacity study backlog", "prep my call on IDP with Joe"). Parse these and treat them as pre-selected priority topics that skip the suggestion step. They still appear in the agenda but don't need user confirmation.
- **inline reference materials**: The user may name specific source documents, Slack messages, files, or comparison frames they want included (e.g. "check Slack for the IDP doc he shared", "compare with my OKRs", "include the user engagement expectations doc", "use Confluence page X"). These are **required inputs**, not optional context. Fetch every named source in Step 1 and treat them as primary anchors in Step 2c deep research. If a named source cannot be found, ask the user before proceeding rather than silently skipping it.

## Process

### Step 1: Gather context (automatic, all in parallel)

Run all of these without asking permission:

**People directory (do this first):**
- Read `Work/LLM_Context/Contacts/people.md` and look up the person
- Extract their **search terms**, squad, domain, and key relationships
- Use these search terms (not just their name) for all Granola and Slack queries below
- This catches conversations about associated companies, tools, and initiatives (e.g. "Trig" for Mark Ryan, "FSM" for Even Olstad)
- If the person isn't in the file, ask the user for any associated companies/initiatives to search for, and offer to add them to the contacts file afterward

**Observations:**
- Read all files in `Work/People/Observations/` matching the person's name
- Focus on last 90 days, but include older ones if they show relevant patterns

**Previous 121 notes:**
- Read recent files in `Work/People/121s/[person_name]/`
- Extract: what was discussed last time, any commitments made, development threads

**Open actions and tasks:**
- Search `Work/Inbox/Tasks/` and `Work/Inbox/Actions/` for items assigned to or mentioning the person
- Note overdue items and items without due dates

**Granola - recent meetings:**
- Query Granola for meetings with the person (last 30 days)
- Extract: decisions, actions, unresolved topics

**Slack DMs - last 7 days:**
- Find the person's Slack user ID via `mcp__slack__slack_search_users`
- Search DMs with the person for the last 7 days: `mcp__slack__slack_search_public_and_private(query="in:<@USERID> after:YYYY-MM-DD", channel_types="im")`
- Look for messages where they share topics they want to discuss (e.g. "for tomorrow let's discuss: ...", "agenda for our 121", bullet lists of topics)
- Also note any unresolved threads, requests, or commitments from the DM

**Person's 121 notepad (if exists):**
- Check for `Work/People/121s/[person_name]/notepad.md` - may contain running notes for the next 121

### Step 2: Suggest topics (present to user, wait for selection)

From all gathered context, compile a numbered list of suggested topics. Each topic gets one line of context explaining why it's relevant.

**Topic sources, in priority order:**
1. **Their agenda** - topics from Slack DMs where they explicitly listed discussion items (label these as "their topic")
2. **Overdue/urgent actions** - anything past due or due this week
3. **Development threads** - patterns from observations that warrant a conversation
4. **Open commitments** - actions from previous 121s or meetings not yet closed
5. **Strategic/contextual** - relevant developments from Granola meetings or broader context

**Format:**

```
Suggested topics for [Name] 121:

From [Name]'s Slack message ([date]):
  1. [Topic] (their topic)
  2. [Topic] (their topic)
  ...

From context:
  7. [Topic] - [one line of why this is relevant]
  8. [Topic] - [one line of why this is relevant]
  ...

Which topics do you want to include? You can also add your own or reorder.
```

**Wait for user response.** They may:
- Select by number ("1, 2, 4, 7, 8")
- Add their own topics
- Reorder or group topics
- Say "all" or "go with those"

After topic selection, ask one follow-up:

> "Any specific deliverables or commitments you want [Name] to walk away with? (e.g. produce a document, prototype, timeline, decision by a date)"

If the user provides these, embed them in the "action items to land" section and shape the conversation flow questions to drive toward these commitments. If the user says no or skips, proceed without.

**Skip this prompt if:** the user already specified deliverables in their inline context.

### Step 2c: Deep research on focal topics

For the 1-2 main discussion topics (user-supplied inline topics, or the top-priority selected topics), do targeted research beyond the generic context gathered in Step 1.

**Confluence:**
- Search for the person's strategy documents, experiment pages, MFM pre-reads
- Search for related strategies by other people on the same topic (for comparison or context)
- Pull specific data: metrics, experiment results, timeline commitments

**Slack channels:**
- Search relevant team/squad channels for recent discussion threads on the topic
- Look for debates, blockers, or decisions that provide conversation ammunition

**Strategy language:**
- Note the person's own frameworks, terminology, and strategic framing from their documents
- Use their language back at them in the conversation flow - it's more effective coaching to connect to how they already think about the problem

**What to extract:**
- Specific data points that support or challenge the person's current approach
- Comparable approaches by others (e.g. a peer who solved the same problem differently)
- Timeline gaps between stated plans and actual delivery
- The person's own stated diagnosis vs their actual resource allocation

**Do NOT:**
- Turn this into an exhaustive research report - extract only what's needed to make the conversation sharp
- Duplicate the person's strategy back at them - focus on gaps, tensions, and acceleration opportunities

### Step 3: Generate prep document

Using only the selected topics, generate the prep document.

**Document structure (target format):**

```markdown
# 121 with [Name] - [DD] [Month] [YYYY]

## Agenda (aim for 30 min)

| Time | Topic | Owner |
|------|-------|-------|
| 0-5 min | [Their topics first] | [Name] |
| 5-15 min | [Main discussion topic] | Chris |
| 15-22 min | [Secondary topic] | Both |
| 22-28 min | [Quick items / action checks] | Chris |
| 28-30 min | Commitments recap | Both |

[Brief guidance on how to manage the flow - what to timebox, where conversation might spiral, how to redirect.]

---

## [Topic heading - for each selected topic]

### The ask
[What you want to walk out with - a decision, a commitment, clarity on something]

### Why this matters now
[ONE OR TWO succinct sentences. The data point, deadline, or pattern that makes this urgent right now. NOT a bulleted context dump - if you find yourself listing four bullets, you're explaining background, not stating why now.]

### Conversation flow
[2-4 numbered questions that drive toward the outcome. Push toward decisions and commitments, not exploration. Keep each question to one line where possible - the prep doc is a cheat sheet, not a script.]
- Anticipate likely pushback as a single indented line under the question, only when the pushback is genuinely likely. Don't manufacture pushback for every question.
- Reference specific data points inline (metrics, timelines, comparable approaches) - don't restate context that's already in 'Why this matters now'.
- Where possible, use the person's own strategy language and frameworks to frame questions - connects to how they already think about the problem.
- If a comparable approach exists (e.g. a peer solved this differently), reference it as a concrete alternative, not a judgment.

---

## Open actions to check status

| Action | Due | Status |
|--------|-----|--------|
| [Action] | [Date] | Check |

## Development thread

[Only if there's an active development pattern worth continuing. Keep to 3-4 lines max. Connect observations to show trajectory, not just individual incidents.]

## Admin / quick checks

- [ ] [Scheduling confirmations, reminders, quick status checks]
- [ ] [Items that need 30 seconds, not a discussion]

## Action items to land

- [ ] [Specific commitment you want from this meeting]
- [ ] [Specific deliverable with a review date]

---
Sources: [list Granola meetings, observations, Slack DMs, Confluence pages used]
```

**Style rules (from user preferences):**
- Focused on driving a specific outcome, not covering everything
- 4-5 discussion points max per major topic
- Structured to help Chris keep the conversation on track
- Time-boxed sections so the conversation doesn't drift
- Questions push toward decisions and commitments, not exploration
- Anticipate pushback only where genuinely likely, as a single inline line
- Their agenda items come first - show respect for their time
- Sentence case for all headings
- No em dashes - use regular hyphens or restructure
- 'Why this matters now' is 1-2 sentences max. If you need more, you're explaining background, not urgency.
- Conversation flow questions are one line where possible. The prep doc is a cheat sheet, not a script.

### Step 4: Save and present

**Save to:** `Work/People/121s/[person_name]/YYYY-MM-DD_[Name]_121_prep.md`

- Create the person's folder if it doesn't exist
- Use lowercase for folder names (matching existing convention: `maria`, `Even`, etc. - match what already exists)

**Present to user:**
- Show the full document in the terminal for review
- Confirm the save location
- Do NOT generate a Slack message to send to the person (removed - the user handles this themselves)

## Key principles

### Their agenda first
If they shared topics via Slack DM, those lead the agenda. This shows you value their preparation and keeps them engaged. Your topics fill the remaining time.

### Outcome-driven, not exhaustive
Each topic should have a clear "walk out with" outcome. If you can't articulate what the topic achieves, it's not ready for the agenda.

### Patterns over incidents
When raising development feedback, connect observations across time. "The May 20 sync showed the authority that was missing in April" is more useful than "you were good in May."

### Development patterns belong in observations, not the prep doc
If you find yourself writing a multi-paragraph development thread that synthesises behaviour across weeks/months, save it as a fresh observation file (`Work/People/Observations/observation_[Name]_[YYYY-MM-DD].md`) and reference it in the prep doc rather than embedding the full pattern. The prep doc is for tomorrow's conversation; the observation is the durable record that later 121s, 360s, and performance reviews draw on. Always offer to create the observation alongside the prep doc when a pattern surfaces.

### Honest about trade-offs
If there are 10 possible topics and only 30 minutes, say so. Help the user prioritise rather than cramming everything in.

### Don't sanitise
Include the real coaching angles, the pushback to anticipate, the uncomfortable questions. This is a private prep doc, not a shared agenda.

## Related files

- Observations: `Work/People/Observations/observation_[Name]_*.md`
- Previous 121s: `Work/People/121s/[person_name]/`
- Actions/Tasks: `Work/Inbox/Tasks/`, `Work/Inbox/Actions/`
- Coaching prep (for coaching plans): `.claude/skills/coaching-prep/SKILL.md`
- Post-meeting processing: `.claude/skills/post-meeting/SKILL.md`
- 121 prep style preferences: project memory `feedback_121_prep_style.md`
