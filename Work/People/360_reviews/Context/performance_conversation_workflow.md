# Performance Conversation Prep Workflow

## Purpose

This workflow generates a structured conversation guide for delivering performance feedback. It transforms a completed 360 review into a timed, practical conversation script with talking points, questions, and backup responses.

**Key principle:** This is a conversation GUIDE, not a script to read verbatim. It helps you stay structured while keeping the conversation natural and collaborative.

## Trigger Commands

When the user says:
- `performance conversation prep: [Name]`
- `perf conversation prep: [Name]`

Follow this complete process.

---

## Prerequisites

**Required before running this workflow:**
- Completed 360 review for the person (`360_[Name]_FY26.md`)
- Final performance descriptor confirmed (post-calibration)

**If 360 review doesn't exist:**
- Inform user: "No 360 review found for [Name]. Run `360 [Name]` first to generate the review."
- Do not proceed

---

## Output Format Overview

**The conversation prep document follows this structure:**

```markdown
# Performance Conversation Prep: [Name] - FY26

**Date:** [Meeting date]
**Performance Descriptor:** [Role Model | High Impact | Fully Successful | Developing | Risk]

---

## Autodesk performance conversation framework

[Key principles from PDF guide]

---

## Meeting flow

### Opening (5 minutes)
[Opening script and framing]

### Performance descriptor: [Descriptor] (10 minutes)
[Share descriptor, rationale, pause for reaction]

### Celebrate strengths (15 minutes)
[2-4 strengths from 360, with questions to ask]

### Development areas (20 minutes)
[2-3 development areas from 360, with specific examples and questions]

### Make [Name] aware of (if applicable)
[Individual concerns from team feedback to address privately]

### Priorities for next year (10 minutes)
[3-4 priorities with success criteria]

### Action items (5 minutes)
[Concrete next steps for first 30 days]

### Closing (5 minutes)
[Summary, final questions, affirmation]

---

## Conversation principles
[Do's and don'ts]

## Backup: Questions [Name] might ask
[Anticipated questions with suggested responses]

## Notes during conversation
[Space for live notes]
```

---

## Step 1: Gather Inputs

### A. Read the 360 Review (Required)

1. Locate: `Work/People/360_reviews/[Name]/360_[Name]_FY26.md`
2. Read completely - this is your primary source
3. Extract:
   - Key strengths (from Section 4)
   - Development areas (from Section 7)
   - Peer feedback highlights (from Section 2)
   - Self-assessment themes (from Section 3)
   - Recommendations (from Section 8)

### B. Get Performance Descriptor (Required)

Ask user: "What is [Name]'s final performance descriptor?"

Options:
- **Role Model** - Performance consistently sets the standard for others
- **High Impact** - Performance clearly exceeds expectations
- **Fully Successful** - Performance meets expectations of role and level
- **Developing** - Performance inconsistent or not yet at expected level
- **Risk** - Performance below expectations, requires immediate focus

### C. Read Reference Documents

1. **Performance Conversation Guide PDF** - `Work/People/360_reviews/Context/PerformanceConversation_Employee_Quick Reference Guide.pdf`
   - Extract conversation framework principles
   - Note the recommended conversation structure

2. **One ORBIT Behaviours** - `Work/People/360_reviews/Context/One_Orbit_behaviours.md`
   - Reference for behavioral feedback alignment

### D. Optional: Additional Context

- Recent 1:1 notes from `Work/People/121s/[name]/`
- Meeting transcripts via Granola MCP
- Any specific concerns user wants to address

---

## Step 2: Validate and Confirm

Present a checklist to the user:

```
I've located the following for [Name]'s conversation prep:

**Required:**
✓ 360 Review: 360_[Name]_FY26.md
✓ Performance Descriptor: [descriptor from user]
✓ Conversation Guide PDF

**From the 360 Review:**
- Strengths identified: [count]
- Development areas identified: [count]
- Peer reviewers included: [names]

**Optional context found:**
- 1:1 notes: [yes/no]
- Additional documents: [list]

Ready to generate the conversation prep document?
```

**Only proceed after user confirmation.**

---

## Step 3: Generate Document Sections

### Opening Section

Create a natural opening that:
- Sets collaborative tone ("This is a two-way conversation")
- Previews the structure
- Acknowledges this is about growth, not judgment

**Template:**
```markdown
### Opening (5 minutes)

"[Name], today I want to share your performance descriptor, explain the rationale, celebrate your strengths, and discuss focus areas for next year. This is collaborative - I want your perspective throughout."
```

### Performance Descriptor Section

Structure:
1. **State the descriptor clearly** - Don't bury the lead
2. **Provide brief positive framing** - What it means, why it's earned
3. **Give 3-4 bullet rationale** - Key reasons from 360
4. **Pause for reaction** - Explicit note to give space

**Tailor tone to descriptor:**
- Role Model/High Impact: Celebratory, acknowledge excellence
- Fully Successful: Positive, emphasize this is a strong outcome
- Developing/Risk: Supportive, focus on path forward

### Strengths Section

For each strength (2-4 total):
1. **Name the strength** - Clear heading
2. **Brief explanation** - Why it matters, what you observed
3. **Specific example** - From 360 peer feedback
4. **Question to ask** - Engage them in reflection

**Format:**
```markdown
#### 1. [Strength name]

[1-2 sentences on what you observed and why it matters]

**Ask:** "[Reflective question about this strength]"
```

### Development Areas Section

For each area (2-3 total):
1. **Name the area** - Clear, non-judgmental heading
2. **Context** - Why this matters for their growth
3. **Specific example** - Concrete instance from 360
4. **What you'd like to see** - Clear, actionable expectation
5. **Questions to ask** - Engage them in problem-solving

