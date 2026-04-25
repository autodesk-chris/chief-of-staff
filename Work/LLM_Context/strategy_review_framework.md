# Strategy review framework

This framework evaluates strategy documents against best practice criteria. It assesses quality regardless of document format - the goal is to identify gaps and suggest improvements, not enforce template compliance.

## Sources

- Confluence strategy template (Forma Design operating model)
- Crafting problem statements best practice
- Experimentation overview (hypothesis and prediction criteria)

---

## 1. Strategy foundations

### Criteria

| Element | What good looks like |
|---------|---------------------|
| **User focus** | ONE primary user clearly defined. If in-market, the ideal user (or subset). Strategy should win disproportionately for this user. |
| **Business impact** | Clear company-level metric or outcome being moved. |
| **Business situation** | Data points that help understand current state. Grounded in reality, not assumptions. |

### Review questions

- Is there a single user this strategy wins for?
- Can we identify them in our data?
- What metric moves if this succeeds?
- Is the context grounded in actual data?

---

## 2. Problem spaces

### Structure criteria

| Element | What good looks like |
|---------|---------------------|
| **Trunk problem** | The big meaningful problem for the target user. One clear, significant problem articulated. |
| **Branch problems** | 2-3 problems blocking delivery of trunk problem. Connected to outcomes/key results. |
| **Supporting evidence** | Data points that justify why the problem exists. |

### Problem statement quality criteria

Each problem statement must pass ALL of these:

| Criterion | What good looks like | Red flags |
|-----------|---------------------|-----------|
| **Observable** | Describes what users ARE or AREN'T doing | Assumes motivation ("reluctant", "don't understand", "confused") |
| **Measurable** | Can be validated with data | Vague terms ("low", "poor", "not enough") |
| **Solution-free** | No product words or mechanisms | Contains product names, feature names, UI elements |
| **User language** | Uses user's words, not product jargon | Contains internal terms ("activation", "retention", "on-ramp", "funnel") |

### Goldilocks test

| Level | Example | Verdict |
|-------|---------|---------|
| **Too broad** | "Users don't find value in early-stage design tools" | ❌ Unmeasurable, no clear gap |
| **Too narrow** | "The navigation link between products is hard to find" | ❌ Solution embedded (specific UI element) |
| **Just right** | "Most users working on construction documentation never explore site design options - only 2.3% try more than one approach in their first month" | ✅ Observable, measurable, solution-free, user-framed |

### Ultimate test

> Hand the problem statement to a team with zero context. Ask: "Can you brainstorm 3 totally different ways to solve this?"
> - If yes → problem is well-defined
> - If no → you've defined a solution, not a problem

---

## 3. Customer value

### Criteria

| Element | What good looks like |
|---------|---------------------|
| **Value statement** | Tangible value users gain if trunk problem is solved. Expressed in practical, outcome-oriented terms. |
| **User-centric framing** | Described from user perspective, not product perspective. Avoids feature language. User could say "yes, that's what I want." |

### Examples

| Type | Example | Verdict |
|------|---------|---------|
| **Good** | "Architects can test site layouts against real constraints before committing to detailed design, reducing rework downstream" | ✅ User role, user goal, user outcome |
| **Bad** | "Users get access to Board's collaboration features and real-time analysis tools" | ❌ Feature language, product names |

---

## 4. Strategic direction

### Criteria

| Element | What good looks like |
|---------|---------------------|
| **Mission** | 1-2 sentences on why this strategy exists and the enduring value it creates. Clear purpose that someone outside the team would understand. |
| **In-scope** | Product set, geographies, on-ramps, user journey stage clearly defined. |
| **Out of scope** | Explicit about what this strategy will NOT do. What success does NOT look like. |
| **Outcomes** | Changes in behavior and key results, aligned to strategic outcomes. Defined as behavior changes, not feature delivery. |
| **Destination** | The endgame that defines when strategy is complete. Clear picture of success with metrics. |

### Metrics criteria

| Element | What good looks like |
|---------|---------------------|
| **3-5 key metrics** | Specific metrics identified to track progress. |
| **Baselines defined** | Current values stated - where we're starting from. |
| **Targets specified** | Clear targets to achieve. |
| **Kill criteria** | Threshold that would make us stop investing. |

---

## 5. Solution spaces

### Criteria

| Element | What good looks like |
|---------|---------------------|
| **Key capabilities** | Levers or moats we must be excellent at. Things competitors would struggle to replicate. |
| **Bet solution space** | Areas we plan to leverage to solve problems. Directional without being overly prescriptive on specific solutions. |

### Bets criteria

