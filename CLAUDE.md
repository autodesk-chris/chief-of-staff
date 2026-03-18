# Chief of Staff - Project Context

This file contains project-specific instructions for the Chief of Staff Personal OS project.

## Julie: Hierarchical Agent System

Julie is a hierarchical agent architecture where specialized agents handle different domains. Commands are automatically routed to the appropriate agent based on pattern matching.

### Architecture overview

```
┌─────────────────────────────────────────────────────────────┐
│                      User Input                              │
│                    (./pos "command")                         │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Command Parser                             │
│                (scripts/parse_command.py)                    │
│                                                              │
│  Detects agent via pattern matching → routes to specialist   │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌───────────┐   ┌───────────┐   ┌───────────┐
    │   Tasks   │   │  People   │   │ Strategy  │
    │   Agent   │   │   Agent   │   │   Agent   │
    └───────────┘   └───────────┘   └───────────┘
    ┌───────────┐   ┌───────────┐   ┌───────────┐
    │Reflection │   │ Meetings  │   │    MFM    │
    │   Agent   │   │   Agent   │   │   Agent   │
    └───────────┘   └───────────┘   └───────────┘
    ┌───────────┐
    │  Hiring   │
    │   Agent   │
    └───────────┘
```

### Specialized agents

| Agent | Commands | Role |
|-------|----------|------|
| **Tasks** | `new task:`, `update:`, `/today`, `process notepad` | Task, idea, feature, reminder, action management |
| **People** | `observation:`, `360:`, `feedback:`, `performance conversation prep:` | Observations, 360 reviews, performance conversations |
| **Strategy** | Query-based (OKR, strategy, bet keywords) | Strategic analysis with progressive L1→L2→L3 disclosure + Confluence |
| **Reflection** | `daily summary`, `/summary`, `session:`, `slack report`, `scan slack`, `4ps roundup`, `leadership update` | Daily summaries, session logging, Slack reports, commitment scanning, team 4Ps, leadership updates |
| **Meetings** | `prep meeting:`, `121:`, `post meeting:` | Meeting prep, Granola integration |
| **MFM** | `mfm review:`, `mfm summary:` | Monthly Focus Meeting reviews and summaries |
| **Hiring** | `setup role:`, `screen CVs:`, `shortlist:`, `interview prep:`, `interview eval:` | CV screening, interview evaluation, candidate assessment |

### Key locations

- **Agent personas:** `.claude/personas/AGENT_*.md`
- **Command routing:** `scripts/detect_agent.py`
- **Memory system:** claude-mem MCP with project partitioning
- **Obsidian vault:** `Work/`

### Quick command reference

```bash
# Tasks
./pos "new task: [title] due: [YYYY-MM-DD] details: [text] tags: [tag1, tag2]"
./pos "update: [title] status: [completed|in-progress|blocked|waiting]"
./pos "/today"                          # Generate today's task summary
./pos "process notepad"                 # Process captured notes
./pos "archive completed"               # Archive items completed > 7 days ago

# People
./pos "observation: [Name] - [observation text]"
./pos "360: [Name]"                     # Generate full 360 review
./pos "performance conversation prep: [Name]"  # Create conversation guide from 360

# Meetings
./pos "prep meeting: [meeting title]"   # Prepare for upcoming meeting
./pos "121: [person name]"              # Prepare for 1:1
./pos "post meeting: [meeting title]"   # Process meeting notes

# Reflection
./pos "session: [summary of work]"      # Log work session
./pos "daily summary"                   # End-of-day interview
./pos "slack report"                    # Comprehensive Slack report
./pos "scan slack"                      # Scan Slack for commitments, extract tasks/actions
./pos "4ps roundup"                     # Review team 4Ps from Slack vs MFM priorities
./pos "leadership update"               # Synthesize leadership channels into update

# MFM
./pos "mfm review: [squad] [month]"     # Review MFM pre-read
./pos "mfm summary: [squad] [month]"    # Create post-MFM summary

# Hiring
./pos "setup role: [role name]"         # Generate evaluation guide from JD
./pos "screen CVs: [role name]"         # Batch screen all CVs in folder
./pos "review CV: [name] for [role]"    # Screen single CV
./pos "shortlist: [name] for [role]"    # Move CV + create screen notes + interview prep
./pos "interview prep: [name] for [role]" # Generate interview questions
./pos "interview eval: [name] for [role]" # Full evaluation with Granola + CV
./pos "candidate summary: [name]"       # Generate shareable notes
```

