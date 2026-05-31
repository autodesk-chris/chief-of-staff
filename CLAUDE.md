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
| **Tasks** | `new task:`, `update:`, `/todo`, `process notepad` | Task, idea, feature, reminder, action management |
| **People** | `observation:`, `360:`, `feedback:`, `performance conversation prep:` | Observations, 360 reviews, performance conversations |
| **Strategy** | Query-based (OKR, strategy, bet keywords) | Strategic analysis with progressive L1→L2→L3 disclosure + Confluence |
| **Reflection** | `daily summary`, `/summary`, `session:`, `slack report`, `scan slack`, `4ps roundup`, `leadership update` | Daily summaries, session logging, Slack reports, commitment scanning, team 4Ps, leadership updates |
| **Meetings** | `prep meeting:`, `121:`, `post meeting:` | Meeting prep, Granola integration |
| **MFM** | `mfm review:`, `mfm summary:`, `run [month] monthly focus meeting for [squad]` | Monthly Focus Meeting reviews (Confluence input) and summaries |
| **Hiring** | `setup role:`, `screen CVs:`, `shortlist:`, `interview prep:`, `interview eval:` | CV screening, interview evaluation, candidate assessment |

### Natural language routing

**Always route through Julie first.** When a user's natural language request maps to an existing agent command or skill, use that command/skill rather than doing the work manually. If unsure which command fits, ask.

Common mappings:
- "prepare for my 1:1 with X" / "I have a check-in with X" = `./pos "121: X"`
- "prep for [meeting]" = `./pos "prep meeting: [meeting]"`
- "I have feedback about X" = `./pos "observation: X - [feedback]"`

All other workflows (post-meeting, coaching prep/review, call reflection, session logging, daily summary, 4Ps, todo, notepad processing, role expectations, strategy review, presentations) are auto-discovered via skill descriptions in `.claude/skills/*/SKILL.md`.

### Key locations

- **Agent personas:** `.claude/personas/AGENT_*.md`
- **Skills:** `.claude/skills/*/SKILL.md`
- **Command routing:** `scripts/detect_agent.py`
- **Memory system:** claude-mem MCP with project partitioning
- **Obsidian vault:** `Work/`

### Quick command reference

```bash
# Tasks
./pos "new task: [title] due: [YYYY-MM-DD] details: [text] tags: [tag1, tag2]"
./pos "update: [title] status: [completed|in-progress|blocked|waiting]"
./pos "/todo"                           # Generate daily to-do list
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
./pos "run [month] monthly focus meeting for [squad]"  # Natural language MFM trigger

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

**User workflow translation:**
- User says: "mark follow-up gail task as complete"
- You run: `./pos "update: Follow up with Gail status: completed"`
- User says: "update the offsite budget"
- You ask: "What status would you like to set?" and provide the options

**Don't do this:**
- Don't search for files with Glob/Grep before updating
- Don't read files to confirm existence
- Just run the update command - fuzzy matching handles everything

### Archiving Completed Items

```bash
./pos "archive completed"
```

Finds items with status `completed` and `completed-date` older than 7 days, moves them to `Work/Archive/{Type}s/YYYY-MM/`. Run periodically to keep inbox clean.

### Task Creation Best Practices

When creating tasks from user input, extract short, meaningful titles:

- Keep titles short and succinct (3-8 words maximum)
- Format: [Verb] + [Subject] + [Optional context]
- Move detailed context, background, and specifics to the details field
- Extract dates and convert to YYYY-MM-DD for the due date field

**Example:**
*Input:* "new task: Follow up with Sarah about the API integration issue she mentioned in standup"
- **Title:** "Follow up with Sarah on API authentication"
- **Details:** "Authentication tokens expiring too quickly, causing customer complaints. Mentioned in standup this morning."

## Team Feedback Commands

### Observation Commands

- **Trigger phrases**: "observation:", "I have feedback:", "feedback:"
- **Required format**: `Name - observation text` (name before dash is required)
- **Files stored in**: `Work/People/Observations/`
- **Filename format**: `observation_[name]_[date].md`
- If name format is incorrect, ask the user conversationally for the proper format

### 360 Review Commands

**Quick 360 file creation:**
- **Trigger**: "360 review: [Name]" or "360: [Name]"
- Creates empty template file at `Work/People/360_reviews/360_[name]_FY26.md`

**360 Review Generation (synthesis task):**
- **Trigger**: "360 [FirstName]", "review [Name]", or "generate 360 for [Name]"
- **Process**: Read `Work/People/360_reviews/360_review_workflow.md` for detailed instructions
- Immediately list files in person's folder and shared reference folder (no permission needed)
- Show document checklist to user, then proceed with synthesis after confirmation

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

## Memory systems

Four memory layers are available, each serving a different purpose:

| Layer | Location | Loaded | Maintained by | Best for |
|-------|----------|--------|---------------|----------|
| **CLAUDE.md** | Project root + parent dirs | Always | User | Stable operating instructions, project structure, command reference |
| **Auto-memory** | `.claude/projects/.../memory/` | MEMORY.md always; topic files on demand | Claude | Patterns about user (writing style, preferences, relationship context, recurring references) |
| **claude-mem** | External MCP database | Index at session start; details via search | Claude (automatic) | Work history - past research, decisions, discoveries. Searchable and timestamped |
| **LLM_Context** | `Work/LLM_Context/` | Only when task points there | User | Domain knowledge too large for memory files (strategies, frameworks, playbooks, team structures) |

**When to store where:**
- "How to work" instructions go in **CLAUDE.md**
- Stable patterns about the user go in **auto-memory** (tell Claude "remember this")
- Large reference documents go in **LLM_Context** (and reference them from CLAUDE.md if they should be found automatically)
- Work journal entries accumulate automatically in **claude-mem**

**User commands:**
- "Remember that I always want X" - saves to auto-memory
- "Forget that" / "Stop remembering X" - removes from auto-memory
- "Did we already look into X?" / "What did we find last time?" - searches claude-mem

## Analytics context

Before any analytics work (direct queries or invoking analytics skills), read `Work/LLM_Context/Analytics/site_design_events.md` for verified event names, query patterns, and corrections. Include relevant context (especially corrections like deprecated event names) when delegating to analytics skills. Key points:
- Page name `"DesignMode"` is deprecated - use `"Site Design"`
- Use `Loaded a Page` with `name` filter for MAU, not `product` property
- Use `site_design_analysis_run` for analysis events, not `Activation: Triggered Analysis` (dead) or `Any Forma Analysis` (black box)
- Full research log at `Work/Notes/Data/data_understanding_site_design_analytics.md`

## Automation Expectations

For this project, be **proactive and automated**:

**Do automatically (no permission needed):**
- File discovery: List files in Work/People folders
- Document reading: Read required files
- Command execution: Execute ./pos commands
- Git status: Check repository state

**Do confirm before:**
- Major synthesis work (360 reviews)
- Writing/creating files
- Git commits and pushes
- Destructive operations

## Validation Pattern for Multi-Input Tasks

For tasks requiring 5+ input documents (like 360 reviews):

1. **Discover** - Automatically find and list all inputs
2. **Present** - Show checklist of what was found
3. **Confirm** - Get explicit approval before proceeding
4. **Execute** - Proceed with synthesis/analysis
