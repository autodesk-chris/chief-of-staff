---
name: 121-prep-carl
description: Prepare for Chris's 1:1 with Carl Christensen (his manager, VP Forma Design). Differs from generic 121-prep because Carl is the boss, not a direct report - sources, tone, and structure are all "boss-up" rather than "boss-down". Reads Chris's running notepad and recent prep doc as primary anchors, pulls leadership-channel signal, frames topics as positions Chris is taking with Carl rather than coaching threads. Use when "121: Carl", "121 prep: Carl", "prep my 1:1 with Carl", or any request to prepare for a meeting with Carl Christensen. Overrides the generic 121-prep skill for Carl specifically.
---

# 121 prep - Carl

Carl-specific variation of the 121 prep skill. The generic skill assumes Chris is preparing for a direct report; Carl is Chris's manager (VP Forma Design), so the sources, structure, and tone all flip.

## Trigger phrases

- `121: Carl`
- `121 prep: Carl`
- Natural language: any request to prepare for a 1:1 with Carl. Examples:
  - "prep my 121 with Carl"
  - "prepare for my 1:1 with Carl"
  - "I have a check-in with Carl"
  - "prep me for my call with Carl"

This skill takes precedence over the generic `121-prep` skill when the person is Carl.

## Key paths (different from generic skill)

| What | Path |
|------|------|
| 121 folder | `Work/People/Carl/121/` |
| Running notepad | `Work/People/Carl/121/121_notepad.md` |
| Prior preps | `Work/People/Carl/121/Carl_121_YYYY-MM-DD_prep.md` (and older variants) |
| Annual review context | `Work/People/Carl/Annual review/` |
| Save filename | `Work/People/Carl/121/Carl_121_YYYY-MM-DD_prep.md` |

## Arguments

- **inline focal topics**: Chris may supply topics inline ("121: Carl - focus on unified home scope, Hans tension"). Treat as pre-selected, skip suggestion step for those.
- **inline reference materials**: Chris may name specific Slack threads, Confluence pages, documents, or framing he wants included. Treat as required anchors, not optional.

## Process

### Step 1: Gather context (all in parallel, no permission needed)

**Carl's running notepad (read first):**
- `Work/People/Carl/121/121_notepad.md`
- This is the primary source for what Chris has been parking for the next 121
- Look for: items under the next-121 heading, items Chris has been mulling, recurring frustrations, Carl's own quotes Chris has captured
- Note Carl's recurring phrases/frameworks - feed them back in the conversation flow

**Most recent prep doc:**
- Find the latest `Carl_121_*_prep.md` in the folder
- Extract: what was on the table last time, action items Chris committed to land, where Carl pushed back

**Granola - last Carl 121s (last 60 days):**
- Query for "Carl 121" or similar - meetings are typically titled this way
- Pull decisions and open commitments from the most recent 1-2 meetings
- Do NOT expect Carl to pre-share an agenda in Granola - Granola is for past meeting record only

**Slack DMs with Carl (last 7 days):**
- Carl user ID: `U01HS2AS43X`
- Search: `mcp__slack__slack_search_public_and_private(query="in:<@U01HS2AS43X> after:YYYY-MM-DD", channel_types="im")`
- Look for:
  - Carl flagging "pay attention to this thread" or pointing Chris at things
  - Pre-shared agenda items ("for our 121", "things to discuss", numbered lists)
  - Open threads where Chris is waiting on Carl's direction or vice versa
  - Tension points or unresolved exchanges