---

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
- Observation commands operate on `./Work/People/Observations/`
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

### Archiving Completed Items

To prevent inbox folders from accumulating hundreds of completed items, use the archive command periodically.

**Command:**
```bash
./pos "archive completed"
```

**What it does:**
- Finds all items with status `completed` and a `completed-date` older than 7 days
- Moves them to `Work/Archive/{Type}s/YYYY-MM/` folders (organized by completion month)
- Returns a summary of what was archived

**Archive folder structure:**
```
Work/Archive/
├── Tasks/
│   ├── 2026-01/
│   ├── 2026-02/
│   └── 2026-03/
├── Ideas/
├── Features/
├── Actions/
└── Reminders/
```

**Notes:**
- Items completed in the last 7 days stay in the inbox for easy reference
- Only items with a `completed-date` field are archived (automatically added when marking complete)
- Archived files preserve their original names and content
- Run periodically (weekly/monthly) to keep inbox folders clean

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

## Notepad Processing

**Purpose:** Frictionless capture → structured processing → organized storage

**Three-stage workflow:**

1. **Capture** (ongoing)
   - Write anything to Work/1-Notepad/Notepad.md
   - No structure needed, no categorization needed
   - Just brain dump - mix of actionable and strategic thinking
   - Central notepad is for fast, frictionless capture

2. **Process** (when ready)
   - Run: `./pos "process notepad"`
   - Script splits notepad into sections
   - Classifies each section as actionable or strategic
   - Checks memory for duplicate tasks
   - **Shows classification results and asks for confirmation**
   - Creates tasks/actions/reminders/features/decisions from actionables
   - Routes strategic thinking to domain-specific notepads
   - Archives processed content with timestamp
   - Clears central notepad

3. **Digest** (in context - future phases)
   - Review domain notepads when working in that area
   - Strategy work → Work/Notes/Strategy/notepad.md
   - People work → Work/People/notepad.md
   - Meeting prep → Work/Meetings/Prep/notepad.md
   - Ideas → Work/Inbox/Ideas/notepad.md
   - Domain agents will have "digest" commands to process their notepads

**Classification logic:**

**Actionable** (creates items):
- Tasks: Clear action with deliverable ("Review...", "Prepare...", "Schedule...")
- Actions: Work assigned to someone ("[Person] needs to...")
- Reminders: Things not to forget ("Remember to...", "Don't forget...")
- Features: Julie improvements ("I want Julie to...")
- Decisions: Decisions made ("Decided to...", "Decision:")

**Strategic** (routes to domain notepads):
- Strategy: OKRs, product strategy, high-level planning
- People: Team observations, 121 topics, feedback thoughts
- Meetings: Meeting prep ideas, discussion topics
- Ideas: Incomplete exploratory thoughts

**Key principles:**
- Conservative extraction (better to route to strategic than create wrong item)
- User confirmation before creating items
- Memory integration for duplicate detection
- Preserve original notepad in Archive/ with timestamp
- Central notepad cleared and ready for new capture

**Domain notepads:**
Each domain agent will later have a "digest [domain]" command to process their notepad into final documents/items (future phases).

**Files:**
- Central notepad: Work/1-Notepad/Notepad.md
- Archive: Work/1-Notepad/Archive/notepad_YYYY-MM-DD_HHMM.md
- Domain notepads: Work/Notes/Strategy/, Work/People/, Work/Meetings/Prep/, Work/Inbox/Ideas/

## Team Feedback Commands

### Observation Commands

