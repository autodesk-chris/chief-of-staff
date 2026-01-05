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

### Status Updates (Primary Method)

When the user asks to mark something as complete, blocked, in progress, etc., **immediately use the update command**. Do not search for files first - fuzzy matching handles it automatically.

**Command syntax:**
```bash
./pos "update: [item title] status: [status]"
./pos "update: [item title] status: [status] note: [optional note]"
```

**Available status values:**
- `active` - Currently actionable
- `in-progress` - Actively working on it
- `blocked` - Cannot proceed (add note explaining why)
- `waiting` - Waiting on someone/something
- `on-hold` - Paused temporarily
- `completed` - Finished
- `archived` - No longer relevant

**Examples:**
```bash
./pos "update: Follow up with Gail status: completed"
./pos "update: Review monetisation status: blocked note: Waiting for budget approval"
./pos "update: Draft offsite presentation status: in-progress note: Starting research"
```

**User workflow translation:**
- User says: "mark follow-up gail task as complete"
- You run: `./pos "update: Follow up with Gail status: completed"`
- User says: "update the offsite budget"
- You ask: "What status would you like to set? (active, in-progress, blocked, waiting, on-hold, completed, archived)"
- User responds: "blocked, waiting for finance"
- You run: `./pos "update: offsite budget status: blocked note: Waiting for finance"`

**How it works:**
- Fuzzy matching finds items automatically - no need to search first
- Works across all item types (tasks, ideas, features, actions)
- Auto-updates today document after status change
- Handles files with or without existing status fields

**When user doesn't specify status:**
- The command will error with: "Status is required. Please specify: status: [...]"
- Ask the user: "What status would you like to set?" and provide the options
- Then run the command with their chosen status

**Don't do this:**
- ❌ Search for files with Glob/Grep before updating
- ❌ Read files to confirm existence
- ❌ Look for exact filenames
- ✅ Just run the update command - it handles everything

### Task Creation Best Practices

When creating tasks from user input, extract short, meaningful titles:

**Title extraction:**
- Keep titles short and succinct (3-8 words maximum)
- Extract core action + primary subject
- Format: [Verb] + [Subject] + [Optional context]
- Move detailed context, background, and specifics to the details field

**Examples:**

*Input:* "new task: I need to prepare the quarterly business review presentation for the executive team including slides on revenue, customer metrics, and product roadmap"
- **Title:** "Prepare quarterly business review presentation"
- **Details:** "For executive team. Include slides on revenue, customer metrics, and product roadmap."

*Input:* "new task: Follow up with Sarah about the API integration issue she mentioned in the standup this morning where the authentication tokens are expiring too quickly and causing customer complaints"
- **Title:** "Follow up with Sarah on API authentication"
- **Details:** "Authentication tokens expiring too quickly, causing customer complaints. Mentioned in standup this morning."

*Input:* "new task: Review and provide feedback on the new hiring process documentation that HR sent over, focusing on whether it aligns with our team's needs for the engineering roles we're planning to hire for in Q2"
- **Title:** "Review hiring process documentation"
- **Details:** "From HR. Focus on alignment with team needs for Q2 engineering roles."

**Principles:**
- **Actionable:** Title starts with verb when possible
- **Scannable:** Easy to read in task lists
- **Specific enough:** Clear what the task is about
- **Context preserved:** Everything else goes in details field
- **Due dates and tags:** Extract separately and preserve

**Date extraction:**
- Look for dates mentioned in the task text (e.g., "next Friday", "January 15th", "by end of month")
- Extract and convert to YYYY-MM-DD format for the due date field
- If date is ambiguous or unclear, ask the user to confirm
- Remove date references from details field after extracting to avoid duplication

**Example:**
*Input:* "new task: Send proposal to client by next Wednesday and make sure to include the pricing breakdown"
- **Title:** "Send proposal to client"
- **Due:** [Calculate next Wednesday in YYYY-MM-DD format]
- **Details:** "Include pricing breakdown"

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
