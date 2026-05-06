# Chief of Staff - Personal OS

A personal operating system powered by Claude Code that streamlines daily workflows through an intelligent multi-agent architecture called Julie.

## Overview

Chief of Staff integrates Claude Code with an Obsidian vault to provide:
- Intelligent command routing to specialized agents
- Task, idea, and feature management
- Team feedback and 360 review workflows
- Meeting preparation with Granola integration
- Strategic analysis with progressive context disclosure
- Daily summaries and reflection workflows

## Julie: Agent Architecture

Julie uses a hierarchical agent system where specialized agents handle different domains:

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
```

### Specialized agents

| Agent | Role | Key Commands |
|-------|------|--------------|
| **Tasks** | Task, idea, feature, action management | `new task:`, `update:`, `/todo` |
| **People** | Observations, 360 reviews, team feedback | `observation:`, `360:`, `feedback:` |
| **Strategy** | OKR analysis, strategic insights | Query-based (uses L1→L2→L3 progressive disclosure) |
| **Reflection** | Daily summaries, session logging | `daily summary`, `session:` |
| **Meetings** | Meeting prep, post-meeting processing | `prep meeting:`, `121:`, `post meeting:` |
| **MFM** | Monthly Focus Meeting reviews | `mfm review:`, `mfm summary:` |
| **Hiring** | CV screening, interview evaluation | `review CV:`, `screen CVs:`, `interview eval:` |

## Installation

### Requirements
- Python 3.8+
- Claude Code CLI
- Obsidian (optional, for vault visualization)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/autodesk-chris/chief-of-staff.git
cd chief-of-staff
```

2. Ensure the `pos` script is executable:
```bash
chmod +x pos
```

3. (Optional) Open Obsidian and point it to the `Work/` folder

## Usage

### Quick start

Use `./pos` to interact with your Personal OS:

```bash
# Create items
./pos "new task: Review Q1 report due: 2026-03-01 details: Focus on revenue tags: quarterly"
./pos "new idea: Dark mode for dashboard tags: product, ui"
./pos "new feature: Export to PDF details: Allow report export tags: enhancement"

# Update status
./pos "update: Review Q1 report status: completed"
./pos "update: Dark mode status: in-progress note: Starting design phase"

# Generate to-do list
./pos "/todo"
```

### Task management

```bash
# Create task with all options
./pos "new task: [title] due: [YYYY-MM-DD] details: [text] tags: [tag1, tag2]"

# Update task status
./pos "update: [title] status: [completed|in-progress|blocked|waiting|on-hold|archived]"
./pos "update: [title] status: [status] note: [optional note]"

# Generate daily to-do list
./pos "/todo"

# Process notepad captures
./pos "process notepad"
```

### Team feedback

```bash
# Record observation
./pos "observation: Sarah Johnson - Great presentation skills details: Clear communication"

# Create 360 review template
./pos "360: John Smith"
./pos "360 review: John Smith"
```

### Meeting workflows

```bash
# Prepare for meeting
./pos "prep meeting: Q1 Planning"

# Prepare for 1:1 (pulls context from observations, past meetings, etc.)
./pos "121: Sarah"

# Process meeting notes
./pos "post meeting: Q1 Planning"
```

### MFM reviews

```bash
# Review MFM pre-read with 5-dimensional framework
./pos "mfm review: strategic accounts Feb"
./pos "review mfm: marketing February"

# Create post-MFM summary
./pos "mfm summary: strategic accounts Feb"
./pos "post mfm: first strike Jan"
```

### Hiring workflows

```bash
# Set up role evaluation criteria from JD
./pos "setup role: Growth Eng Manager"

# Screen all CVs for a role
./pos "screen CVs: Growth Eng Manager"

# Screen single CV
./pos "review CV: Sumit Patil for Growth Eng Manager"

# Shortlist and generate interview prep
./pos "shortlist: Sumit Patil for Growth Eng Manager"

# Evaluate after interview (uses Granola transcript)
./pos "interview eval: Sumit Patil for Growth Eng Manager"
```

### Daily workflow

```bash
# Log work session (throughout day)
./pos "session: Worked on Julie agent system, added orchestration layer"

# Conduct daily summary interview (end of day)
./pos "daily summary"
```

## Project structure

