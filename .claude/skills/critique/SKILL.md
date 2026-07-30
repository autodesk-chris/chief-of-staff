---
name: critique
description: Get an independent, fresh-eyes critique of a draft or output by spawning a general-purpose agent with no prior conversation context. Reads the current conversation to identify the draft, the trigger material, the user's substantive positions, and any private/holding decisions, then builds a self-contained brief and gets structured critique against a standard seven-question framework. Returns critique, not a rewrite. Use when "critique this draft", "critique this message", "critique the reply", "critique the post", "critique:", "fresh review", or similar. Most useful when Claude has been deep in drafting with the user so Claude's own read is anchored - the fresh agent catches what Claude won't.
---

# Critique skill

## When to use

After substantive collaborative work on a high-stakes outbound piece (Slack reply, email, Confluence page, board update, decision doc) where Claude has been deeply involved in drafting. Claude's perspective is now anchored; a fresh agent with no shared history catches things Claude won't.

Don't use for routine reviews where self-judgement is enough, or for work too informal to warrant the overhead.

## Workflow

### 1. Read the conversation

Extract the following. If anything is genuinely unclear, ask the user before proceeding - do not invent.

- **The draft or output.** The substantive piece the user is preparing to send, publish, or share. May be inline or in a file just written.
- **The trigger material.** What the draft responds to or addresses - a Slack post, an email, a brief, a decision being made. Usually pasted or referenced earlier.
- **Supporting context.** Other inputs that bear on the draft - team feedback, prior threads, source documents, observations.
- **Substantive positions.** Stated views, arguments, evidence the user is making in or behind the draft. The case being made.
- **Private/holding decisions.** Things the user has explicitly chosen NOT to surface - "I'll hold this", "don't deploy that", defensive instincts the user has agreed to suppress, existential or sensitive context kept out of the visible output. Tag these clearly in the brief so the agent treats them as boundaries, not measurement criteria.

### 2. Build a self-contained brief

The brief must stand alone - the agent has no prior context. Paste source material verbatim; don't paraphrase. The agent's value depends on forming an independent read of primary text.

### 3. Spawn the agent

Agent tool, subagent_type=general-purpose, foreground unless the user is working in parallel.

### 4. Return the critique

Summarise findings to the user. Include:
- Headline verdict (send / send with edits / hold pending)
- Specific edits identified
- Anything Claude missed that the agent caught - be honest; this is the skill's value
- Anything Claude called right that the agent confirmed
- Where the agent's judgement seems questionable, flag it. Fresh-eyes is not gospel.

Then ask the user what they want to do next. Don't auto-update the draft.

## Agent brief template

Fill the bracketed sections from the conversation.

```
You are giving an independent, critical review of a draft that [USER ROLE] intends to [SEND/POST/SHARE] [WHERE]. You have no prior context with them; that's deliberate - I want a fresh outside read.

# THE SITUATION
[2-4 sentences: who's involved, platform, what's prompting the message, what's at stake. Include role/relationship context the recipient already has.]

# TRIGGER MATERIAL
[Raw quote of what's being responded to. If multiple sources, include them all.]

# SUPPORTING CONTEXT
[Other inputs bearing on the draft, quoted verbatim.]

# USER REFLECTIONS
Tag legend:
- SUBSTANTIVE: positions and case the user is making. Use to understand intent.
- PRIVATE/HOLDING: deliberate choices about what NOT to surface. Do NOT measure the draft against them; FLAG if any leak into the visible draft.

[List each reflection with tag and one-line description.]

# THE DRAFT
[Paste verbatim.]

# WHAT I WANT FROM YOU

Critical, independent review. Do NOT rewrite the message - analysis, not a competing draft. Use SUBSTANTIVE reflections to understand intent; treat PRIVATE/HOLDING reflections as boundaries that must not leak.

Address these seven questions in order. Be specific - reference exact phrases when you critique.

1. **Does the draft meet the bar?** If the trigger material set a standard or question explicitly, does the draft answer it with evidence rather than assertion? If no explicit bar, what implicit bar should this draft be meeting?

2. **Tone audit.** Paragraph by paragraph. Where does it sound defensive, accusatory, point-scoring, or like positioning rather than engaging? Where does it land as a genuine peer / colleague / appropriate-tier response?

3. **What's missing.** Anything in supporting context that materially changes the picture but isn't in the draft? Anything in the trigger material not answered? Anything specific the trigger raised that the draft sidesteps?

4. **What's over-claimed.** Where is the draft asserting more than the evidence supports? Convert any categorical claims back to what the underlying evidence actually said.

5. **Structural moves.** Asks, commitments, escalations, pushbacks - do they land as partnership / accountability / curiosity moves, or as complaints / accusations / positioning?

6. **One cut, one add.** Single weakest line or paragraph to cut. Single most important thing to add.

7. **Leak check** (only if PRIVATE/HOLDING items exist). Does anything in the draft reveal or imply them? Flag explicit leaks AND leaks-by-avoidance (silence on a topic that itself reveals a held position).

End with a one-paragraph overall verdict: send as-is, send with specific edits (name them), or hold pending more work (say what work).

Be direct. The user values pushback over false agreement. If the draft is mostly good, say so plainly and focus on what's not. If it has a fundamental problem, say that first.
```

## Constraints

- **Critique, not rewrite.** The agent must not return a competing draft. User owns the writing; agent's job is analysis only.
- **Private/holding items are boundaries, not criteria.** The agent may flag leaks; it must not say "you should have included this" about a held item.
- **Be honest about anchoring.** When reporting back, name where the critique caught something Claude missed.
- **Don't auto-fetch.** Skill works from what's in the conversation. If the user references material not in the conversation, ask them to paste it. Keeps the skill portable across projects.
- **One agent per critique.** Pattern depends on a single independent read.

## Not in scope

- Rewriting the draft (user owns the writing)
- Auto-fetching external sources (user pastes)
- Replacing user judgement on substantive vs private tagging (skill scaffolds discipline; user provides judgement)
- Quality scores or rubrics (returns specific edits and a verdict, not a grade)
