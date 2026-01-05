# Project Summary: Team Feedback & 360 Review System

**Session Date:** January 3, 2026
**Project:** Chief of Staff Personal OS - Team Feedback Module
**Status:** ✅ Core implementation complete, improvements planned

---

## 1. Project Overview

### What was built:
Comprehensive team feedback and 360 review system integrated into the Personal OS project, allowing command-line capture of observations and AI-powered synthesis of performance reviews.

### Original goals:
1. Create observation command to capture feedback about team members
2. Build 360 review generation system that synthesizes multiple inputs
3. Optimize for context window efficiency
4. Establish patterns for complex workflows

### Current status:
- ✅ Observation feature: Complete and committed
- ✅ 360 review structure: Complete
- ✅ Workflow documentation: Complete
- 🔄 Review output improvements: Planned (awaiting implementation)

---

## 2. Key Decisions Made

### Decision 1: Separate observation files from 360 reviews
**Reasoning:** Observations are point-in-time feedback, while 360 reviews are comprehensive synthesis documents. Keeping them separate allows for:
- Continuous observation capture
- Periodic review synthesis
- Clear audit trail of feedback over time

**Structure chosen:**
```
Work/Team/
├── Observations/              # Point-in-time feedback
└── 360_reviews/              # Comprehensive reviews
    ├── [Person folders]/
    └── [Shared references]
```

### Decision 2: Individual folders for each team member (not shared 360 files)
**Original plan:** Single 360 review file per person in shared folder
**Final decision:** Individual folders per person containing all their feedback
**Reasoning:**
- Better organization of multiple feedback documents
- Self-assessment, peer feedback, and assessments all in one place
- Easier to manage inputs for review generation

### Decision 3: Context-optimized architecture (CRITICAL)
**Problem identified:** Putting detailed 360 workflow instructions in CLAUDE.md would:
- Load ~300 lines every conversation
- Waste context on 90% of conversations (which are about tasks/ideas, not reviews)
- Reduce effectiveness on common tasks

**Solution:** "Router pattern"
- CLAUDE.md: 4 lines (lightweight pointer)
- 360_review_workflow.md: 300 lines (loaded only when needed)
- Result: Optimal context usage

**User insight:** "I know you perform better when the information in a file is only at the level you need to complete a task."

### Decision 4: Workflow = PROCESS, Reference = CONTENT (no duplication)
**Problem found:** Initial workflow duplicated CARE method definitions from assessment guide
**Fix:** Workflow references guide instead of duplicating
**Principle:** Single source of truth - update criteria in one place

**User quote:** "Why did you include the information from the assessment guide into the workflow file, rather than read performance_assessment guide and use it as context?"

