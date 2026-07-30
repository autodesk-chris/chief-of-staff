# Monthly Focus Meeting (MFM) Review Framework

## Purpose of this document

This document provides the analytical framework for reviewing Monthly Focus Meeting pre-read documents. Use this as context when asking Claude to review MFM submissions from squads.

## Finding the Right MFM Document

### Source of truth

MFM documents live in Confluence (fdo space), inside the Growth and Adoption Product Area folder. Each squad has its own sub-folder. **Always fetch live from Confluence via the Atlassian MCP - do not save local copies.**

**CloudId:** `0e31f281-3568-4559-ae88-153abcdead38`

**Squad Confluence lookup:**

| Squad | Folder ID | Title pattern | Author(s) | CQL |
|-------|-----------|---------------|-----------|-----|
| Marketing | `722332003` | `{Month} 2026 – Squad Focus Meeting – Marketing` | Ben Storey | `ancestor = 722332003 AND type = page` |
| Strategic Accounts | `719586327` | `Strategic Accounts – {Month} Review` or `Strategic Accounts - {Month} Review` | Anders Wester | `ancestor = 719586327 AND type = page` |
| First Strike | `712784768` | `2026 {Month} Monthly Planning Meeting - Growth` (also `- SD FSM`, `- Board FSM`) | Even Olstad, Katarina Plavec | `ancestor = 712784768 AND type = page` |
| Monetisation | `856500256` | `NN_{Month} [Monthly] Focus Meeting` (e.g. `03_June Focus Meeting`) | Maria Chefneux | `parent = 856500256 ORDER BY lastmodified DESC` |
| User Engagement | `747097031` | `{Month} 26 Monthly Focus Meeting` | Joseph Price | `ancestor = 747097031 AND type = page` |
| Community | `944215356` | `YYYY Month - Monthly Focus Meeting - Community` (e.g. `2026 July - Monthly Focus Meeting - Community`) | Mairead Morgan | `ancestor = 944215356 AND type = page` |

**Note on title patterns:** Squads are inconsistent. Titles may include year as `2026` or `26`, month as full name or abbreviation, and various suffixes. Always match the target month by scanning all results rather than relying on exact title format.

### Automated discovery process

When user says "review the [Squad Name] MFM for [Month]":

1. **Parse the request:**
   - Extract squad name and month
   - Look up the squad in the table above

2. **Fetch from Confluence (always):**
   - Run the squad's CQL query against cloudId `0e31f281-3568-4559-ae88-153abcdead38`
   - From results, identify the **target month page** (match month name in title)
   - Also identify the **previous month page** (needed for action carry-forward analysis)
   - Fetch both pages with `getConfluencePage` using `contentFormat: markdown`
   - **Important:** Sort by creation date to find the latest page for the target month (squads may have multiple pages per month)

3. **Perform action carry-forward analysis** (see section below)

4. **Proceed with five-dimensional framework analysis**

5. **Handle issues:**
   - If Confluence MCP is not connected: ask user to reconnect via `/mcp`
   - If multiple pages match the target month: show list and ask user to clarify
   - If no pages match: list available pages and ask user to confirm month/squad

### Action carry-forward analysis

**Purpose:** Explicitly track what the squad planned last month vs what they delivered this month. This is a key accountability tool.

**Process:**
1. From the **previous month's MFM**, extract the "Next Month" / "Focus Next Month" / "Prioritized Bets" section - these are the committed actions
2. From the **current month's MFM**, extract the "Progress Last Month" / "Review Last Month's Progress" section - these are the reported outcomes
3. Match each planned action to its outcome and produce an **action carry-forward table**

**Output format - include in every MFM review:**

### Action carry-forward from {previous month}

