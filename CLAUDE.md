# Chief of Staff - Project Context

This file contains project-specific instructions for the Chief of Staff Personal OS project.

## Project Overview

This project builds a personal operating system that integrates Claude Code with Obsidian to manage tasks, ideas, and features through command-line automation.

## Project Structure

```
Chief_of_staff/
├── CLAUDE.md (this file - Claude operates from here)
├── PersonalOS_prd.md (product requirements)
├── README.md (project documentation)
├── scripts/ (Python scripts for commands - to be created)
├── Work/ (Obsidian vault)
│   ├── LLM_Context/ (reference files)
│   ├── Inbox/
│   │   ├── Tasks/
│   │   ├── Ideas/
│   │   └── Features/
│   ├── Notes/
│   └── Research/
└── .gitignore
```

## Obsidian Vault Location

- **Vault Path**: `/Users/smallc/AI/Chief_of_staff/Work/`
- **Inbox Path**: `/Users/smallc/AI/Chief_of_staff/Work/Inbox/`

## Development Guidelines

- Use Python for all automation scripts
- Follow the PRD specifications exactly for file formats and command syntax
- Test all commands with edge cases (special characters, missing fields, etc.)
- Keep scripts modular and well-documented
- Commit frequently with clear messages

## Command Implementation Notes

- Most commands operate on the Obsidian vault at `./Work/Inbox/` (relative to project root)
- Observation commands operate on `./Work/Team/Observations/`
- File naming must sanitize special characters and replace spaces with underscores
- YAML frontmatter must be properly formatted
- Date parsing should handle YYYY-MM-DD format
- Tags should be converted from comma-separated strings to YAML list format

## Team Feedback Commands

### Observation Commands

- **Trigger phrases**: "observation:", "I have feedback:", "feedback:"
- **Required format**: `Name - observation text` (name before dash is required)
- **Files stored in**: `Work/Team/Observations/`
- **Filename format**: `observation_[name]_[date].md`
- **Example**: `observation: Sarah Johnson - Great presentation details: Excellent communication tags: leadership`
- If name format is incorrect, the command will error and you should ask the user conversationally for the proper format

### 360 Review Commands

**Quick 360 file creation:**
- **Trigger**: "360 review: [Name]" or "360: [Name]"
- Creates empty template file at `Work/Team/360_reviews/360_[name]_FY26.md`

**360 Review Generation (synthesis task):**
- **Trigger**: "360 [FirstName]", "review [Name]", or "generate 360 for [Name]"
- **Process**:
  1. Read `Work/Team/360_reviews/360_review_workflow.md` for detailed instructions
  2. Immediately list files in person's folder and shared reference folder (no permission needed)
  3. Show document checklist to user
  4. After user confirmation, proceed with synthesis
- This is a multi-step synthesis task - be proactive and automated in file discovery

## Complex Workflow Pattern

This project uses a **router pattern** for complex, specialized workflows:

**Example: 360 Review Generation**
- CLAUDE.md: Lightweight trigger recognition (4 lines)
- 360_review_workflow.md: Detailed step-by-step process (loaded on demand)
- reference_docs.md: Assessment criteria and frameworks

**When to use this pattern:**
- Workflow is complex (5+ steps)
- Used infrequently (<20% of conversations)
- Requires multiple reference documents
- Benefits from detailed documentation

**Benefits:**
- Keeps CLAUDE.md lean and focused
- Context loaded only when needed
- Optimizes performance for common tasks

## Automation Expectations

For this project, be **proactive and automated**:

**Do automatically (no permission needed):**
- ✅ File discovery: List files in Work/Team folders
- ✅ Document reading: Read required files
- ✅ Command execution: Execute ./pos commands
- ✅ Git status: Check repository state

**Don't ask permission for:**
- Directory listings in project folders
- Reading markdown/CSV files
- Basic file operations

**Do confirm before:**
- Major synthesis work (360 reviews)
- Writing/creating files
- Git commits and pushes
- Destructive operations

**Balance:** Automate discovery and reading, but confirm before major synthesis or file creation.

## Validation Pattern for Multi-Input Tasks

For tasks requiring 5+ input documents (like 360 reviews):

**Process:**
1. **Discover** - Automatically find and list all inputs
2. **Present** - Show checklist of what was found
3. **Confirm** - Get explicit approval before proceeding
4. **Execute** - Proceed with synthesis/analysis

**Why this works:**
- Quality control (catch missing inputs early)
- Transparency (user sees what's being used)
- Confidence (no surprises)
- Efficiency (no micromanaging the discovery phase)

## Lessons from 360 Review Implementation

**Context efficiency matters:**
The 360 review workflow is detailed (~300 lines) but only used occasionally. Keeping it in a separate file prevents cluttering context for common tasks like creating tasks/ideas/observations.

**Architecture that worked:**
- CLAUDE.md: 4 lines pointing to workflow
- 360_review_workflow.md: Process only (HOW to do it)
- performance_assessment_guide.md: Criteria and frameworks (WHAT to evaluate)
- One_Orbit_behaviours.md: Behavioral definitions (referenced, not copied)

**Key insight:**
Optimize CLAUDE.md for the 80% use case, not the 20% edge cases. Most conversations are about tasks, ideas, and observations - not 360 reviews.

## Testing Checklist

Before marking any stage complete:
- [ ] Test with normal inputs
- [ ] Test with special characters in titles
- [ ] Test with missing optional fields
- [ ] Test with very long descriptions
- [ ] Verify file is created in correct location
- [ ] Verify frontmatter is properly formatted
- [ ] Verify content matches expected format
