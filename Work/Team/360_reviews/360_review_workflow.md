# 360 Review Generation Workflow

## Purpose
This workflow defines the PROCESS for generating comprehensive 360 performance reviews. Assessment criteria and frameworks are defined in `performance_assessment_guide.md`.

## Trigger Commands
When the user says:
- "360 [FirstName]" (e.g., "360 Anders")
- "review [Name]"
- "generate 360 for [Name]"

Follow this complete process:

---

## Output Format Overview

**CRITICAL: The final 360 review MUST follow this exact structure and formatting:**

```markdown
# 360 Review: [Name] - FY26 H2

## 1. Executive Summary (150-200 words)
[Brief prose paragraph with 2-3 key highlights]

## 2. Peer Feedback Summary (300-400 words total)
**Feedback from [Peer 1 Name] ([Role]):**
- Bullet point
- Bullet point
- Bullet point

**Feedback from [Peer 2 Name] ([Role]):**
- Bullet point
- Bullet point

[Continue for each peer reviewer]

## 3. Self-Assessment Summary (150-200 words)
- Bullet point capturing key contribution
- Bullet point on outcomes
- Bullet point on behaviors
- Bullet point on challenges
- Bullet point on development areas
[5-7+ bullets total]

## 4. Key Strengths (250-300 words)
**[Strength Title 1]**
Brief prose intro sentence.
- Bullet with evidence
- Bullet with impact
- Bullet with quote

**[Strength Title 2]**
Brief prose intro sentence.
- Bullet with evidence
- Bullet with impact

## 5. Outcomes Delivered (125-175 words)
[Brief prose context]
- Bullet: Outcome with OKR alignment
- Bullet: Impact with evidence
- Bullet: Peer validation

## 6. Behaviors and Impact (150-200 words)
[Brief intro on One ORBIT alignment]

**One Autodesk:**
- Bullet with example
- Bullet with quote

**Trusted:**
- Bullet with example

## 7. Areas for Improvement (500-550 words, double weight of Strengths)
**[Development Area 1]**
Context sentence on why it matters.
- Bullet: Observation
- Bullet: Impact
- Bullet: Suggestion
- Bullet: Target

**[Development Area 2]**
Context sentence.
- Bullets with details

**[Development Area 3]**
Context sentence.
- Bullets with details

## 8. Recommendations & Goals (125-175 words)
**Immediate Actions (Next 30 Days):**
- Bullet
- Bullet

**Q1 FY27 Goals:**
- Bullet with target
- Bullet with target
```

**Key formatting rules:**
1. **Sections 2-3**: Bullet points ONLY (no prose paragraphs)
2. **Sections 4-8**: Brief prose intro + bullets for evidence/details
3. **Section 2**: Individual subsection for EACH peer reviewer
4. **Never**: Pure prose paragraphs in synthesis sections

---

## Step 1: Locate the Person's Folder

1. Look for folder in `Work/Team/360_reviews/[FirstName]_[LastName]/`
2. Use fuzzy matching on first name (e.g., "Anders" → "Anders_Webster")
3. If multiple matches exist, ask user to clarify
4. If folder doesn't exist, inform user and ask if they want to create it

**Example folders:** `Anders_Webster/`, `Chris_Small/`, `Sarah_Johnson/`

---

## Step 2: Read All Input Documents

Read documents in this specific order:

### A. Read from Person's Folder (`360_reviews/[Name]/`)

**All feedback documents for this person are in their folder.**

Read ALL `.md` and `.csv` files in the folder (except the final 360 review), including:

**Self-Assessment:**
- Look for files containing "self" or "assessment" in the name
- Read completely - this is the person's own perspective

**Peer Feedback & Peer Assessments:**
- Read ALL other feedback files in the folder
- These may be named anything (e.g., "feedback_from_john.md", "peer_assessment.md", "peer_review_1.md")
- May include both qualitative feedback and assessment ratings
- Note patterns and themes across multiple feedback sources

### B. Read Shared Reference Documents (`360_reviews/` parent folder)

**CRITICAL - Read in this order:**

1. **`performance_assessment_guide.md`** - Read completely and carefully
   - Contains all assessment criteria and frameworks
   - Defines WHAT and HOW dimensions
   - Explains CARE method
   - References One ORBIT behavioral framework
   - Provides rating scales and evaluation standards

2. **`One_Orbit_behaviours.md`** - Read completely
   - Defines the specific One ORBIT behaviors
   - Provides behavioral framework details
   - Essential for evaluating the HOW dimension

