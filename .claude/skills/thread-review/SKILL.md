---
name: thread-review
description: >
  Review a Slack thread, DM, or group DM and recommend a next move. Reads the
  full conversation, decodes reactions/emojis as signal, summarises the topic
  and each participant's position, recommends one concrete next action, and
  drafts a succinct response in Chris's voice. Always offers to push the draft
  into Slack as a real draft (never auto-sends). Use when "review thread:
  [URL]", "review conversation: [URL]", "thread review: [URL]", "what should I
  do with this thread/conversation", or when given a Slack thread, DM, or
  group DM URL and asked for next steps. NOT for sweeping public/private
  channels (use scan slack / slack report).
---

# Thread review

Review a single Slack thread, DM, or group DM end-to-end. Produces four outputs: topic summary, per-participant positions, recommended next move, and a draft response written in Chris's voice. Always offers to push the draft into Slack as a real attached draft (never sends without explicit approval).

## Trigger phrases

Primary:
- `review thread: [URL]`
- `review conversation: [URL]`

Natural language fallbacks:
- "what should I do with this thread/conversation: [URL]"
- "next steps for this thread/conversation: [URL]"
- "review this thread/conversation [URL]"
- Any message that pastes a Slack thread, DM, or group DM URL and asks for analysis or next steps

## Process

### Step 1: Parse the URL and fetch the conversation

The skill operates in **two modes** depending on URL shape:

**Mode A - Thread mode** (URL contains `/p[TIMESTAMP]`):
```
https://[workspace].slack.com/archives/[CHANNEL_ID]/p[TIMESTAMP_NO_DOT]
```
Extract:
- `channel_id` - the part after `/archives/`
- `message_ts` - the part after `p`, with a `.` inserted before the last 6 digits (e.g. `p1779816169638059` → `1779816169.638059`)

Fetch via:
```
mcp__slack__slack_read_thread(channel_id="...", message_ts="...")
```

**Mode B - Conversation mode** (URL has no `/p[TIMESTAMP]`, just `/archives/[ID]`):

Fetch ~30-50 recent messages via:
```
mcp__slack__slack_read_channel(channel_id="...", limit=50)
```

Then **inspect the response to determine destination type**:
- If `channel_info.is_dm` is true, or the response identifies it as "Group DM" → **DM or Group DM**: proceed with conversation review (this is the intended use case for conversation mode)
- If it's a **public or private channel** (named channel with members, not a DM) → **refuse and redirect**: tell the user this skill doesn't sweep channels, recommend `scan slack` for commitment extraction or `slack report` for activity sweeps. Channel sweeps need different framing (commitments, activity) than this skill produces (positions, alignment, draft).

**Expand in-conversation threads:**

In DMs and group DMs, participants often start sub-threads on individual messages. When fetching in conversation mode, scan the response for any message marked with "Thread: N replies" (or similar indicator). For each, fetch the thread via `slack_read_thread(channel_id, message_ts)` and weave the replies into the position mapping in Step 5.

In thread mode (Mode A), there is no equivalent step - the thread is already the unit of review.

### Step 2: Establish the participant set

Before mapping positions or drafting, identify who is a **member of this thread** versus who is merely referenced. This filter is load-bearing - it determines who can legitimately be tagged for alignment.

**Members of the thread** (qualify for alignment asks):
- Anyone who has posted at least one message in the thread
- Anyone @-mentioned **as a direct address** ("@person, what do you think?", "@person - your call")
- The direct recipient(s) of a DM or group DM

**Not members** (do NOT qualify, even if they have strong views):
- People @-mentioned in **narrative context** describing prior events ("there was a discussion between @X and @Y last week", "@X raised this in an earlier thread")
- People referenced by name without an @-mention
- People whose views are quoted or paraphrased but who aren't part of *this* conversation

**The narrative vs direct-address heuristic**: if the @-mention appears inside a sentence describing something that already happened, treat as referenced-not-member. If it appears as a direct address asking for or expecting a response, treat as a member. When in doubt, err conservative and don't tag.

