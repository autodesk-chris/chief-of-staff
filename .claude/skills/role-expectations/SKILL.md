---
name: role-expectations
description: >
  Create a role expectations document for a team member or squad lead. Two
  sections: executive summary (the destination) and detailed expectations with
  What/Key activities/Expectations format. Use when "role expectations for
  [name]", "/role-expectations [name]", or "create expectations for [name]".
---

# Role Expectations Document Generator

Create a role expectations document for a team member or squad lead.

## Arguments

- **person**: Name of the person (required)
- **squad**: Squad or area they lead (optional)

## Process

### Step 1: Gather context

Search for existing information about {{person}}:

1. **121 folder**: `Work/People/121s/{{person}}/` - notepad, recent meeting notes
2. **Merged notepad**: `Work/1-Notepad/Notepad.md` - search for mentions of {{person}} or their squad
3. **Strategy-memory**: `/Users/smallc/AI/forma-agentic-memory-strategy/` - relevant OKRs, objectives, bets
4. **Granola meetings**: Query for recent meetings with {{person}} about their area of focus

Present a summary of what you found before proceeding.

### Step 2: Ask clarifying questions

Before drafting, ask the user:

1. What is the primary mission/focus for {{person}}?
2. What does success look like in 6 months?
3. What autonomy level should they have?
4. Any specific blockers, constraints, or context to include?
5. What tone - outcome-focused, task-oriented, or balanced?

### Step 3: Generate document

Create a two-section document:

**Section 1: The destination (executive summary)**

```markdown
# The destination

## Why we're doing this
[Strategic context - why this squad/role matters]

## What success looks like
[3-5 outcome statements - what's true when we've succeeded]

## The focus
[Key principles/priorities - what to optimize for]

## How I expect you to work
[Autonomy level, experimentation expectations, communication]

## My role
[What support the user will provide]
```

**Section 2: Detailed expectations**

For each responsibility, use this format:

```markdown
### [Responsibility name]

**What**: [One sentence describing ownership]

**Key activities**:
- [Specific deliverable or action]
- [Another deliverable]

**Expectations**: [How to approach it, quality bars, principles to follow]
```

Include:
- Current state data from meetings (metrics, blockers, decisions)
- Known blockers and constraints
- Operating principles section at the end

### Step 4: Iterate

Show the draft to the user. Expect 2-3 rounds of refinement:
- Adjust tone and emphasis based on feedback
- Add/remove sections as needed
- Incorporate specific examples or context

### Step 5: Save

Save to: `Work/People/121s/{{person}}/{{person}}_expectations_[area].md`

Confirm with user before saving.

## Key principles

- **Destination over tasks**: Lead with outcomes, not to-do lists
- **Real data**: Include actual metrics, blockers, context from meetings
- **Prove the motion**: Focus on learning/proving vs hitting arbitrary targets
- **High autonomy + alignment**: Clear guardrails, not micromanagement
- **Test assumptions**: Call out hypotheses to validate

## Example output structure

```
# The destination
  - Why we're doing this
  - What success looks like
  - The focus
  - How I expect you to work
  - My role

---

# Detailed expectations
  - [Responsibility 1] - What / Key activities / Expectations
  - [Responsibility 2] - What / Key activities / Expectations
  - ...
  - Operating principles
```

## Reference

This skill was created based on the Maria PLG Monetisation role expectations document. See `Work/People/121s/maria/Maria_expectations_pm_monetization.md` for a complete example.