3. **`Q3 OKRs - for H2.md`** - Strategic context for Q3

4. **`Q4 - OKRs (updated for H2).md`** - Strategic context for Q4

---

## Step 3: Validate Inputs and Confirm

**Before proceeding with analysis, validate all required documents are present.**

### Required Document Checklist:

Present a list to the user showing what was found:

**From Person's Folder:**
- [ ] Self-assessment document
- [ ] Peer feedback files (list each one found)
- [ ] Peer assessment files (list each one found)
- [ ] Any other feedback documents (list all)

**From Shared Reference Folder:**
- [ ] `performance_assessment_guide.md`
- [ ] `One_Orbit_behaviours.md`
- [ ] `Q3 OKRs - for H2.md`
- [ ] `Q4 - OKRs (updated for H2).md`
- [ ] `360_review_workflow.md` (this file)

### Confirmation Message Format:

```
I've located the following documents for [Name]'s 360 review:

**Person's Folder (360_reviews/[Name]/):**
✓ Self-assessment: [filename]
✓ Peer feedback: [filename 1]
✓ Peer assessment: [filename 2]
✓ Additional feedback: [filename 3]
[... list all feedback documents found]

**Shared Reference Documents:**
✓ Performance Assessment Guide
✓ One ORBIT Behaviours
✓ Q3 OKRs for H2
✓ Q4 OKRs for H2
✓ 360 Review Workflow

**Status:**
[X] All required documents present
[ ] Missing documents (see below)

Missing:
- [List any missing documents]

Ready to proceed with the review synthesis?
```

### If Documents Are Missing:

- Clearly list what's missing
- Explain why it's needed
- Ask user if they want to:
  - Add the missing documents and restart
  - Proceed without them (with reduced quality)
  - Cancel and come back later

### Only Proceed After User Confirmation

**Do not start synthesis until:**
1. All documents are listed and shown to user
2. User explicitly confirms to proceed

---

## Step 4: Analyze and Synthesize

**Apply the frameworks from `performance_assessment_guide.md`:**

### Feedback Weighting and Prioritization

**CRITICAL: Prioritize peer feedback over self-assessment**

1. **Start with peer feedback as the primary evidence source**
   - Read all peer feedback first
   - Identify key themes and patterns across peer sources
   - Note areas where multiple peers agree

2. **Use self-assessment to provide context and intent**
   - Self-assessment helps explain the "why" behind actions
   - Provides the individual's perspective on their work
   - Should support, not drive, the narrative

3. **Emphasize areas where peer feedback corroborates self-assessment**
   - These are the strongest data points
   - Show alignment between self-perception and external perception
   - Highlight these as validated strengths or confirmed development areas

4. **Flag discrepancies between self-view and peer perception**
   - When self-assessment claims strengths not reflected in peer feedback, note this as potential blind spot
   - When peers see strengths not emphasized in self-assessment, note this as opportunity for greater confidence
   - These gaps are valuable feedback for self-awareness

5. **When in conflict, peer feedback takes precedence**
   - Multiple external perspectives carry more weight than self-perception
   - Use self-assessment to understand intent, but rely on peer feedback for impact

**Evidence Hierarchy:**
- **Strong**: Multiple peer sources agree on the same point
- **Moderate**: Peer feedback mentions it, self-assessment confirms
- **Weak**: Only in self-assessment, no peer corroboration

**Target Weighting:**
- **70% of evidence citations should come from peer feedback**
- **30% from self-assessment**
- Self-assessment primarily used where it aligns with peer observations or provides useful context

---

### Analysis Framework

1. **Use the CARE method** as defined in the guide to structure your analysis

2. **Identify Themes:**
   - What patterns emerge across multiple feedback sources?
   - Where is there consensus among peers?
   - Where are there gaps or contradictions?
   - What does peer feedback emphasize that self-assessment doesn't?

3. **Evaluate Against the Guide's Criteria:**
   - Apply the WHAT dimension (outcomes) as defined in the guide
   - Apply the HOW dimension (behaviors) as defined in the guide
   - Use the One ORBIT framework from the guide
   - Apply rating scales if defined in the guide

4. **Balance the Review:**
   - Highlight clear strengths with evidence (primarily peer feedback)
   - Identify growth areas constructively (primarily peer feedback)
   - Ensure feedback is actionable and specific
   - Aim for 50/50 balance between strengths and improvements