### Decision 5: Validation step before synthesis
**Requirement:** Show all input documents before starting review
**Reasoning:**
- Quality control (catch missing inputs early)
- Transparency (user sees what's being used)
- Confidence (explicit confirmation before work begins)

### Decision 6: Peer feedback prioritization (NEW - not yet implemented)
**Issue:** Initial 360 review felt too weighted toward self-assessment
**Solution:** 70% peer feedback, 30% self-assessment in evidence weighting
**Additional changes:** Separate improvements section, 50/50 balance, shorter length

---

## 3. Technical Implementation

### Architecture Pattern: Router + On-Demand Loading

```
Lightweight Router (CLAUDE.md)
    ↓ points to
Detailed Workflow (360_review_workflow.md)
    ↓ references
Reference Documents (guide, OKRs, behaviors)
    ↓ synthesizes
Individual Inputs (self-assessment, peer feedback)
```

### Technologies:
- Python scripts for command parsing and file creation
- Markdown for all documents (Obsidian integration)
- YAML frontmatter for metadata
- Bash for file operations
- Git for version control

### Design Patterns:
1. **Command pattern** - Natural language triggers parsed and routed
2. **Router pattern** - Lightweight pointers to detailed workflows
3. **Template pattern** - Consistent file structures across all items
4. **Validation pattern** - Checklist confirmation before execution

---

## 4. Code Changes Summary

### Created Files:

**`Work/Team/Observations/`** (folder)
- **Purpose:** Store all observation files about team members
- **Naming:** `observation_[Name]_[Date].md`

**`Work/Team/360_reviews/`** (folder structure)
- **Purpose:** Store 360 review documents and supporting files
- **Structure:**
  - Individual folders: `[FirstName]_[LastName]/`
  - Shared references: assessment guide, OKRs, behaviors
  - Workflow file

**`scripts/create_observation.py`**
- **Purpose:** Create observation files with date-based naming
- **Key functions:**
  - `create_observation()` - Main creation function
  - `create_observation_frontmatter()` - YAML generation
  - `create_observation_content()` - Markdown content
  - `create_360_review()` - Generate 360 review template
- **Features:**
  - Extracts team member name from "Name - observation" format
  - Auto-generates date-based filenames
  - Handles duplicates with timestamp suffix
  - Creates 360 template files with comprehensive structure

**`scripts/utils.py`** (modified)
- **Added functions:**
  - `get_team_path()` - Returns Team folder path
  - `get_observations_path()` - Returns Observations folder path
  - `get_360_reviews_path()` - Returns 360 reviews folder path
  - `extract_team_member_name()` - Parse name from title

**`scripts/parse_command.py`** (modified)
- **Added functions:**
  - `is_observation_command()` - Detect observation triggers
  - `parse_observation_command()` - Parse observation fields
- **Modified:** `execute_command()` to handle observation and 360 commands
- **Triggers supported:**
  - Observations: "observation:", "I have feedback:", "feedback:"
  - 360 reviews: "360 review:", "360:", "360 [Name]", "review [Name]"

**`pos`** (modified)
- **Purpose:** Updated help text with observation and 360 examples
- **Added examples:**
  - `./pos "observation: Sarah - Great presentation..."`
  - `./pos "360 review: Sarah Johnson"`

**`Work/Team/360_reviews/360_review_workflow.md`**
- **Purpose:** Detailed process for generating comprehensive 360 reviews
- **Structure:** 7-step workflow from discovery to delivery
- **Key features:**
  - Document discovery and validation
  - Input checklist with confirmation
  - CARE framework application
  - Quality checks
- **Length:** ~300 lines (loaded on demand)

**`Work/Team/360_reviews/performance_assessment_guide.md`**
- **Purpose:** Assessment criteria and frameworks
- **Content:** CARE method, WHAT/HOW dimensions, One ORBIT behaviors
- **Source:** Provided by user

**`Work/Team/360_reviews/One_Orbit_behaviours.md`**
- **Purpose:** Detailed One ORBIT behavioral framework
- **Source:** Provided by user

**`Work/Team/360_reviews/Q3 OKRs - for H2.md`** & **`Q4 - OKRs (updated for H2).md`**
- **Purpose:** Strategic context for outcome validation
- **Source:** Provided by user

### Modified Files:

**`CLAUDE.md`** (Project)
- **Added:** Observation command documentation
- **Added:** 360 review command documentation (lightweight)
- **Updated:** Team feedback commands section
- **Changes:** Clear separation between quick file creation and synthesis tasks

**`README.md`**
- **Added:** Observation command examples
- **Added:** 360 review command examples
- **Updated:** Project structure diagram
- **Added:** File format examples for observations and 360 reviews

---

## 5. Commands & Setup

### New Commands Available:

**Observation Commands:**
```bash
# Create observation
./pos "observation: Name - observation details: text tags: tag1, tag2"
./pos "I have feedback: Name - feedback text tags: teamwork"

# Examples
./pos "observation: Sarah Johnson - Great presentation details: Excellent communication tags: leadership"
```

**360 Review Commands:**
```bash
# Create empty 360 template
./pos "360 review: Full Name"

# Generate comprehensive review (synthesis task)
# Just say: "360 FirstName"
360 Anders
review Chris
generate 360 for Sarah
```

### File Naming Conventions:
- Observations: `observation_[Name]_[YYYY-MM-DD].md`
- 360 Reviews: `360_[Name]_FY26.md`
- Person folders: `[FirstName]_[LastName]/`

### Folder Structure:
```
Work/Team/
├── Observations/
│   └── observation_*.md
└── 360_reviews/
    ├── [Person folders]/
    │   ├── self_assessment.md
    │   ├── peer_feedback_*.md
    │   └── 360_[Name]_FY26.md
    ├── performance_assessment_guide.md
    ├── One_Orbit_behaviours.md
    ├── Q3 OKRs - for H2.md
    ├── Q4 - OKRs (updated for H2).md
    └── 360_review_workflow.md
```

---

## 6. Problems Solved

### Problem 1: Excel file not readable
**Issue:** User added Excel file to person's folder but it wasn't showing in Obsidian and Claude can't read binary files
**Solution:** Convert to markdown or CSV format
**File affected:** `Feedback_On_My_Team_and_Next_Level_Subordinate_Organization.xlsx`
**Status:** User needs to convert (provided instructions)

### Problem 2: Permission prompts for file listing
**Issue:** During "360 Anders" test, permission prompt appeared for `ls` command
**Root cause:** Multiple redundant file discovery commands
**Solution:**
- Be more efficient with initial file discovery
- User can click "don't ask again for ls commands in this path"
- Updated CLAUDE.md to emphasize proactive automation

### Problem 3: Context window waste
**Issue:** Detailed 360 workflow in CLAUDE.md would load every conversation
**Impact:** Reduced effectiveness on common tasks (90% of conversations)
**Solution:** Router pattern - 4-line pointer in CLAUDE.md, detailed workflow loaded on demand
**Learning:** Optimize for common case, not edge cases

### Problem 4: Content duplication
**Issue:** Workflow file duplicated CARE method definitions from assessment guide
**Impact:**
- Single source of truth violated
- Harder to maintain
- Redundant context loading
**Solution:** Workflow references guide instead of duplicating content
**Principle:** Workflow = PROCESS, Reference docs = CONTENT

### Problem 5: Missing validation step
**Issue:** Review generation could start without confirming all inputs present
**Solution:** Added Step 3 to workflow - validate inputs and get confirmation
**Benefits:** Quality control, transparency, early error detection

### Problem 6: Review output issues (identified, not yet fixed)
**Issues:**
- Too long (~3000 words)
- Too weighted toward self-assessment
- Too positive (70% strengths, 30% improvements)
- Areas for improvement buried in other sections
- No peer feedback summary at start

**Solution planned:** See Pending Items section

---

## 7. Pending Items

### 1. Update Global CLAUDE.md
**Status:** Approved, not yet implemented
**Changes needed:**
- Add section on task management (checklists, showing thinking)
- Add section on context window efficiency principles
- Add section on multi-file architecture patterns
- Add section on critical thinking partnership

### 2. Update Project CLAUDE.md
**Status:** Approved, not yet implemented
**Changes needed:**
- Add complex workflow pattern documentation
- Add automation expectations
- Add validation pattern for multi-input tasks
- Add lessons learned section

### 3. Revise 360 Review Workflow
**Status:** Approved, not yet implemented
**Changes needed:**

**Step 4 (Analysis):**
- Add peer feedback prioritization (70% peer, 30% self)
- Add guidance on evidence hierarchy
- Emphasize corroboration between sources

**Step 5 (Structure):**
- NEW: Peer Feedback Summary at start (300-400 words)
- Shorten Executive Summary to 150-200 words
- Separate "Areas for Improvement" section (300-400 words)
- Equal space for strengths and improvements (50/50)
- Reduce total length to 1500-2000 words

**Step 6 (Quality Check):**
- Add checks for peer feedback primacy
- Add checks for length targets
- Add checks for 50/50 balance

### 4. Excel File Conversion
**Status:** User action required
**File:** `Anders_Webster/Feedback_On_My_Team_and_Next_Level_Subordinate_Organization.xlsx`
**Action:** Convert to markdown or CSV format
**Options provided:** Markdown table, CSV export, or selective content copy

### 5. Test Complete 360 Review Generation
**Status:** Not yet tested with all improvements
**Next:** After workflow updates are complete, test full "360 Anders" workflow

---

## 8. User Preferences & Context

### Working Style:
- **Critical thinking partnership:** User wants pushback, not just agreement
- **Context optimization awareness:** Sophisticated understanding of LLM performance
- **Clean architecture preference:** "Simple and clean" - avoids over-engineering
- **Evidence-based decisions:** Wants to see the data/output before agreeing

### Key Insights:
1. **Context efficiency matters:** User caught that loading 360 workflow every conversation would reduce effectiveness
2. **Separation of concerns:** Strong preference for modular, single-purpose files
3. **Automation with confirmation:** Wants proactive discovery but explicit confirmation before major work
4. **Transparency:** Wants to see what inputs are being used (validation checklist)

### Domain Context:
- **Autodesk employee:** One ORBIT is company-specific behavioral framework
- **People manager:** Conducting 360 reviews for team members
- **Performance review context:** FY26, H2 period, using CARE method
- **OKR-driven:** Outcomes evaluated against Q3/Q4 OKRs

### Communication Preferences:
- Direct and professional
- Wants to understand the "why" behind decisions
- Appreciates when Claude admits mistakes ("I was wrong")
- Values intellectual honesty over false agreement

### Quotes that reveal preferences:
- "I want you to act like a critical brainstorm partner and not agree with me if you disagree"
- "I know you perform better when the information in a file is only at the level you need to complete a task"
- "I want to keep things very simple and clean"

---

## 9. Next Steps

### Immediate (This Session):
1. ✅ Create this project summary
2. 🔄 Update Global CLAUDE.md with task management principles
3. 🔄 Update Project CLAUDE.md with workflow patterns
4. 🔄 Revise 360_review_workflow.md with new synthesis guidance
5. ✅ Commit all changes

### Short Term (Next Session):
1. Convert Excel file to readable format
2. Test complete 360 review generation with Anders
3. Validate new review structure and length
4. Iterate on balance and content based on output

### Future Enhancements:
1. Add observation summary command (view all observations for a person)
2. Auto-link observations into 360 review files
3. Template for setting up new team member folders
4. Analytics on observation patterns and themes

---

## 10. Quick Reference

### Key File Locations:

**Configuration:**
- Global preferences: `/Users/smallc/AI/CLAUDE.md`
- Project config: `/Users/smallc/AI/Chief_of_staff/CLAUDE.md`

**Team Feedback:**
- Observations: `Work/Team/Observations/`
- 360 Reviews: `Work/Team/360_reviews/`
- Workflow: `Work/Team/360_reviews/360_review_workflow.md`

**Scripts:**
- Observation creation: `scripts/create_observation.py`
- Command parsing: `scripts/parse_command.py`
- Utilities: `scripts/utils.py`

**Documentation:**
- Project README: `README.md`
- This summary: `project_summary.md`

### Important Commands:

```bash
# Create observation
./pos "observation: Name - text details: text tags: tags"

# Generate 360 review
# Just say: "360 FirstName"

# View today's summary
./pos "/today"

# Commit changes
git add [files]
git commit -m "message"
git push origin main
```

### Key Patterns Established:

**Router Pattern:**
```
CLAUDE.md (4 lines) → workflow_file.md (detailed) → reference_docs.md (criteria)
```

**Validation Pattern:**
```
1. Discover inputs
2. Show checklist
3. Get confirmation
4. Execute synthesis
```

**Evidence Hierarchy:**
```
Strong: Multiple peer sources agree
Moderate: Peer + self-assessment align
Weak: Only self-assessment, no peer support
```

---

## Git History

### Commits Made:
1. **"Add team feedback observation feature"** (d5536b9)
   - Added observation command
   - Created Team folder structure
   - Updated documentation
   - 10 files changed, 351 insertions

### Repository:
- URL: https://github.com/autodesk-chris/chief-of-staff
- Branch: main
- Status: Pushed to remote

---

## Architecture Lessons Learned

### Context Window Optimization:
- ✅ Optimize for the 80% use case
- ✅ Load specialized workflows on demand
- ✅ Keep CLAUDE.md lightweight and focused
- ✅ Use router pattern for complex workflows

### File Architecture:
- ✅ Workflow files: PROCESS only
- ✅ Reference files: CONTENT/CRITERIA only
- ✅ Never duplicate between files
- ✅ Single source of truth always

### Critical Thinking:
- ✅ Challenge assumptions before agreeing
- ✅ Explain trade-offs honestly
- ✅ Say "I was wrong" when appropriate
- ✅ Present alternatives with honest analysis

---

**End of Project Summary**