```
Chief_of_staff/
├── pos                       # Main command interface
├── CLAUDE.md                 # Project instructions for Claude
├── README.md                 # This file
├── project_summary.md        # Current implementation status
├── scripts/
│   ├── parse_command.py      # Command routing and parsing
│   ├── detect_agent.py       # Agent detection logic
│   ├── create_item.py        # Create tasks/ideas/features
│   ├── todo.py               # Daily to-do list generation
│   ├── update_item.py        # Status updates
│   ├── observation.py        # Team observations
│   ├── meeting_prep.py       # Meeting preparation
│   ├── daily_summary_interview.py  # Daily reflection
│   ├── session_log.py        # Session logging
│   ├── notepad_processor.py  # Notepad processing
│   ├── strategy_query_helper.py    # Progressive strategy loading
│   ├── mfm_agent.py          # MFM review workflows
│   ├── hiring_agent.py       # CV screening and interview evaluation
│   └── utils.py              # Shared utilities
├── .claude/
│   ├── hooks/                # Deterministic enforcement hooks
│   │   └── check-em-dashes.sh
│   ├── personas/             # Agent persona definitions
│   │   ├── AGENT_TASKS.md
│   │   ├── AGENT_PEOPLE.md
│   │   ├── AGENT_STRATEGY.md
│   │   ├── AGENT_REFLECTION.md
│   │   ├── AGENT_MEETINGS.md
│   │   ├── AGENT_MFM.md
│   │   └── AGENT_HIRING.md
│   └── skills/               # Auto-discovered skills (YAML frontmatter)
│       ├── coaching-prep/    # Pre-call coaching evidence gathering
│       ├── coaching-review/  # Post-call coaching tracker updates
│       ├── call-reflection/  # Communication pattern analysis
│       ├── post-meeting/     # Meeting summary and action extraction
│       ├── session-logging/  # Work session logging
│       ├── daily-summary/    # End-of-day interview
│       ├── todo/             # Daily to-do with condensed overview
│       ├── 4ps-writing/      # Weekly 4Ps drafting
│       ├── notepad-processing/ # Notepad classification and routing
│       ├── role-expectations/  # Role expectations documents
│       ├── review-strategy/  # Strategy document review
│       ├── presentation/     # HTML presentation (v1)
│       └── presentation-v2/  # HTML presentation (v2, branding)
└── Work/                     # Obsidian vault
    ├── Inbox/
    │   ├── Tasks/            # Task files
    │   ├── Ideas/            # Idea files
    │   ├── Features/         # Feature requests
    │   ├── Actions/          # Action items
    │   └── Today/            # Daily summaries
    ├── Team/
    │   └── Observations/     # Team observations
    ├── People/               # Person-specific context
    ├── Process/
    │   └── MFM/              # MFM pre-reads and summaries
    ├── LLM_Context/
    │   ├── strategy-memory/  # L1/L2/L3 strategy hierarchy
    │   └── MFM_review_framework.md
    ├── 1-Notepad/            # Frictionless capture
    ├── 4Ps/                  # Weekly 4Ps documents
    └── Daily_Logs/           # Session logs
```

## File format

Items use Markdown with YAML frontmatter:

```markdown
---
type: task
due-date: 2026-03-01
status: active
tags: [quarterly, report]
---
# Task: Review Q1 report

## Details

Focus on revenue metrics and team performance.
```

## Status values

| Status | Description |
|--------|-------------|
| `active` | Currently actionable |
| `in-progress` | Actively working on it |
| `blocked` | Cannot proceed |
| `waiting` | Waiting on someone/something |
| `on-hold` | Paused temporarily |
| `completed` | Finished |
| `archived` | No longer relevant |

## Memory system

Julie uses claude-mem for semantic memory with project-based partitioning:
- Stores observations, decisions, and context
- Enables duplicate detection during notepad processing
- Supports cross-session knowledge retrieval

## Development

### Running tests

```bash
# Test agent detection
python3 scripts/detect_agent.py

# Test strategy helper
python3 scripts/strategy_query_helper.py

# Test MFM agent
python3 scripts/mfm_agent.py
```

### Agent personas

Each agent has a persona file in `.claude/personas/` that defines:
- Role and responsibilities
- Commands handled
- Access permissions
- Workflows and output formats
- Memory usage patterns

## Current status

**Complete:**
- 7 specialized agents (Tasks, People, Strategy, Reflection, Meetings, MFM, Hiring)
- 13 auto-discovered skills with YAML frontmatter descriptions
- Coaching plan workflow (prep + review paired skills)
- Call reflection with personal growth pattern tracking
- Em dash enforcement hook (deterministic style guard)
- CLAUDE.md trimmed to lean routing document (285 lines)

**Architecture:** Skills use Claude Code's auto-discovery via `.claude/skills/*/SKILL.md` with YAML frontmatter. Agents use persona files in `.claude/personas/`. Hooks enforce style rules deterministically.