- **Trigger phrases**: "observation:", "I have feedback:", "feedback:"
- **Required format**: `Name - observation text` (name before dash is required)
- **Files stored in**: `Work/People/Observations/`
- **Filename format**: `observation_[name]_[date].md`
- **Example**: `observation: Sarah Johnson - Great presentation details: Excellent communication tags: leadership`
- If name format is incorrect, the command will error and you should ask the user conversationally for the proper format

### 360 Review Commands

**Quick 360 file creation:**
- **Trigger**: "360 review: [Name]" or "360: [Name]"
- Creates empty template file at `Work/People/360_reviews/360_[name]_FY26.md`

**360 Review Generation (synthesis task):**
- **Trigger**: "360 [FirstName]", "review [Name]", or "generate 360 for [Name]"
- **Process**:
  1. Read `Work/People/360_reviews/360_review_workflow.md` for detailed instructions
  2. Immediately list files in person's folder and shared reference folder (no permission needed)
  3. Show document checklist to user
  4. After user confirmation, proceed with synthesis
- This is a multi-step synthesis task - be proactive and automated in file discovery

### Role Expectations Documents

**Trigger**: `/role-expectations [name]` or "create role expectations for [name]"

**Process**: Read and follow `.claude/skills/role-expectations.md`

Creates a two-section document:
1. **The destination** (executive summary) - outcome-focused vision
2. **Detailed expectations** - responsibilities with What/Key activities/Expectations format

**Example**: See `Work/People/121s/maria/Maria_expectations_pm_monetization.md`

## Daily Summary Commands

### Session Logging

**Purpose:** Log Claude work sessions throughout the day for automatic inclusion in daily summary

**Automated workflow (recommended):**

When the user types **"session"** in the Claude conversation (not in terminal), you should:

1. **Automatically review the entire conversation**
2. **Generate a structured summary** with:
   - 1-2 sentence overview at the top
   - Bullet points covering key topics, decisions, and outputs (as many as needed for clarity)
   - Enough detail for someone else to understand what was worked on
3. **Immediately run** `./pos "session: [generated summary]"` via Bash tool
4. **Confirm** the session was logged

**Summary format guidelines:**
- Start with brief overview sentence
- Use bullet points for details
- Include: topics discussed, decisions made, outputs created, problems solved
- Write for an external reader, not just the user
- Be concise but complete

**Example automated summary:**
```
Discussed session logging workflow in the Chief of Staff system and clarified how the daily summary commands work. Decided to implement an automated conversation review feature.

- Clarified difference between 'project summary' and daily summary interview commands
- Explained session logging creates one daily file with all sessions timestamped
- Explored batch logging options - user wanted automated conversation review
- Agreed on approach: user types 'session', Claude auto-generates summary and logs via Bash
```

**Manual command (if needed):**
```bash
./pos "session: [what you worked on]"
./pos "/session [summary]"
```

**Storage:** `Work/Daily_Logs/claude_sessions_YYYY-MM-DD.md`

**Format:** Timestamped entries appended to daily log file (one file per day, multiple sessions per file)

### Daily Summary Interview

**Purpose:** End-of-day interview conducted by Claude to capture summary of daily work for weekly 4Ps writing

**Trigger:** When user says "daily summary", "create daily summary", or similar

**When to use:** At end of work day (takes 3-5 minutes)

**Automated workflow:**

1. **Automatically gather context** (no permission needed):
   - Read this week's 4Ps from `Work/Weekly_4Ps/` (priorities and plans)
   - Read today summary from `Work/Inbox/Today/today_YYYY-MM-DD.md` (completed/in-progress tasks)
   - Read Claude session logs from `Work/Daily_Logs/claude_sessions_YYYY-MM-DD.md`
   - Read any observations created today from `Work/People/Observations/`

2. **Conduct interview IN the conversation**:
   - Use gathered context to inform questions
   - Ask 5-6 questions to supplement file contents:
     - What meetings did you have today, and what were the key takeaways?
     - What progress did you make on this week's plans?
     - What key decisions were made?
     - Any important Slack discussions or messages?
     - Any surprises or unexpected changes?
     - Anything else important to capture?
   - Let user answer each question in the conversation