| Timeframe | What to include |
|-----------|-----------------|
| **Now** (0-3 months) | Immediate focus areas |
| **Next** (3-6 months) | Follow-on priorities |
| **Later** (6-12 months) | Future direction |

Bets can be as simple as a single line describing what's being proposed.

| Type | Example | Verdict |
|------|---------|---------|
| **Good** | "Guide users to design tasks relevant to their current project work" | ✅ Directional, outcome-oriented |
| **Bad** | "Improve the ACC module switcher entry flow" | ❌ Specific UI/feature solution |

### Experiment evaluation (apply only if bet includes an experiment)

#### Hypothesis quality

| Criterion | What to check |
|-----------|---------------|
| **User perspective** | Stated from user's POV, not product perspective |
| **Belief statement** | Uses "We believe..." - avoids solution framing |
| **Problem space aligned** | Connects to supporting data |
| **Falsifiable** | Can be definitively validated or refuted with measurable outcomes |
| **Format** | No "if/could/should" in the belief statement |

#### Hypothesis examples

| Type | Example | Verdict |
|------|---------|---------|
| **Bad** | "We believe we should improve the entry flow" | ❌ Solution, not belief |
| **Bad** | "We believe users would benefit from better onboarding" | ❌ Goal, not falsifiable |
| **Good** | "We believe users who navigate directly from active project work have higher intent than those responding to email prompts, because they are already in a working context" | ✅ User-framed, falsifiable, connected to behavior |

#### Hypothesis tests

1. Can the belief be proven false?
2. Is it written as a belief, not a solution/goal?
3. Does it connect to the root cause?
4. Is it logically supported by evidence?

#### Prediction quality

| Criterion | What to check |
|-----------|---------------|
| **Format** | Uses "If... then..." with clear condition and expected outcome |
| **Hypothesis connection** | Clearly validates or invalidates the belief |
| **Testability** | Outcome is observable and falsifiable |
| **Outcome-level framing** | Multiple solution variations could test it |

#### Prediction examples

| Type | Example | Verdict |
|------|---------|---------|
| **Bad** | "If we add profiling questions, users will convert better" | ❌ Solution-specific, vague outcome ("better") |
| **Good** | "If users are guided to design tasks relevant to their current project work, then the percentage who return within 30 days will increase from 31% to 45%" | ✅ Condition clear, outcome measurable, multiple solutions could test it |

#### Prediction tests

1. Is it written as "If... then..."?
2. Does it align with the hypothesis by testing its truth?
3. Can it be observed and proven false?
4. Could different solution variations be used to test it?

---

## 6. Risks and dependencies

### Criteria

| Element | What good looks like |
|---------|---------------------|
| **Risks** | Potential blockers identified. What could prevent progress. |
| **Dependencies** | Critical team dependencies called out. Cross-team alignment addressed. |

---

## Quick reference checklist

```
FOUNDATIONS
[ ] One primary user defined
[ ] Business impact clear (metric identified)
[ ] Business situation grounded in data

PROBLEM SPACES
[ ] Trunk problem articulated
[ ] Branch problems identified (2-3)
[ ] Problems are observable (not assumed motivation)
[ ] Problems are measurable (have data)
[ ] Problems are solution-free (no product/feature words)
[ ] Problems use user language (not internal jargon)
[ ] Another team could propose 3 different solutions

CUSTOMER VALUE
[ ] Value is tangible and outcome-oriented
[ ] Framed from user perspective, not features

STRATEGIC DIRECTION
[ ] Mission is clear (1-2 sentences)
[ ] Scope defined (in and out)
[ ] Destination described with metrics
[ ] 3-5 metrics with baselines and targets

SOLUTION SPACES
[ ] Key capabilities identified
[ ] Bet solution space is directional (not prescriptive)
[ ] Bets are prioritized (Now/Next/Later)
[ ] IF experiments: hypothesis uses "We believe...", is falsifiable, user-framed
[ ] IF experiments: prediction uses "If... then...", outcome is measurable

RISKS & DEPENDENCIES
[ ] Blockers identified
[ ] Critical team dependencies called out
```

---

## Output format for reviews

### 1. Assessment summary
Brief overall assessment - what's strong, what needs work.

### 2. Section-by-section review
For each framework section:
- What's present
- What's missing
- Quality assessment

### 3. Key gaps and why they matter
Focus on 2-3 most important issues and their strategic impact. Explain WHY each gap matters, not just that it exists.

### 4. Data utilization (if data provided)
- Cross-reference strategy claims against source data
- Identify insights in data not leveraged by strategy
- Flag any data discrepancies

### 5. Suggested feedback (if requested)
Constructive framing for sharing with author:
- Acknowledge what's working
- Frame improvements as building on good work
- Provide concrete asks
- Offer support