5. **Be Evidence-Based:**
   - Quote specific examples from peer feedback
   - Reference concrete outcomes mentioned by peers
   - Tie observations to behaviors and results
   - Use OKRs to validate significance of outcomes
   - Corroborate with self-assessment where alignment exists

---

## Step 5: Structure the Review Document

**Follow the structure specified in `performance_assessment_guide.md`.**

If the guide doesn't specify a structure, use this default:

### Document Header
```markdown
---
type: 360-review
team-member: [Name]
fiscal-year: FY26
review-period: H2 2025
generated: [Today's Date]
status: draft
---

# 360 Review: [Name] - FY26 H2
```

### Required Sections (Total target: 1500-2000 words)

**CRITICAL: Balance strengths and improvements equally (50/50)**

1. **Executive Summary** (150-200 words)
   - Brief overall assessment
   - 2-3 key highlights (mix of strengths and development areas)
   - High-level summary only - details come later
   - Keep this concise and focused

2. **Peer Feedback Summary** (300-400 words total) - INDIVIDUAL SECTIONS WITH BULLETS

   **CRITICAL FORMAT REQUIREMENTS:**
   - **DO NOT write prose paragraphs synthesizing all peer feedback together**
   - **DO create a separate subsection for EACH individual peer reviewer**
   - **DO use bullet points exclusively in this section**
   - Each peer gets their own named heading with their role/relationship
   - Use as many bullets as needed to properly capture what that peer said
   - This section shows transparency: what did each person actually say?

   **Subsection format for each peer:**
   ```markdown
   **Feedback from [Peer Name] ([Role/Relationship]):**
   - Key strength or observation they mentioned
   - Specific example or impact they noted
   - Development area they suggested (if any)
   - Additional points as needed
   ```

   **Cover for each peer:**
   - Key strengths they observed
   - Impact they noted
   - Specific examples or behaviors they mentioned
   - Development areas they identified (if any)
   - Working relationship context (if relevant)

   **Do not include self-assessment** in this section - peer feedback only

   **Complete example:**
   ```markdown
   ## Peer Feedback Summary

   **Feedback from Sarah Johnson (VP Product, Cross-functional Partner):**
   - Strong leadership in driving the Q3 integration initiative
   - Excellent at stakeholder communication during complex negotiations
   - Proactive in identifying blockers and escalating appropriately
   - Could improve delegation to team members on tactical execution
   - Suggestion: Empower team to own more decisions independently

   **Feedback from Mike Chen (Senior Engineer, Direct Report):**
   - Creates psychologically safe environment for the team
   - Provides clear technical direction and architectural guidance
   - Sometimes takes on too much work personally rather than delegating
   - Great at coaching through complex technical problems
   - Suggestion: Trust team more with customer-facing responsibilities

   **Feedback from Alex Rodriguez (Sales Director, Internal Customer):**
   - Responsive and solution-oriented when issues arise
   - Deep product knowledge that helps close enterprise deals
   - Strong advocate for customer needs in product discussions
   ```

   **Why this format:**
   - Shows what each individual peer said (transparency)
   - Makes it easy to see patterns across multiple peers
   - Allows reader to understand different perspectives
   - Provides clear attribution for feedback

3. **Self-Assessment Summary** (150-200 words) - BULLET POINTS ONLY

   **CRITICAL FORMAT REQUIREMENTS:**
   - **DO NOT write prose paragraphs**
   - **DO use bullet points exclusively**
   - **Use as many bullets as needed** to properly capture their perspective
   - This section presents what the individual themselves said about their work
   - Keep bullets concise but comprehensive

   **What to cover:**
   - Key contributions they highlighted
   - Outcomes they're most proud of
   - Behaviors or strengths they emphasized
   - Challenges they faced and how they addressed them
   - Development areas they identified for themselves
   - Goals or growth areas they mentioned

   **Format:**
   ```markdown
   ## Self-Assessment Summary

   - [Key contribution/accomplishment they highlighted]
   - [Specific outcome or impact they noted]
   - [Behavior or approach they emphasized]
   - [Challenge they addressed]
   - [Development area they identified]
   - [Growth goal they mentioned]
   ```

   **Complete example:**
   ```markdown
   ## Self-Assessment Summary

   - Led three major cross-functional initiatives from inception to delivery
   - Drove Q3 OKR completion by coordinating across 5 different teams
   - Focused on building trust through transparent communication and follow-through
   - Navigated organizational restructuring while maintaining team morale
   - Identified need to improve delegation and scale impact through others
   - Worked to develop stronger strategic thinking beyond day-to-day execution
   - Proud of impact on customer satisfaction scores (increased 15%)
   - Seeking opportunities to develop as a people leader
   ```

   **Why this format:**
   - Provides the individual's own perspective clearly
   - Shows self-awareness about strengths and development needs
   - Makes it easy to compare self-perception with peer feedback
   - Scannable format for quick understanding