3. **Collate and summarize**:
   - Combine file contents + user answers
   - Generate structured bullet-point summary
   - Include meetings, decisions, progress, Claude sessions, completed tasks

4. **Save summary**:
   - Write to `Work/Inbox/Today/summary_YYYY-MM-DD.md`
   - Confirm to user that summary was saved

**Key principle:** Files provide baseline context, interview fills in gaps (meetings, Slack discussions, decisions not captured elsewhere).

**Output format:**
- Bullet-point format
- Enough detail for team member to understand
- Key decisions highlighted
- Meetings summarized with takeaways
- Claude work sessions automatically included
- Links to related observations
- Progress on weekly plans noted

**Best practice workflow:**
1. Throughout day: Type "session" in Claude conversations to auto-log work
2. End of day: Type "daily summary" to conduct interview and generate summary
3. End of week: Use daily summaries to write 4Ps

**File naming:**
- Session logs: `Work/Daily_Logs/claude_sessions_YYYY-MM-DD.md`
- Daily summaries: `Work/Inbox/Today/summary_YYYY-MM-DD.md`
- Distinct from auto-generated: `Work/Inbox/Today/today_YYYY-MM-DD.md` (task lists)

### Today Summary (Smart Summary)

**Purpose:** Generate today's task summary with an intelligently condensed yesterday overview

**Trigger:** When user says "today", "show today", "today summary", or similar

**Automated workflow:**

1. **Generate base summary**: Run `./pos "/today"` via Bash tool
2. **Read the generated file**: `Work/Inbox/Today/today_YYYY-MM-DD.md`
3. **Extract yesterday overview section**: Get content between "## Yesterday's overview" and "## Overdue Tasks" (or next section)
4. **Summarize using LLM**: Process the yesterday overview to:
   - Keep meeting names (bold headers) but condense to 1-2 sentences focusing on outputs/decisions/actions
   - Condense other sections (decisions, actions, completed) to key highlights only
   - Aim for ~5-10 lines total for yesterday overview
   - Preserve the most actionable information
5. **Update the file**: Replace the yesterday overview section with the condensed version
6. **Display to user**: Show the updated today summary

**Summarization prompt guidelines:**
- Focus on outputs, decisions, and action items
- Remove verbose details that don't affect today's work
- Keep what the user needs to remember or act on
- Each meeting should be 1-2 sentences maximum
- Preserve formatting (bold headers, bullet points)

**Why this approach:**
- Detailed summaries remain in `summary_YYYY-MM-DD.md` files for 4Ps writing
- Today view stays concise and scannable
- No API costs (uses current Claude conversation)
- User gets context without information overload

**Example condensation:**
Before: 3 bullet points about budget meeting details
After: "Decided to allocate 70k across Community, Inbound, and Conferences, with focus on Community given resource constraints."

## MFM Reviews

When user asks to review an MFM or monthly focus meeting: Read `/Users/smallc/AI/Chief_of_staff/Work/LLM_Context/MFM_review_framework.md`

## Confluence integration

Julie has access to Confluence via the Atlassian MCP. The Strategy and MFM agents use it for live knowledge.

**CloudId:** `0e31f281-3568-4559-ae88-153abcdead38`
**Primary space:** `fdo` (Forma Design Org)

**Key pages:**
- Operating model: page `641971975`
- FY27 H1 Strategic Narrative: page `731183409`
- Product Strategy FY27+: page `761685470`
- AI Strategy: page `745484925`
- 5-Year Capability Roadmap: page `745484947`

**When to use:** Strategy queries asking for "latest" or "current", MFM prep (squad strategies/bets), operating model questions, OKR status checks.

**Quick access:**
```
mcp__atlassian__getConfluencePage(cloudId="0e31f281-3568-4559-ae88-153abcdead38", pageId="PAGE_ID", contentFormat="markdown")
mcp__atlassian__searchAtlassian(query="Forma Design [topic]")
```

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
- ✅ File discovery: List files in Work/People folders
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