**Important:** Frame as opportunities to increase impact, not weaknesses.

**Format:**
```markdown
#### 1. [Development area]
**(Primary development area)** [if applicable]

"[Context on why this matters]"

**Specific example:**
"[Concrete instance from 360 feedback]"

**What I'd like to see:**
"[Clear, actionable expectation]"

**Ask:**
- "[Question to understand their perspective]"
- "[Question to engage them in solution]"
```

### Individual Concerns Section (If Applicable)

If 360 feedback contains specific concerns from individual team members that should be addressed privately:
- Don't name this section in a way that singles people out negatively
- Frame as "things to be aware of" rather than complaints
- Focus on actionable follow-up

**Only include if genuinely needed.**

### Priorities Section

Structure:
1. **Ask first** - "What do you think your focus areas should be?"
2. **Then align** - Present 3-4 priorities with success criteria
3. **Include progress checks** - How you'll track together

**Format:**
```markdown
#### [Priority name]

**Success looks like:**
- [Measurable outcome]
- [Behavioral change]

**Progress checks:** [How and when you'll review]
```

### Action Items Section

Concrete next steps for first 30 days:
- 4-6 specific actions
- Mix of quick wins and longer-term setup
- Include how you'll support them

### Closing Section

1. **Summary** - 2-3 sentence recap of descriptor + key themes
2. **Final questions** - "What's unclear?" "How are you feeling?"
3. **Affirmation** - Genuine, specific appreciation

---

## Step 4: Add Supporting Sections

### Conversation Principles

```markdown
## Conversation principles

**Do:**
- ✅ Listen more than talk - give [Name] space
- ✅ Use specific examples from 360
- ✅ Keep tone positive and forward-looking
- ✅ Ask for [Name]'s perspective throughout
- ✅ End with clear action items

**Avoid:**
- ❌ Comparing [Name] to peers
- ❌ Bringing up compensation (separate conversation)
- ❌ Making it feel one-way or scripted
```

### Backup Questions

Anticipate 2-4 questions they might ask based on:
- Their descriptor level
- Development areas identified
- Known concerns from self-assessment

**Common questions by descriptor:**

For High Impact:
- "Why High Impact and not Role Model?"

For Fully Successful:
- "What would it take to get to High Impact?"

For Developing:
- "How long do I have to improve?"

### Notes Section

Empty section for live note-taking during conversation:
```markdown
## Notes during conversation

**[Name]'s reaction to descriptor:**

**[Name]'s perspective on development areas:**

**Agreements reached:**

**Follow-up items:**
```

---

## Step 5: Quality Check

Before presenting, verify:

### Structure Checks
- [ ] All sections present and properly ordered
- [ ] Timing annotations included (5 min, 10 min, etc.)
- [ ] Total meeting time ~60 minutes
- [ ] Questions to ask included in each major section

### Content Checks
- [ ] Descriptor rationale has 3-4 specific points from 360
- [ ] Each strength has specific example from peer feedback
- [ ] Each development area has specific example
- [ ] Development areas framed constructively, not punitively
- [ ] Priorities are actionable with success criteria
- [ ] Action items are concrete for first 30 days

### Tone Checks
- [ ] Collaborative language throughout
- [ ] Balance of strengths and development (not just criticism)
- [ ] Forward-looking focus on growth
- [ ] Genuine affirmation at close

### Alignment Checks
- [ ] Conversation framework principles from PDF incorporated
- [ ] Key themes from 360 review reflected accurately
- [ ] Development areas match 360 Section 7
- [ ] Strengths match 360 Section 4

---

## Step 6: Present and Save

**Present to user:**
1. Show summary of what was generated
2. Highlight any areas where you made judgment calls
3. Ask if they want to review before saving

**Save location:**
`Work/People/360_reviews/[Name]/Performance_conversation_[Name]-FY26.md`

**Only save after user approval.**

---

## Important Guidelines

### Do:
- ✓ Keep language conversational, not robotic
- ✓ Include specific quotes and examples from 360
- ✓ Make questions open-ended to invite dialogue
- ✓ Provide backup answers for anticipated pushback
- ✓ Leave space for the conversation to breathe

### Don't:
- ✗ Make it a script to read verbatim
- ✗ Include every detail from the 360 (select highlights)
- ✗ Focus only on development areas
- ✗ Use jargon or HR-speak
- ✗ Rush - this document helps with a high-stakes conversation

---

## Troubleshooting

**If 360 review is missing:**
- Cannot proceed - 360 is required input
- Direct user to run `360 [Name]` first

**If descriptor not confirmed:**
- Ask user directly - don't guess
- Calibration must be complete before conversation prep

**If 360 is thin on content:**
- Note which sections have limited input
- Flag to user that conversation may need additional context
- Suggest gathering more feedback before the meeting

**If development areas are sensitive:**
- Frame with extra care
- Focus on observable behaviors, not personality
- Emphasize support and path forward

---

## Example Usage

**User says:** "performance conversation prep: Joe"

**Process:**
1. "I'll generate the conversation prep for Joe. Let me gather the required inputs..."
2. [Read 360 review from Joe's folder]
3. "What is Joe's final performance descriptor?"
4. [User: "High Impact"]
5. [Read PDF guide and One ORBIT]
6. [Present validation checklist]
7. "Ready to proceed?"
8. [After confirmation: Generate full document]
9. "I've created the conversation prep. Here's a summary of key points..."
10. "Would you like me to save this to Joe's folder?"
11. [Save after approval]