4. **Key Strengths** (250-300 words) - PROSE + BULLETS

   **CRITICAL FORMAT REQUIREMENTS:**
   - **DO NOT write pure prose paragraphs**
   - **DO use: Brief prose intro + bullet points for evidence**
   - Identify 3-4 specific strengths
   - Use primarily peer feedback quotes and examples (70%+)
   - Apply CARE framework to show impact
   - Reference One ORBIT behaviors where applicable

   **Format for each strength:**
   ```markdown
   **[Strength Name/Title]**

   [1-2 sentence prose intro providing context or theme]

   - Specific example or evidence point from peer feedback
   - Quantifiable outcome or impact
   - Quote or observation from peer reviewer
   - Connection to One ORBIT behavior or framework
   - Additional supporting evidence
   ```

   **Complete example:**
   ```markdown
   ## Key Strengths

   **Driving Cross-Functional Collaboration**

   Multiple peers highlight her ability to break down silos and create alignment across diverse teams:

   - **Sales partnership**: "Transformed our relationship with Sales from transactional to strategic" (VP Sales)
   - **Product alignment**: Led monthly sync that reduced feature conflicts by 40%
   - **One Autodesk behavior**: Consistently prioritizes shared goals over individual team wins
   - **Customer impact**: Cross-team collaboration enabled 3 major enterprise deals to close
   - Quote: "She's the person who makes sure everyone's rowing in the same direction" (Engineering Director)

   **Delivering Results Under Pressure**

   Demonstrates Relentless behavior through sustained execution during high-stakes situations:

   - Q3 product launch: Delivered on time despite 30% team turnover
   - Customer crisis: Led recovery effort that retained $2M account (CEO directly recognized)
   - Process improvement: Maintained quality while reducing cycle time from 6 weeks to 3 weeks
   - Team feedback: "Never loses focus even when things get chaotic" (Direct Report)
   ```

   **Why this format:**
   - Brief prose provides context and theme
   - Bullets make evidence scannable
   - Easier to see specific examples and impact
   - Better readability than dense paragraphs

5. **Outcomes Delivered** (125-175 words) - PROSE + BULLETS

   **Format:** Brief context, then bulleted outcomes with evidence and OKR alignment

   **Example:**
   ```markdown
   ## Outcomes Delivered

   **Strategic Initiative Leadership**

   Led several high-impact initiatives that directly supported Growth OKRs:

   - **Customer expansion**: Drove 3 strategic accounts from pilot to production (Q4 KR2: 4 accounts with 100+ MAUs)
   - **Revenue impact**: Initiatives contributed to $1.2M in expansion revenue
   - **Cross-functional delivery**: Coordinated Product, Sales, and CS to launch enterprise tier
   - **Peer validation**: "Her leadership was critical to closing our largest deal" (Sales VP)
   - **OKR alignment**: Outcomes directly supported Q3 Growth objective on enterprise adoption
   ```

6. **Behaviors and Impact** (150-200 words) - PROSE + BULLETS

   **Format:** Brief theme/intro, then bulleted examples organized by One ORBIT behaviors

   **Example:**
   ```markdown
   ## Behaviors and Impact

   Performance demonstrates strong alignment with One ORBIT framework:

   **One Autodesk:**
   - Acted as linking point between Sales, Product, and CS (multiple peers noted)
   - "Consistently breaks down silos" (Joseph, Peer Squad Lead)
   - Prioritized shared goals over individual team wins

   **Trusted:**
   - Built credibility through follow-through on commitments
   - "I can always count on her to deliver what she promises" (Direct Report)
   - Transparent communication during difficult organizational changes

   **Relentless:**
   - Sustained 9-month customer engagement driving adoption outcomes
   - Maintained momentum through Q3 restructuring
   - "Never loses focus on customer success" (Customer Success Director)
   ```

