# Review strategy skill

## Purpose

Review a strategy document against best practice criteria. Evaluates quality regardless of document format - the goal is to identify gaps and suggest improvements while preserving author agency.

## Trigger phrases

- `review strategy: [document path]`
- `strategy review: [document path]`
- `review strategy: [document path] feedback` (includes feedback draft)
- `review strategy: [document path] against [data file]` (cross-references data)

## Process

### 1. Read inputs

- Read the strategy document at the specified path
- Read the review framework from `Work/LLM_Context/strategy_review_framework.md`
- If data file specified, read that for cross-referencing

### 2. Evaluate against framework

For each section of the framework, assess:

**Section 1: Strategy foundations**
- Is ONE primary user clearly defined?
- Is business impact tied to a specific metric?
- Is the business situation grounded in data?

**Section 2: Problem spaces**
- Is there a clear trunk problem?
- Are branch problems identified?
- Do problem statements pass quality criteria:
  - Observable (not assumed motivation)
  - Measurable (has data)
  - Solution-free (no product words)
  - User language (not internal jargon)
- Apply the "3 solutions" test

**Section 3: Customer value**
- Is tangible user value articulated?
- Is it framed from user perspective, not features?

**Section 4: Strategic direction**
- Is mission clear (why this exists)?
- Is scope defined (in and out)?
- Is destination described with metrics?
- Are baselines and targets specified?
- Are kill criteria defined?

**Section 5: Solution spaces**
- Are key capabilities identified?
- Are bets directional (not prescriptive solutions)?
- Are bets prioritized (Now/Next/Later)?
- IF experiments included:
  - Do hypotheses use "We believe..." format?
  - Are hypotheses falsifiable and user-framed?
  - Do predictions use "If... then..." format?
  - Are outcomes measurable?

**Section 6: Risks and dependencies**
- Are blockers identified?
- Are team dependencies called out?

### 3. Cross-reference data (if provided)

- Check data accuracy (do claims match source?)
- Identify data insights not leveraged
- Note patterns that could inform strategy

### 4. Produce output

## Output format

### Assessment summary

[2-3 sentences on overall quality - what's strong, what needs work]

### Section-by-section review

| Section | Assessment | Key finding |
|---------|------------|-------------|
| Foundations | ✅/⚠️/❌ | [Brief finding] |
| Problem spaces | ✅/⚠️/❌ | [Brief finding] |
| Customer value | ✅/⚠️/❌ | [Brief finding] |
| Strategic direction | ✅/⚠️/❌ | [Brief finding] |
| Solution spaces | ✅/⚠️/❌ | [Brief finding] |
| Risks & dependencies | ✅/⚠️/❌ | [Brief finding] |

[Detailed findings for each section with specific examples from the document]

### Key gaps and why they matter

Focus on 2-3 highest-leverage improvements:

1. **[Gap]** - [Why it matters for strategy quality]
2. **[Gap]** - [Why it matters for strategy quality]
3. **[Gap]** - [Why it matters for strategy quality]

### Data utilization (if data provided)

| Data insight | Strategic implication | Used in strategy? |
|--------------|----------------------|-------------------|
| [Insight] | [Implication] | ✅/❌ |

### Checklist results

```
FOUNDATIONS
[✅/⚠️/❌] One primary user defined
[✅/⚠️/❌] Business impact clear
[✅/⚠️/❌] Business situation grounded in data
...
```

### Suggested feedback (if requested)

Draft Slack/email message that:
- Opens with what's working (1-2 specific strengths)
- Frames feedback as building on good work
- Focuses on 2-3 high-leverage shifts
- Provides concrete asks for each
- Offers support
- Uses "I'd like..." framing (collaborative, not critical)

## Key principles

### Evaluate quality, not format
The author may not have followed the template exactly. That's fine. Look for whether the essential elements are present and well-formed, regardless of structure.

### Acknowledge what's working
Every strategy has strengths. Identify them first. This creates psychological safety and shows you're not dismissing the work.

### Explain why gaps matter
Don't just flag missing elements - explain the strategic impact. "Customer value is missing" is less useful than "Without customer value, we can't answer whether this is worth pursuing."

### Frame constructively
The goal is to help authors improve, not to make them feel everything is wrong. Focus on 2-3 high-leverage shifts rather than 10 issues.

### Distinguish user problems from business problems
A common failure mode is strategies that solve the business's problem (acquisition, activation) without articulating the user's problem. Flag this distinction.

### Check hypotheses vs predictions
"By doing X, we'll achieve Y" is a prediction about a solution. "We believe [user behavior/need]" is a hypothesis that can be tested multiple ways. The latter is more valuable for learning.

## Examples

### Trigger
```
review strategy: Work/Notes/ACC onramp/validating_acc_onramp_strategy.md against Work/Notes/ACC onramp/acc_data.md feedback
```

### Output includes
- Full section-by-section assessment
- Data cross-reference showing which insights are/aren't used
- Slack-ready feedback message

## Related files

- Framework: `Work/LLM_Context/strategy_review_framework.md`
- Confluence template: Search "Strategy document" in Confluence (Forma Design space)
- Problem statements guide: `Work/LLM_Context/PLG and experimentation/crafting_problem_statements_best_practice.md`
- Experimentation criteria: `Work/LLM_Context/PLG and experimentation/experimentation_overview.md`