Output a short participant list internally before proceeding (it doesn't need to appear in the final review unless useful):
- Members: [names]
- Referenced but not members: [names]

### Step 3: Load voice and style memory

Before drafting any response, read these five memory files in full. Do not rely on the MEMORY.md index alone - the index lists titles but not content, and drafting requires the actual guidance:

1. `/Users/smallc/.claude/projects/-Users-smallc-AI-Chief-of-staff/memory/user_writing_style.md` - voice, sentence shape, tone
2. `/Users/smallc/.claude/projects/-Users-smallc-AI-Chief-of-staff/memory/user_leadership_signature.md` - data honesty, ground-optimism framing
3. `/Users/smallc/.claude/projects/-Users-smallc-AI-Chief-of-staff/memory/user_feedback_style.md` - coaching-via-questions, outcome-oriented
4. `/Users/smallc/AI/Chief_of_staff/Work/LLM_Context/Personal/strategic_working_style.md` - PLG lens, experiment-first, guardrails over directives
5. `/Users/smallc/.claude/projects/-Users-smallc-AI-Chief-of-staff/memory/feedback_commissioner_consultant.md` - set outcome/constraints vs slide into tactics

If a file doesn't exist, skip it and note which were unavailable in the output.

### Step 4: Decode reactions and emojis as signal

Reactions are first-class signal, not noise. For every message in the thread, inspect reactions and interpret:

- **Standard emojis in context**:
  - `100` (💯) - strong endorsement / "spot on"
  - `agree` / `+1` / `thumbsup` - explicit agreement
  - `raised_hands` (🙌) - celebratory agreement / "let's go"
  - `eyes` (👀) - noted / watching / "I've seen this"
  - `thinking_face` (🤔) - skeptical or processing
  - `pray` (🙏) - thanks / please
  - `dart` (🎯) - on target
- **Custom workspace emojis** (e.g. `:agree:`, `:disagree:`): the name *is* the meaning. Custom emojis exist because the workspace wanted a more deliberate signal than standard ones - weight accordingly.
- **Combinations matter**: two reactions from one person (e.g. `100` + `agree`) is a stronger signal than one.
- **Source seniority matters**: a reaction from the most senior person in the thread is a stronger signal than from a peer. Carl Christensen reacting carries more weight than a peer reacting.
- **Absence matters**: if a key participant didn't react to a summary or position post, flag it as unresolved alignment, not assumed alignment.
- **Don't strip emoji-only replies** - they often carry the actual decision signal in leadership threads.

### Step 5: Map the conversation

Build a mental model of:
- **Topic**: what is being discussed and why it matters
- **Origin**: who posted the opener, when, what they were asking for
- **Trajectory**: how the discussion has evolved - has it converged, diverged, stalled, or escalated?
- **Positions**: per participant, what they've argued, where they shifted, what they last said
- **State**: open debate / converged / stalled / awaiting action / dead
- **Loose threads**: questions raised but not answered, asks not yet responded to

In **conversation mode**, the position mapping spans the parent messages and any expanded in-conversation threads (per Step 1). Treat sub-threads as part of the conversation, not as separate topics - their content informs the participant's overall position.

### Step 6: Recommend a next move

Pick ONE concrete next action. Resist listing options - the value is in the recommendation. Typical moves:

- **Post a closing message** - debate has converged, time to land the position
- **Post a check-in** - ask remaining participants for explicit alignment or pushback
- **Escalate to a meeting** - too much disagreement or nuance for async
- **Assign an owner** - convert agreement into a concrete deliverable with a date
- **Let it die** - thread no longer needs Chris's input

Briefly explain *why this move and not the others*, in one or two sentences. This is where rationalisation belongs - not in the draft response itself.

### Step 7: Draft the response

**Two-filter rule for alignment asks**: a person should only be tagged for alignment if BOTH conditions are true:

1. **They are a member of the thread** (per Step 2)
2. **They have an unresolved point of view that needs addressing** - they've posted a position that hasn't been signed off, raised a question that hasn't been answered, or are in a role where their input is required for the decision to land

Members with no relevant POV do not get tagged. Non-members with strong views do not get tagged. Both filters must pass.

Example application (FSM thread):
- Member who already signalled alignment via reactions → don't re-tag
- Member with an unanswered question → tag
- Member with an unsigned POV → tag
- Non-member referenced in narrative → never tag, regardless of views

**Default to curiosity before counter-position.** When the draft is responding to a position someone has stated in the thread - especially one Chris doesn't fully agree with - the first move should be a question that surfaces their reasoning ("why do you feel...?", "help me understand...", "can you give me more context on this point?"), not a counter-argument. Pair with an empowerment move where appropriate ("happy to defer if...", "happy to be a contributor if..."). Counter-positions belong in follow-up messages once the reasoning is on the table. See `feedback_curiosity_before_position` memory.

**Default: succinct.** Match the thread's depth - short threads get short replies, dense threads can carry layered reasoning, but lean short. Add rationalisation only when the topic's complexity genuinely warrants it (e.g. the position is non-obvious, the audience is skeptical, or precedent is being set).

Voice rules (from loaded memory files):
- Empowerment tone, not directive
- Stream-of-consciousness OK for thinking-out-loud posts, tighter for closing/decision posts
- Practical over theoretical
- Ground optimism in data honesty - if numbers are quoted, source precision matters
- Coaching via questions where appropriate - don't always close down debate, sometimes open it
- Commissioner over consultant: set outcome and constraints, don't prescribe tactics

Format rules:
- Sentence case for any inline headings
- No em dashes - use regular hyphens or restructure
- Markdown: `**bold**`, `_italic_`, bullet points where they help scannability

**Always append this disclaimer footer** to the draft, italicised and separated by a blank line:

```
_Drafted with Claude. If the tone misses, that's the robot. Read for intent._
```

This footer is non-negotiable - it goes on every draft pushed via this skill. It signals AI assistance, owns the substance, and lets readers calibrate if the wording lands awkwardly.

### Step 8: Present the four-section review

Output in this exact order:

```markdown
## Topic
[1-3 sentence summary of what the thread is about and the current state]

## Positions
- **[Person 1]**: [what they argued, including any shift] [emoji signal if relevant]
- **[Person 2]**: [...]
- **[Person 3]**: [...]

## Recommended next move
[One concrete action + one or two sentences on why this and not the alternatives]

## Draft response
> [the draft, formatted as it would appear in Slack]
>
> _Drafted with Claude. If the tone misses, that's the robot. Read for intent._
```

### Step 9: Offer to push the draft into Slack

Always offer. Ask:

> Push this as a draft into the thread? (**y** / **edit** / **n**)

- **y** → call `mcp__slack__slack_send_message_draft(channel_id=..., message=..., thread_ts=...)` where `thread_ts` is the parent message's timestamp. Return the channel link.
- **edit** → accept inline edits in the terminal, re-show the updated draft, ask again.
- **n** → leave it as terminal-only. User copy-pastes if they want.

**Handle `draft_already_exists`**: if the API returns this error, do not retry or overwrite. Surface to the user:

> You already have a draft in this channel. Resolve it in Slack first (send, edit, or delete), then re-run.

Drafts are user state. Silently clobbering them erodes trust.

### Step 10: Optional - save the review

If the thread is significant (leadership-level decision, strategic discussion, contested topic), offer to save the review to `Work/Notes/Threads/[topic_slug]_YYYY-MM-DD.md`. Default to *not* saving unless the user asks or the topic is clearly load-bearing.

## Guidelines

- **Detect URL mode first** - thread URLs have `/p[ts]`, conversation URLs don't; refuse and redirect for public/private channels without a thread anchor
- **Read the full thread or conversation before drafting** - never draft from the opener alone; in conversation mode, expand any in-conversation sub-threads
- **Establish membership before mapping positions** - the participant filter determines who can legitimately be tagged for alignment
- **Two filters for alignment asks** - tag only if (a) member of the thread/conversation AND (b) has an unresolved POV that needs addressing
- **Decode emojis explicitly** - if a senior person used `100` + `agree`, name it in the positions section
- **One recommendation, not three** - the value is in the call, not the menu
- **Succinct draft is the default** - rationalise only when complexity warrants
- **Always append the Claude disclaimer footer** - non-negotiable on every drafted response
- **Never auto-send** - always show the draft, always require explicit `y` to push as a draft, and even then it's just a draft (user sends from Slack)
- **Flag what you couldn't load** - if any voice memory file was missing, say so in a footer
- **Match conversation tone** - if it's casual, the draft should be casual; if it's a formal leadership decision, the draft should be tighter

## What this skill is NOT for

- Sweeping multiple channels for activity (use `scan slack` / `slack report`)
- Reviewing a public or private channel via its URL (refuse and redirect - see Step 1 Mode B)
- 4Ps post threads specifically (use `4ps roundup`)
- DMs in the context of preparing for a 1:1 (use `121-prep`)
- Sending messages directly without a thread context (use `m365` / `slack` tools directly)