7. **Areas for Improvement** (500-550 words) - PROSE + BULLETS (DOUBLE WEIGHT OF STRENGTHS)

   **CRITICAL:** This section must be separate and substantially weighted (500-550 words, roughly double Key Strengths)

   **Format:** Context/why it matters, then bullets with observations and suggestions

   **Example:**
   ```markdown
   ## Areas for Improvement

   **Delegation and Scaling Impact**

   Multiple peers identify a pattern of taking on too much personally rather than leveraging the team:

   - **Observation**: "Takes on too much himself rather than delegating" (Manager, peer)
   - **Impact**: Limits team's growth and creates bottleneck
   - **Specific example**: Handles all customer calls personally instead of enabling team
   - **Suggestion**: Identify 2-3 request types suitable for delegation or self-serve
   - **Why it matters**: As a manager, impact should multiply through team, not individual IC work
   - **Target**: Reduce personal direct touches by 25% while maintaining outcomes

   **Team Communication and Transparency**

   Direct reports identify gaps in communication about strategic decisions:

   - **Observation**: "Not aware of leadership discussions until after decisions made" (Direct Report)
   - **Impact**: Team feels excluded and can't align with broader context
   - **Specific example**: Team learned about org changes from others, not from manager
   - **Suggestion**: Establish bi-weekly team updates on strategic discussions
   - **Why it matters**: Distributed team needs predictable communication rhythms
   - **Target**: Zero surprises - team hears major news from manager first
   ```

8. **Recommendations & Goals** (125-175 words) - PROSE + BULLETS

   **Format:** Brief framing, then bulleted immediate actions and goals

   **Example:**
   ```markdown
   ## Recommendations & Goals

   **Immediate Actions (Next 30 Days):**

   - Schedule career development conversations with each direct report
   - Establish bi-weekly team communication rhythm for strategic updates
   - Enroll in Manager Essentials training course

   **Q1 FY27 Goals:**

   - **Scale through delegation**: Reduce personal account touches by 25% while maintaining outcomes
   - **Team development**: Implement monthly knowledge-sharing sessions
   - **Technical depth**: Partner with Product team 4-6 hours/month on platform capabilities
   ```

---

### FORMAT REMINDER - CRITICAL

**Before writing the review, confirm you will:**

1. ✓ Create individual subsection for EACH peer with bullets (Section 2)
2. ✓ Use ONLY bullet points for Self-Assessment Summary (Section 3)
3. ✓ Use prose intro + bullets for ALL synthesis sections (Sections 4-8)
4. ✓ NEVER write pure prose paragraphs in sections 2-8
5. ✓ Follow the exact structure shown in Output Format Overview above

**If you find yourself writing long prose paragraphs without bullets, STOP and reformat.**

---

### Structural Guidelines

**Length Management:**
- **Total document: 1400-1700 words maximum** (25% reduction from previous target)
- Executive Summary: 150-200 words
- Peer Feedback Summary: 300-400 words (bullet points by individual peer)
- Self-Assessment Summary: 150-200 words (bullet points)
- Key Strengths: 250-300 words
- Outcomes Delivered: 125-175 words
- Behaviors and Impact: 150-200 words
- Areas for Improvement: 500-550 words
- Recommendations & Goals: 125-175 words

**Balance Requirements:**
- **Areas for Improvement should have roughly double the word count of Key Strengths**
- Key Strengths: 250-300 words
- Areas for Improvement: 500-550 words (approximately 2x Key Strengths)
- This reflects the importance of providing detailed, actionable development feedback
- Other sections (Outcomes, Behaviors) should balance both strengths and development areas

**Evidence Requirements:**
- **70% of quotes and examples from peer feedback**
- **30% from self-assessment** (primarily where corroborated)
- Self-assessment used mainly for context and intent
- Peer feedback drives the narrative

**Important:** Follow any specific formatting or rating scales defined in the assessment guide.

---

## Step 6: Quality Check

Before presenting to user, verify:

### Structure Checks
✓ **Executive Summary is first** (150-200 words) and concise prose paragraph
✓ **Peer Feedback Summary is second** (after exec summary, before self-assessment)
✓ **Peer Feedback Summary: CRITICAL FORMAT CHECK**
   - Has individual subsection for EACH peer reviewer (count them)
   - Each peer has heading: "**Feedback from [Name] ([Role]):**"
   - Each peer subsection uses ONLY bullet points (NO prose paragraphs)
   - Total is 300-400 words
   - Contains ZERO self-assessment content
✓ **Self-Assessment Summary is third** (after peer feedback, before synthesis sections)
✓ **Self-Assessment Summary: CRITICAL FORMAT CHECK**
   - Uses ONLY bullet points (NO prose paragraphs)
   - 5-7+ bullets capturing key themes from self-assessment
   - 150-200 words total