| Planned action | Status | Update from current MFM | Learning |
|----------------|--------|-------------------------|----------|
| {Initiative from prev month} | Done / Partial / Not done / Carried forward | {What the current MFM says about it} | {Why it did/didn't happen, what was learned} |

**Status definitions:**
- **Done** - Completed as planned or better
- **Partial** - Started but not finished, or scope reduced
- **Not done** - Not addressed at all in the current month's progress
- **Carried forward** - Explicitly moved to next month's plan
- **Dropped** - Was planned but consciously removed (check if explained)

**What to flag:**
- Actions that appear in neither progress nor next month's plan (silently dropped)
- Actions carried forward 2+ months without progress
- New priorities that appeared without explanation of what they displaced

### Adding a new squad

When a new squad's MFM folder is discovered:
1. Add it to the lookup table above with folder ID (if known), title pattern, author(s), and CQL
2. Save a reference memory with the same details
3. If the user provides a Confluence folder URL, extract the folder ID from the URL path

## What is a Monthly Focus Meeting?

**Purpose:** Provide the opportunity for squads and leadership to examine progress and decide what to do next.

**Desired Outcomes:**
1. Clear monthly focus
2. Confidence in quarterly targets
3. Early identification of issues and support needed

**Key principle:** MFM should result in **decisions**, not just information sharing. The meeting should answer: "What should we do next and why?"

---

## The Five-Dimensional Analysis Framework

When reviewing an MFM pre-read, evaluate against these five dimensions:

### 1. Examine Progress (Retrospective Quality)
**What to look for:**
- Clear metrics with month-over-month changes
- Confidence levels on quarterly KRs (on track, at risk, likely failure)
- Honest assessment of misses with root cause analysis
- Commentary on whether metrics are moving in right direction

**Red flags:**
- Numbers presented without context or interpretation
- Far behind on targets without discussing implications
- Confidence ratings that don't match the data
- Missing discussion of what changed and why

**Strong examples:**
- "KR2 dropped 9% after closing experiment mid-January. Rates had peaked at 37% during the experiment."
- "Root cause identified: technical training alone insufficient. CS enablement with value narratives needed."

**Weak examples:**
- Just stating current numbers without explaining what happened
- Generic "on track" when numbers tell different story
- No connection between actions taken and results seen

### 2. Decide What to Do Next (Strategic Clarity)
**What to look for:**
- Clear problem statements (not just task lists)
- Prioritized bets with expected impact on specific KRs
- Evidence of trade-offs (what they're NOT doing)
- Connection between learnings and next actions

**Red flags:**
- Long list of priorities without clear ranking
- Activities described without expected outcomes
- "Everything is important" without forced choices
- Discovery work prioritized when far behind targets

**Key questions:**
- Can you identify the top 2-3 priorities from reading the document?
- Is expected impact stated for each bet?
- Are effort estimates provided?
- Is sequencing/dependencies clear?

**Strong examples:**
- "Top 3 priorities: (1) Scale adoption momentum using proven playbook (expect 25% uplift), (2) CS enablement design to test value narrative hypothesis, (3) H1 OKR definition (2 weeks)"
- Clear statement of problem being solved, how it connects to KRs, and why this approach

**Weak examples:**
- "Continue onboarding experimentation series" without specifics on which experiments, expected impact, or capacity required
- Listing 7 "top priorities" for a single month
- Initiatives described as links without summaries

### 3. Clear Monthly Focus
**What to look for:**
- Specific problem(s) to solve (outcome-focused, not output-focused)
- Which KR(s) the month's work aligns to
- Which metric(s) will be moved
- Rationale for why this focus makes sense

**Red flags:**
- Focus that doesn't address largest gaps in KRs
- Mismatch between problem and proposed solutions
- Spreading thin across too many areas
- Significant capacity on non-KR work without justification

**Test:**
After reading, can you state in 1-2 sentences: "This squad is focusing on X in February because Y, and success looks like Z"?

**Strong examples:**
- "Focus on KR2 and KR3 because meaningful action rates correlate with NURR. Expect experiments to impact mainly KR2."
- Problem clearly stated with branch: "Activation / First Session Value Gap → Branch: Unclear path to value"

**Weak examples:**
- Focus on KR2/KR3 when KR1 has biggest gap and most successful experiments, without explaining why
- Multiple problems stated without clear priority

### 4. Confidence in Quarterly Targets
**What to look for:**
- Explicit confidence rating for each KR
- Discussion of whether targets are achievable at current trajectory
- Math that shows path from current state to target
- Options presented if targets appear unachievable

**Red flags:**
- Large gaps to quarterly targets without discussion of feasibility
- "Challenge" or "At risk" confidence without mitigation plan
- Velocity constraints identified but not addressed in plan
- Incremental improvements proposed when transformational change needed

**Critical assessment:**
- For each KR, calculate gap to target and months remaining
- Look at recent velocity (points/month progress)
- Check if monthly plan can mathematically close gaps
- If not, document needs discussion of: (1) what would need to change, (2) whether to adjust targets, or (3) accept partial achievement

**Strong examples:**
- "H2 target missed. Technical training improved demo confidence (2.3 to 3.9) but overall independence at 3.0 vs 4-5 target."
- Asking leadership: "Given current sales readiness, confirm whether June target is realistic, or if this KR should be re-framed as H2 objective."

**Weak examples:**
- 30% actual vs 70% target with 4 months left, rated "Challenge" with plan for more of same approach
- No discussion of what would need to fundamentally change to hit targets

### 5. Early Identification of Issues and Support Needed
**What to look for:**
- **Blockers:** What's blocking work and what are they doing to unblock?
- **Dependencies:** Where dependent on other teams and how managing those dependencies?
- **Asks:** Specific requests of leadership

**Red flags:**
- Empty dependencies section (unlikely for complex work)
- Blockers mentioned but no mitigation plans
- Same blockers appearing month over month without resolution
- Vague asks that don't enable action

**Strong examples:**
- "Blocker: Team bandwidth. 5 asks per geo per week from account teams. Mitigation: Need alignment on team priorities to protect strategic capacity."
- "Dependency: Data team for PQL pipeline. Management plan: Regular syncs established, first workshop complete, test team identified."
- "Ask: Clarify whether sales KR relies on new team (not yet hired) or existing org. Affects H1 achievability."

**Weak examples:**
- "Blockers: Data gathering takes too long (4 weeks). Mitigation: Run more experiments" (doesn't address root cause)
- Generic asks like "support needed" without specifics
- Dependencies listed without management plans

---

## The Gap Analysis: Common Issues to Identify

### Gap 1: No Decision Framework Presented
**Symptom:** Document presents information but doesn't force a decision.
**What's missing:** Options, trade-offs, recommendations
**Impact:** Meeting becomes status update, not decision-making forum

### Gap 2: Incrementalism vs. Transformation Mismatch
**Symptom:** Need 30-point improvements, plan shows 5-point experiments
**What's missing:** Discussion of whether approach can close gaps
**Impact:** Busy work without meaningful progress toward targets

### Gap 3: Prioritization Ambiguity
**Symptom:** Cannot answer "If team only did 2 things this month, what should they be?"
**What's missing:** Forced ranking, capacity allocation, explicit trade-offs
**Impact:** Team spreads thin, everything moves slowly

### Gap 4: Learning-to-Action Disconnect
**Symptom:** Good learnings captured but unclear how they inform next month
**What's missing:** Explicit connection from "we learned X" to "therefore we're doing Y"
**Impact:** Repeated learning without compounding progress

### Gap 5: Capacity Allocation Invisible
**Symptom:** Many initiatives listed, unclear how much time each requires
**What's missing:** Effort estimates, percentage of team capacity, sequencing
**Impact:** Over-commitment, under-delivery

### Gap 6: Dependency Blind Spots
**Symptom:** Empty dependencies section or dependencies without management plans
**What's missing:** Clear understanding of what's needed from other teams
**Impact:** Surprises, delays, blockers appearing late

### Gap 7: Avoidance of Hard Truths
**Symptom:** Far behind targets but document doesn't address feasibility
**What's missing:** Honest assessment of whether approach or targets need adjustment
**Impact:** Continued investment in unachievable goals

---

## Question Framework for MFM Reviews

Use these question categories to probe the document and prepare for the meeting:

### A. Priority and Capacity
1. **Forced ranking:** "If you could only commit to 3 bets this month with confidence, which 3 and why?"
2. **Capacity reality check:** "What percentage of time goes to ad-hoc work vs. strategic initiatives?"
3. **Trade-off question:** "What are you explicitly choosing NOT to do?"
4. **Leadership support:** "What specific asks should I decline/redirect to protect your focus?"

### B. Strategic Clarity on Targets
5. **Reality check:** "Looking at current state vs. targets with time remaining, are quarterly targets achievable?"
6. **If-we're-honest:** "If you had to bet your own money, what will actual end-of-quarter numbers be?"
7. **Success criteria:** "What would 'good enough' progress look like by month-end to keep quarterly targets within reach?"

### C. Learning Application and Hypothesis Testing
8. **Priority clarity test:** "Why isn't [biggest success from last month] your #1 priority?"
9. **Hypothesis validation:** "How will you know if this new approach is working? What would make you pivot?"
10. **Momentum question:** "Are you optimizing for growth rate or absolute numbers? Different answer = different strategy."

### D. Dependencies and Organizational Alignment
11. **Dependency timing:** "If you surface feedback in [Month], what's realistic timeline for incorporation given product planning cycles?"
12. **Critical path:** "What's the critical path for [dependent initiative], and what happens if [team] has competing priorities?"
13. **Workshop readiness:** "Can [alignment workshop] succeed without [prerequisite decision]?"

### E. Execution and Impact
14. **Expected impact:** "For each priority bet, what specific KR does it impact and by how much?"
15. **Backlog prioritization:** "If I gave you capacity for only 2 experiments, which 2 and why?"
16. **Discovery vs. delivery:** "When behind targets, is discovery the right focus? What's the case for it?"

### F. Retrospective (What Happened)
17. **The experiment that worked:** "Why close/change an experiment that was working?"
18. **Learning to shipping:** "Are you shipping this permanently, iterating, or moving to next experiment?"
19. **Velocity constraints:** "How does this month's plan address structural constraints, or are you accepting slower progress?"

### G. Meta Questions (For Your Own Reflection)
20. **Focus smell test:** Can you state in 1-2 sentences what this squad's focus is and why it will work?
21. **Decision made?** Did meeting result in decisions or just information sharing?
22. **Confidence calibrated?** Do you believe quarterly targets are achievable? If not, when will that decision be made?

---

## Red Flags to Watch For

**In the document:**
- ⚠️ Confidence dropping on quarterly targets without clear plan to recover
- ⚠️ Same blockers appearing month over month without resolution
- ⚠️ Vague priorities or too many priorities (lack of focus)
- ⚠️ Bets that aren't linked to specific KRs
- ⚠️ Outputs being discussed instead of outcomes
- ⚠️ Large gaps to targets without discussion of feasibility
- ⚠️ Successful experiments closed without explanation
- ⚠️ Empty dependencies section

**In the meeting:**
- ⚠️ Defensiveness about targets (suggests they know targets aren't achievable)
- ⚠️ Vague answers about priorities (suggests lack of strategic thinking)
- ⚠️ "We're learning" without "We're shipping" (discovery as delay tactic)
- ⚠️ No asks for help (when behind, they should need something from you)

---

## Review Output Structure

When asked to review an MFM, structure the analysis as follows:

### 1. Executive Summary
- Overall grade (A-F)
- Key strengths and weaknesses
- Bottom-line assessment

### 2. Action carry-forward table
Compare previous month's planned actions against current month's reported progress. See "Action carry-forward analysis" in the discovery section for format and status definitions.

### 3. Content Overview
Scannable summary of what the squad wrote, following the MFM outline structure. The user should be able to skip reading the full source document if short on time.
- **Metrics update:** Table of each KR (target, result, status, one-line explanation), support metrics, OKR transitions
- **Progress last month:** Status of each priority with key numbers, key learnings from experiments/interviews
- **Focus next month:** Each priority with target metrics and key initiatives, additional focus areas
- **Blockers and asks:** Each blocker with severity tag [Critical/Risk], each ask of leadership

### 4. Purpose Achievement Analysis
Rate each of the five dimensions:
- Examine progress: ✅/⚠️/❌
- Decide what to do next: ✅/⚠️/❌
- Clear monthly focus: ✅/⚠️/❌
- Confidence in quarterly targets: ✅/⚠️/❌
- Early identification of issues: ✅/⚠️/❌

For each, provide:
- What the document does well
- What's missing or unclear
- Specific examples from the text

### 5. Strategic Issues and Gaps
Identify major issues using the gap framework:
- Name the issue
- Explain why it matters
- Show impact on execution
- Suggest what's needed

### 6. Critical Questions for the Meeting
Provide 6-7 "must ask" questions and 2-3 "if time" questions:
- Bold the most critical questions
- Explain why each question matters
- Include what the answer reveals

### 7. Comparison (if multiple squads)
Compare quality across squads on key dimensions:
- Retrospective quality
- Strategic thinking
- Prioritization clarity
- Dependency management

### 8. Recommendations for the Meeting
- What to start with (most critical decisions)
- What to push on (areas needing clarity)
- What to test (hypotheses to validate)
- Exit criteria (don't leave meeting until...)

---

## Quality Indicators: Strong vs. Weak MFMs

### Strong MFM Characteristics
✅ Honest about misses with root cause analysis
✅ Learning explicitly informing next actions
✅ Clear prioritization (can identify top 2-3)
✅ Expected impact stated for each bet
✅ Dependencies identified with management plans
✅ Strategic questions raised in Asks section
✅ Math works (plan can close gaps to targets)
✅ Trade-offs acknowledged (saying no to things)

### Weak MFM Characteristics
❌ Numbers without interpretation or context
❌ Avoids discussion of feasibility
❌ Long list of priorities without ranking
❌ Activities without expected outcomes
❌ Empty dependencies section
❌ Same blockers month over month
❌ Discovery prioritized over delivery when behind
❌ Closed successful experiments without explanation

---

## Special Cases

### Fiscal Year Transitions (H2 to H1)
**Challenge:** Defining next period's OKRs mid-month creates circular dependency.

**What to look for:**
- Explicit acknowledgment of transition ambiguity
- Clear timeline for OKR definition
- Thoughtful questions about target-setting in Asks section
- Plan for how to proceed before OKRs finalized

**What to push on:**
- Accelerate OKR definition to reduce ambiguity window
- Ensure current month's bets can flex to final OKRs
- Get prerequisite decisions made (scope, dependencies) before setting targets

### When Far Behind Targets
**Math to do:**
- Calculate gap: Target minus Current
- Calculate runway: Months remaining
- Calculate required velocity: Gap divided by Runway
- Compare to historical velocity

**If required velocity >> historical velocity:**
- Document needs to address: What will fundamentally change?
- Or: Should targets be adjusted?
- Or: Accept partial achievement and optimize for learning?

**Don't accept:** Plan for incremental improvements when transformational change needed.

### When Structural Constraints Exist
**Common constraints:**
- Small user base (long experiment cycles)
- Limited surfaces to test on
- Org changes creating drag
- Dependency bottlenecks

**What to look for:**
- Constraints acknowledged in Blockers section
- Mitigation plans that address root cause
- Asks for leadership help removing constraints
- Adjusted targets if constraints can't be removed

**Red flag:** Constraints identified but plan ignores them (pretends they don't exist).

---

## Context to Provide When Requesting MFM Review

When asking Claude to review an MFM, provide:

1. **This framework document** (load this file as context)
2. **The MFM outline** (if not in this doc, reference /Process/MFM/Outline.md)
3. **The squad's MFM pre-read** (the document to review)
4. **Previous month's MFM** (if available, for trend analysis)
5. **Squad OKRs** (reference to /LLM_Context/OKRs/OKRs.md or equivalent)

**Example prompt:**
> "Review the [Squad Name] MFM for [Month]. Focus on whether it achieves the MFM purpose: clear monthly focus, confidence in quarterly targets, and early identification of issues. I particularly want to understand: (1) Are they focused on the right things to create highest impact? (2) What questions should I ask to test their strategic thinking?"

---

## Key Principles for MFM Reviews

1. **Optimize for decisions, not information sharing**
   - MFM should result in clear choices made
   - Information without decision framework is insufficient

2. **Prioritization requires saying no**
   - True focus means trade-offs
   - "Everything is priority" = nothing is priority

3. **Learning must connect to action**
   - Experiments should inform next bets
   - Avoid repeated learning without compounding progress

4. **Math must work**
   - Current velocity + remaining time must reach targets
   - Or: Honest conversation about adjusting targets

5. **Dependencies need management plans**
   - Not just "we depend on X team"
   - But: "Here's what we need and how we're managing it"

6. **Capacity is finite**
   - Test whether plan fits within available capacity
   - Account for ad-hoc work, not just strategic initiatives

7. **Honesty over optimism**
   - Prefer teams that acknowledge challenges
   - Red flag: Far behind but document doesn't address it

8. **Strategic thinking over process compliance**
   - Following outline format is table stakes
   - Real value is in quality of strategic reasoning

---

## Document Version

**Version:** 1.0
**Created:** February 13, 2026
**Based on:** Analysis of First Strike and Strategic Accounts MFM reviews
**Update trigger:** When new patterns emerge from reviewing multiple MFMs over time