**Leadership channel signal (this is Carl-specific - generic skill doesn't do this):**
- Channel: `#priv-forma-design-leadership-fy27` (ID `C0A0W3R2K42`)
- Also check: any other leadership channels where Carl is active
- Search last 7 days for threads involving Carl, Hans, Khushal, Amy, Julie, Heather, Richard Bao, Ilai
- These threads often surface what's hot for Carl and what he hasn't said directly to Chris yet
- Look for: where Carl took a position, where Carl agreed/disagreed with someone, where Carl asked a question

**Open tasks and actions involving Carl:**
- Search `Work/Inbox/Tasks/` and `Work/Inbox/Actions/` for items mentioning Carl
- Note: items Carl is gating, items Chris owes Carl, items where Carl is the audience downstream (e.g. "Carl can take to Elizabeth")
- Cross-reference today's `Work/Inbox/Today/todo_*.md` for what's overdue or due this week

**This week's 4Ps:**
- Read latest `Work/Inbox/4Ps/[Month]/4ps_YYYY-MM-DD.md`
- Use Priorities and Plans sections to anchor "what Chris is focused on this week" - shapes what's worth bringing to Carl vs handling solo

**Recent meetings where Carl was discussed but not present:**
- Look at recent files in `Work/Meetings/` mentioning Carl
- Especially: strategy/leadership meetings where Carl's name appears as gating or downstream

### Step 2: Suggest topics

Same flow as generic skill - present numbered list, wait for Chris to select. Two differences:

**Topic categories (Carl-specific priority order):**

1. **Time-sensitive Carl-gated items** - things Carl needs to weigh in on this week or that have a deadline (e.g. doc going to Amy, Friday submission)
2. **Open Slack threads needing resolution** - especially tensions where Carl took a position that Chris hasn't closed on
3. **Open commitments from last 121** - what Chris committed to land + status updates Carl will expect
4. **Carl's stated asks** - things Carl has asked Chris to do (mutual expectations, business cases for Elizabeth/Andy Elders, etc.)
5. **Notepad items** - things Chris parked for "next 121"
6. **Strategic / leadership context** - things Chris wants Carl's read on (compound value debates, peer dynamics, escalations)
7. **Admin / FYIs** - quick checks, info exchange, scheduling

**Format:**

```
Suggested topics for Carl 121 - [Date]:

From Carl's Slack DMs ([date range]):
  1. [Topic] - [why it's open]

From the notepad (next 121 section):
  N. [Topic] - [one line]

Time-sensitive / Carl-gated this week:
  N. [Topic] - [deadline + why Carl is the unblocker]

Open from last 121 ([date]):
  N. [Commitment] - [status]

Strategic / leadership context:
  N. [Topic] - [why now]

Which topics do you want to include? (numbers, "all", or add your own)
```

**After topic selection, ask:**
> "Walk out with: what specific direction, agreement, or sponsorship do you want from Carl on each topic?"

If Chris already specified inline, skip this prompt.

### Step 2c: Deep research on focal topics

For the 1-2 main discussion topics, do targeted research:

**Slack threads referenced in the topics:**
- Fetch the actual thread content (not just the search snippet)
- Get Carl's verbatim language - use it back in the conversation flow
- Note who else is in the thread and what positions they took

**Confluence:**
- If the topic references a doc, fetch the current version
- Note any comments from Carl, Hans, Khushal, Amy on the doc

**Previous Carl 121 prep docs (last 2-3):**
- Look for recurring patterns - is this a topic Carl has weighed in on before?
- Use his prior framing/quotes - the consistency anchors the conversation

**What to extract:**
- Carl's verbatim language on the topic (his framings stick)
- Where positions have shifted vs the agreed lane (e.g. "we agreed X in the last 121, now Y is being proposed")
- Concrete data points (dates, deadlines, named stakeholders, dollar figures)
- Likely pushback Carl will have to Chris's position

### Step 3: Generate prep document

**Document structure (Carl-specific):**

```markdown
# 121 with Carl - [DD] [Month] [YYYY]

## Agenda (aim for 30 min)

| Time | Topic | Owner |
|------|-------|-------|
| 0-2 min | [Quick context / opening] | Chris |
| 2-15 min | [Main topic - usually Carl-gated or tension] | Chris |
| 15-25 min | [Secondary topic] | Both |
| 25-28 min | [Admin / quick checks] | Chris |
| 28-30 min | Commitments recap | Both |

[Brief framing - what's the dominant tension this 121 needs to resolve, and where the conversation might drift if not managed.]

---

## Topic 1: [Title]

### The ask
Walk out with: [specific direction, agreement, sponsorship, or escalation from Carl]. Be precise - this is what success looks like.

### Why this matters now
[1-2 sentences max. Deadline, escalation, or shifting position that makes this urgent for THIS 121. Not background.]

### Context Carl needs (3-5 bullets max)
- [Key data point, quote, or development Carl may not have seen]
- [What's changed since last 121 on this topic]
- [Stakeholder positions if relevant]

### Conversation flow
1. **[Opening question or position]** - [one line]
   - Anticipate Carl pushback: "[likely objection]" → "[Chris's counter, using Carl's own language]"
2. **[Second question]** - [one line]
3. **[Decision/commitment question]** - "[exact phrasing of the ask]"

### What I want Carl to commit to
- [ ] [Specific direction or sponsorship - what Chris walks out with]
- [ ] [Second specific commitment if any]

### Use Carl's language
- "[recent Carl quote or framing]" - tie the ask back to how he already thinks about this

---

## Open commitments to check (quick)

| Commitment | Owner | Status |
|------------|-------|--------|
| [From last 121 or recent thread] | Chris/Carl | [Reset / done / blocked] |

## Admin / FYIs (30 seconds each)

- [ ] [Quick info exchange, scheduling, heads-up]

## Action items to land

- [ ] [Specific commitment from Carl]
- [ ] [Specific commitment from Chris]

---
Sources: [Slack DMs, leadership channel threads, Granola meeting IDs, notepad section, prior prep docs, Confluence pages]
```

**Style rules (Carl-specific):**
- This is boss-up. Frame topics as positions Chris is taking, not exploratory conversations.
- "What I want Carl to commit to" replaces the generic "development thread" - Carl isn't being coached.
- "Anticipate pushback" frames Carl's likely objections to Chris's position, not Chris's pushback to Carl.
- Use Carl's verbatim language wherever possible - his framings stick and using them keeps Chris in his frame, which is more persuasive than introducing new framings.
- "Walk out with" is precise: a direction, an agreement, sponsorship for a position, or an escalation. Not "discuss" or "align."
- 30 min is the standard slot. Carl sometimes gives time back - design the agenda so the highest-priority topic comes first.
- When there's a Slack tension, lead with it. Don't bury it behind status updates.
- Sentence case for headings, no em dashes, single quotes for emphasis (per global preferences).

### Step 4: Save and present

**Save to:** `Work/People/Carl/121/Carl_121_YYYY-MM-DD_prep.md`

- Use the date of the 121, not today
- Present the full document in the terminal for review before saving
- Confirm save location
- After saving, offer to update the `121_notepad.md` to remove items that made it into the prep doc (so the notepad stays a forward-looking parking lot, not a history)

## Key differences from generic 121-prep

| Aspect | Generic 121-prep | 121-prep-carl |
|--------|------------------|---------------|
| Direction | Boss-down (Chris → direct report) | Boss-up (Chris → Carl) |
| Path | `Work/People/121s/[name]/` | `Work/People/Carl/121/` |
| Notepad source | Optional, `[name]/notepad.md` | Primary anchor, `121_notepad.md` |
| Slack DM purpose | Their pre-shared agenda | Carl's flags + open tensions |
| Leadership channel | Not used | Critical signal for what's hot |
| Tone | Coaching, development | Positioning, asking, committing |
| "Pushback to anticipate" | Their objections to Chris's coaching | Carl's objections to Chris's position |
| "Development thread" section | Yes | No - replaced with "What I want Carl to commit to" |
| "Walk out with" | A coaching outcome or commitment from them | A direction, sponsorship, or escalation from Carl |

## Recurring Carl frames to reuse

These have come up multiple times - use his language when relevant:

- **"Extreme clarity on ownership creates speed."** (FY27 goals, 23 April 2026)
- **Mutual expectations** - Carl's recurring ask of the leadership team
- **Compound value vs separation** - the pattern Hans raised that Carl has nodded along with
- **Outcome-based design** - the May 19 framing Carl created and asked Chris to integrate
- **"What" vs "how"** - the lane Carl drew for Chris on the unified home work (6/2 121)
- **Solving for now** - frustration Carl expressed about long-running issues never getting fixed (24 Feb notepad)

Read the latest notepad before each prep to update this list - Carl's framings evolve.

## Related files

- Notepad: `Work/People/Carl/121/121_notepad.md`
- Recent preps: `Work/People/Carl/121/Carl_121_*_prep.md`
- Annual review: `Work/People/Carl/Annual review/`
- Generic 121 prep: `.claude/skills/121-prep/SKILL.md` (use for everyone else)
- Coaching prep (if Chris ever ends up on a coaching plan with someone above him): `.claude/skills/coaching-prep/SKILL.md`