✓ **Sections 4-8: CRITICAL FORMAT CHECK**
   - Each section uses combination of brief prose intro + bullet points
   - NO pure prose paragraphs without bullets
   - Evidence and examples are in bullet format
   - Brief (1-2 sentence) prose provides context only
✓ **Areas for Improvement is a separate section** (not buried in other sections)
✓ **Areas for Improvement is 500-550 words** (roughly double Key Strengths)
✓ **Key Strengths is 250-300 words**
✓ **Outcomes Delivered is 125-175 words**
✓ **Behaviors and Impact is 150-200 words**
✓ **Recommendations & Goals is 125-175 words**
✓ **Total document length is 1400-1700 words**
✓ **If ANY section is pure prose paragraphs (except Executive Summary), format is WRONG**

### Evidence Balance Checks
✓ **70%+ of quotes and examples come from peer feedback**
✓ **30% or less from self-assessment**
✓ **Self-assessment primarily used where peer feedback corroborates**
✓ Peer feedback drives the narrative, not self-assessment
✓ Discrepancies between self and peer views are flagged

### Content Balance Checks
✓ **50% of content focuses on strengths**
✓ **50% of content focuses on improvements**
✓ Key Strengths section has equal weight to Areas for Improvement section
✓ Constructive, actionable feedback for development areas
✓ Each strength has concrete examples
✓ Each improvement area has concrete examples

### Framework Checks
✓ All feedback sources were incorporated
✓ Assessment frameworks from the guide were properly applied
✓ CARE method used appropriately
✓ One ORBIT behaviors referenced where applicable
✓ Both WHAT and HOW dimensions are covered (as defined in guide)
✓ OKRs used to validate significance of outcomes
✓ Alignment with all criteria in `performance_assessment_guide.md`

### Quality Checks
✓ Specific examples and quotes are included
✓ Recommendations are specific and actionable
✓ Professional, supportive tone throughout
✓ No vague generalizations without examples
✓ Feedback is constructive and respectful

---

## Step 7: Present and Save

**Present to User:**
1. Show a summary of what was synthesized
2. Highlight key findings
3. Ask if they want to review the full draft before saving

**Save the Document:**
- Filename: `360_[FirstName]_[LastName]_FY26.md`
- Location: In the person's folder (`Work/Team/360_reviews/[Name]/`)
- Only save after user approval

---

## Important Guidelines

### Do:
- ✓ Be specific and evidence-based
- ✓ Use direct quotes from feedback when impactful
- ✓ Balance positive and developmental feedback
- ✓ Make connections between behaviors and outcomes
- ✓ Provide actionable recommendations
- ✓ Maintain professional, respectful tone

### Don't:
- ✗ Make assumptions not supported by evidence
- ✗ Include vague generalizations without examples
- ✗ Focus only on strengths or only on weaknesses
- ✗ Copy-paste large sections without synthesis
- ✗ Rush - this is a thoughtful, important document

---

## Troubleshooting

**If folder doesn't exist:**
- Inform user and ask if they want to create it
- Explain what documents should be added

**If documents are missing:**
- List what's missing (self-assessment, peer feedback, etc.)
- Ask user if they want to proceed with available information

**If feedback is contradictory:**
- Acknowledge the different perspectives
- Look for context that explains differences
- Present both views if resolution isn't clear

**If unsure about interpretation:**
- Ask the user for clarification
- Reference specific passages that are ambiguous
- Don't guess - accuracy matters more than speed

---

## Example Usage

**User says:** "360 Anders"

**Your process:**
1. "I'll generate Anders's 360 review. Let me start by locating all required documents..."
2. [Find and read documents from Anders_Webster folder and parent folder]
3. [Present document checklist and ask for confirmation]
4. "Ready to proceed with the review synthesis?"
5. [After confirmation: Analyze and synthesize using CARE framework]
6. "I've completed my analysis. Here's a summary of key findings: [summary]"
7. "Would you like me to save the complete 360 review to Anders's folder?"
8. [Save after approval]

---

## Notes

- **This workflow = PROCESS only.** All assessment criteria, frameworks, and standards are in `performance_assessment_guide.md`
- Always read the assessment guide completely before starting synthesis
- This workflow is for **generating comprehensive 360 reviews** from existing feedback
- For creating an empty template file, use "360 review: [Full Name]" command instead
- The quality of the review depends on the quality of input documents - garbage in, garbage out
- Take your time - a thoughtful, well-synthesized review is more valuable than a quick one
