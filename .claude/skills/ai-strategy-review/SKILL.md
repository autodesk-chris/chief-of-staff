---
name: ai-strategy-review
description: >
  Review a team's AI productivity strategy against the Forma Design framework.
  Evaluates experiment feasibility, daily behaviour change, success criteria quality,
  constraint clarity, and framework compliance. Optionally incorporates a Granola
  call transcript for richer context. Produces a full review and a shareable summary
  with actions. Use when "review ai strategy: [team]", "ai strategy review: [team]",
  or when given a Confluence URL to an AI productivity strategy page. NOT for
  product/domain strategies (use review-strategy). NOT for cross-team comparison
  (use ai-strategy-compare).
---

# AI productivity strategy review

Review a team's AI productivity strategy against the "what to expect" framework and the "Moving to Agentic-First" principles. Produces two outputs: a full review (for you) and a shareable summary with actions (for the team).

## Trigger phrases

- `review ai strategy: [team name]`
- `ai strategy review: [team name]`
- `review ai strategy: [Confluence URL]`

## Reference documents (baked in)

These are the standards every strategy is evaluated against:

- **Framework:** Confluence page 816462938 - "Your team's AI productivity strategy - what to expect"
- **Principles:** Confluence page 801739348 - "Moving to Agentic-First: What It Means for Forma Design"

Key framework requirements (5 sections):
1. Current state - what the team does, where friction is
2. Activities mapping - automated / augmented / accelerated categorization
3. Constraints needing leadership help - tools, licenses, cross-squad, policy
4. Safe-to-try experiments - concrete things to run within timeframe
5. Signal - how we'll know it's working (team-level observation at 3 months, not a corporate KPI)

Key principles from the VP announcement:
- "Start with agents" - every task, agent-first by default
- "Fix the process, not the workaround" - improve the agentic workflow, not the manual fallback
- "Constraints will surface. That's the point" - expose bottlenecks, escalate fast
- "You are still accountable" - agent use doesn't delegate ownership
- This is about how teams operate together, not individual productivity

## Process

### Step 1: Find and fetch the strategy

**If team name provided:**
1. Search Confluence: `space = "fdo" AND title ~ "[team] AI Productivity Strategy" AND type = "page"`
2. Fetch with `contentFormat: markdown`
3. If no match, list available AI productivity strategies and ask user to clarify

**If Confluence URL provided:**
1. Extract page ID and fetch directly

### Step 2: Evaluate against six dimensions

For each dimension, score as Strong / Adequate / Needs work, with specific examples from the document.

#### D1: Framework compliance
- Does it have all 5 sections?
- Are sections substantive or placeholder?
- Are open questions and disagreements preserved honestly?

#### D2: Experiment feasibility
- Are experiments achievable within the stated timeframe?
- Does the team have the technical capability to build what they're proposing?
- Is there a gap between ambition and ability? (e.g. a non-technical team proposing a multi-agent architecture)
- Are experiments "safe-to-try" or disguised software projects?
- Do experiments have clear owners?

#### D3: Daily behaviour change
- Does the strategy describe how the team will work differently day-to-day?
- Is there a personal adoption path - who's already using agents, who needs support?
- Or does it only describe future systems to build?
- Does it address the "start with agents" principle for everyday tasks?

#### D4: Success criteria quality
- Are signals observable and concrete?
- Could you actually tell in 3 months whether it worked?
- Or are they aspirational percentages with no baseline? ("80% less time" - against what?)
- The framework says "a team-level observation at 3 months, not a corporate KPI"

#### D5: Constraint clarity
- Are blockers specific (tool name, what's missing, who owns it)?
- Are they categorized: things the team can solve vs things needing leadership help?
- Are there constraints the team is absorbing silently that should be escalated?

#### D6: Current progress
- Has the team already started any experiments?
- Does the doc reflect reality or just intent?
- Is there evidence of actual agent usage in the team?

### Step 3: Optionally incorporate call context

Ask: **"Was there a discussion call about this strategy? If so, what's the meeting name in Granola?"**

If yes:
1. Search Granola for the meeting
2. Fetch the transcript
3. Cross-reference: what came up in discussion that isn't in the doc?
4. Note any context that changes the assessment (e.g. team is further along than doc shows, political blockers not captured, fear/adoption dynamics)

If no: proceed with doc-only review.

### Step 4: Produce output

Save two files to `Work/Notes/AI_development/Squad strategies/`:

#### File 1: Full review
Filename: `{team}_ai_strategy_review_{date}.md`

```markdown
# [Team] AI productivity strategy - review and guidance

## TLDR
[3-4 sentences: what's strong, what needs to change, highest-value actions]

---

**Date:** [date]
**Strategy owner:** [from doc]
**Reviewed against:** "Your team's AI productivity strategy - what to expect" framework + "Moving to Agentic-First" principles

---

## Dimensional assessment

| Dimension | Score | Key finding |
|-----------|-------|-------------|
| Framework compliance | Strong/Adequate/Needs work | [Brief] |
| Experiment feasibility | Strong/Adequate/Needs work | [Brief] |
| Daily behaviour change | Strong/Adequate/Needs work | [Brief] |
| Success criteria | Strong/Adequate/Needs work | [Brief] |
| Constraint clarity | Strong/Adequate/Needs work | [Brief] |
| Current progress | Strong/Adequate/Needs work | [Brief] |

## What's working
[Bullet points - specific strengths with examples from the doc]

## Where it falls short
[Numbered sections with detail - specific gaps, why they matter, what to do instead]

## Call takeaways (if call transcript available)
### Context the strategy document doesn't capture
[Bullet points - things said in discussion not reflected in the doc]

### What this changes about the guidance
[Numbered points - how the call context modifies the doc-only assessment]

## Guidance for the team
### Core message
[One sentence framing]

### Specific prompts
[Numbered actionable recommendations]
```

#### File 2: Shareable summary
Filename: `{team}_ai_strategy_call_summary_{date}.md`

```markdown
# [Team] AI strategy - call summary and next steps

**Date:** [date]
**Attendees:** [from call or "Strategy review"]

---

## Summary
[2-3 sentences on overall quality and direction]

---

## Key takeaways
[3-5 bullet points - direct, actionable, building on what's working]

---

## Actions

| What | Who | By when |
|------|-----|---------|
| [Action] | [Owner] | [Timeline] |
```

## Evaluation principles

### Build on energy, don't dampen it
Teams that produced a strategy are already engaged. The goal is to sharpen focus, not criticize effort. Always lead with what's working.

### Be specific about feasibility
"This is too complex" isn't useful. "This is a three-agent architecture that needs an engineer to build - could you get the same value by putting messaging in one Confluence page and having Claude review copy against it?" is useful.

### Distinguish capability gap from ambition gap
A non-technical team proposing to build a multi-agent system has a capability gap. A technical team proposing incremental automation has an ambition gap. Different feedback for each.

### Respect the fear dimension
Some teams have members who are scared AI will cost them their job. If the call reveals this, adjust guidance accordingly - push adoption through safe mechanisms (office hours, voluntary sharing) not mandates.

### Connect to what the team can actually do next
Every piece of guidance should end with a concrete next step the team can take this week or this month. Abstract advice ("be more agentic") is worthless.

### Flag escalation opportunities
If the team has blockers that need leadership help, explicitly note what Chris should escalate and to whom. This is often the highest-value action.
