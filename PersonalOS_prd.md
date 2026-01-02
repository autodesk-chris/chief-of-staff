# Product Requirements Document: Personal Operating System (MVP)

**Author:** Manus AI
**Original Date:** December 31, 2025
**Updated:** January 2, 2026
**Status:** ✅ MVP Complete

## 1. Introduction

### 1.1. Vision

To create a personal operating system that streamlines daily workflows, reduces context switching, and enhances productivity by integrating key communication and task management tools into a unified, AI-powered experience.

### 1.2. Goal

This document outlines the implementation of a Minimum Viable Product (MVP) of a personal operating system using Claude Code and Obsidian. The MVP includes commands for creating tasks, ideas, features, and actions (team commitments) directly through Claude Code, as well as commands for generating daily and weekly activity summaries. The system is inspired by Teresa Torres' 3-layer context model and uses an "Inbox" folder structure to capture and organize all work items.

## 2. Core Architecture

The system will be built on a foundation of three core components:

### 2.1. The Two-Window Setup

- **Obsidian Window (Left)**: Serves as the central knowledge hub, storing all notes, context files, and generated summaries in a structured Markdown format. The primary workspace is the "Inbox" folder where all work items are captured and organized.
- **Claude Code Terminal (Right)**: The execution environment where commands are run to automate workflows. Claude operates from within the Inbox folder to create and manage tasks, ideas, and features.

### 2.2. Obsidian Vault Structure

A dedicated Obsidian vault will be used to store all system-related files. The structure follows Teresa Torres' model with a clear separation between context and work items:

```
Chief_of_staff/
├── pos                    # Command line interface
├── CLAUDE.md              # Project-specific instructions
├── scripts/               # Python automation scripts
│   ├── create_item.py     # Create tasks/ideas/features/actions
│   ├── summary.py         # Generate summaries
│   ├── parse_command.py   # Parse natural language commands
│   └── utils.py           # Helper functions
└── Work/                  # Obsidian vault
    ├── LLM_Context/       # Reference files for Claude
    │   ├── business_profile.md
    │   └── team_members.md
    ├── Inbox/
    │   ├── Tasks/         # User's own tasks
    │   ├── Ideas/         # Ideas and brainstorming
    │   ├── Features/      # Feature requests
    │   └── Actions/       # Team member commitments
    ├── Notes/
    └── Research/
```

**Key Folders**:
- `LLM_Context/`: Reference files for Claude (business context, team members, etc.)
- `Inbox/`: The primary workspace containing all tasks, ideas, features, and actions
- `scripts/`: Python automation scripts that power the commands
- `pos`: Simple command-line interface for executing commands

### 2.3. The 3-Layer Context System

**Layer 1: Global Preferences (`/Users/smallc/AI/CLAUDE.md`)**
- **Purpose**: Universal working preferences for Claude across all AI projects
- **Location**: In the parent AI folder for use across multiple projects
- **Examples**: "Write in layman's terms," "Remind to commit changes to git"

**Layer 2: Project-Specific Instructions (`Chief_of_staff/CLAUDE.md`)**
- **Purpose**: Instructions specific to the Personal OS project
- **Content**: Command syntax, file naming conventions, development guidelines
- **Location**: Project root where Claude operates

**Layer 3: Reference Context Files (`Work/LLM_Context/`)**
- **Purpose**: Work-specific reference context that Claude can load on demand
- **Examples**: `business_profile.md`, `team_members.md`

## 3. Key Features (MVP)

The MVP includes six core commands: four for creating items and two for generating summaries. All items are stored in the Obsidian vault with consistent markdown formatting.

### 3.0. Command Interface

**Method 1: Natural Language with Claude**
- Simply tell Claude what you want in natural language
- Example: "Create a task to review the budget by Friday"
- Claude will create the item and prompt for optional fields

**Method 2: Direct Command Syntax**
- Use the exact command syntax from terminal or through Claude
- Example: `./pos "new task: Review budget due: 2026-01-10"`
- All fields specified upfront

**Workflow:**
1. Item is created immediately
2. User is prompted for due date (if not provided)
3. User is prompted for details (if not provided)
4. User can skip any prompt by saying "skip" or providing the information

### 3.1. `new task` Command

- **Functionality**: Creates a new task file in the `Inbox/Tasks/` folder with a `task_` prefix.
- **Syntax**: `new task: [Task Title] due: [Due Date] details: [Task Details] tags: [comma-separated tags]`
- **Example**: `new task: Prepare Q1 report due: 2026-01-15 details: Compile sales data and create presentation slides. tags: work, reporting`
- **Output**: A new Markdown file (e.g., `Inbox/Tasks/task_Prepare_Q1_report.md`) with the following content:

```markdown
---
type: task
due-date: 2026-01-15
tags: [work, reporting]
---

# Task: Prepare Q1 report

## Details

Compile sales data and create presentation slides.
```

### 3.2. `new idea` Command

- **Functionality**: Creates a new idea file in the `Inbox/Ideas/` folder with an `idea_` prefix.
- **Syntax**: `new idea: [Idea Title] details: [Idea Details] tags: [comma-separated tags]`
- **Example**: `new idea: Gamify the onboarding process details: Add a points system and badges to encourage new users to complete the setup steps. tags: product, engagement`
- **Output**: A new Markdown file (e.g., `Inbox/Ideas/idea_Gamify_the_onboarding_process.md`) with the following content:

```markdown
---
type: idea
tags: [product, engagement]
due-date: null
---

# Idea: Gamify the onboarding process

## Details

Add a points system and badges to encourage new users to complete the setup steps.
```

### 3.3. `new feature` Command

- **Functionality**: Creates a new feature file in the `Inbox/Features/` folder with a `feature_` prefix.
- **Syntax**: `new feature: [Feature Title] details: [Feature Details] tags: [comma-separated tags]`
- **Example**: `new feature: Dark mode support details: Implement a dark mode theme for the user interface. tags: ui, frontend`
- **Output**: A new Markdown file (e.g., `Inbox/Features/feature_Dark_mode_support.md`) with the following content:

```markdown
---
type: feature
tags: [ui, frontend]
due-date: null
---

# Feature: Dark mode support

## Details

Implement a dark mode theme for the user interface.
```

### 3.4. `new action` Command

- **Functionality**: Creates a new action file in the `Inbox/Actions/` folder with an `action_` prefix. Actions track commitments from team members.
- **Syntax**: `new action: [Person] to [Action] due: [Due Date] details: [Action Details] tags: [comma-separated tags]`
- **Example**: `new action: Sarah to review budget proposal due: 2026-01-08 details: Needs approval before board meeting tags: finance, urgent`
- **Output**: A new Markdown file (e.g., `Inbox/Actions/action_Sarah_to_review_budget_proposal.md`) with the following content:

```markdown
---
type: action
due-date: 2026-01-08
tags: [finance, urgent]
---

# Action: Sarah to review budget proposal

## Details

Needs approval before board meeting
```

### 3.5. `/today` Command

- **Functionality**: Generates a daily summary of work items due today and upcoming tasks for the next week.
- **Syntax**: `/today`
- **Output**: A new Markdown file (e.g., `Inbox/today_2026-01-15.md`) with the following sections:

**Tasks Due Today**: Lists all tasks with a due date matching today.

**Tasks Due This Week**: Lists all tasks with a due date within the next 7 days (excluding today).

**Recent Ideas**: Lists all ideas created today.

**Recent Features**: Lists all features created today.

### 3.6. `/weekly` Command

- **Functionality**: Generates a summary of all activity from the past 7 days, including tasks created, ideas captured, and features proposed.
- **Syntax**: `/weekly`
- **Output**: A new Markdown file (e.g., `Inbox/weekly_summary_2026-01-15.md`) with the following sections:

**Tasks This Week**: Lists all tasks created or modified in the last 7 days, organized by due date.

**Ideas This Week**: Lists all ideas captured in the last 7 days.

**Features This Week**: Lists all features proposed in the last 7 days.

**Activity Summary**: Provides counts of total tasks, ideas, and features created during the week.

## 4. Implementation Summary

### ✅ Stage 1: Setup and Configuration (Completed)
- Created GitHub repository at https://github.com/autodesk-chris/chief-of-staff
- Created Obsidian vault folder structure with Tasks, Ideas, Features, and Actions folders
- Set up global CLAUDE.md in `/Users/smallc/AI/` for all AI projects
- Created project-specific CLAUDE.md with command instructions
- Configured .gitignore for Python and Obsidian files

### ✅ Stage 2: Folder Structure (Completed)
- Created `Work/Inbox/` with Tasks, Ideas, Features, Actions subfolders
- Set up `Work/LLM_Context/` for reference files (business_profile.md, team_members.md)
- Created Notes and Research folders for additional organization

### ✅ Stage 3: Creation Commands (Completed)
- Built `scripts/create_item.py` - Main creation script supporting all item types
- Built `scripts/utils.py` - Helper functions for file naming, tag parsing, date validation
- Implemented file naming sanitization (special characters, spaces to underscores)
- Implemented YAML frontmatter generation with type, due-date, and tags
- Added support for optional fields (due dates, details, tags)
- Tested with normal inputs, special characters, and edge cases

### ✅ Stage 4: Summary Commands (Completed)
- Built `scripts/summary.py` - Summary generation for daily and weekly reports
- Implemented `/today` command with tasks due today/this week, recent ideas/features
- Implemented `/weekly` command with 7-day activity and counts
- Added frontmatter parsing to extract metadata from markdown files
- Tested summary generation with various date ranges

### ✅ Stage 5: Integration (Completed)
- Built `scripts/parse_command.py` - Natural language command parser
- Created `pos` CLI interface for simple command execution
- Integrated all scripts with Claude Code
- Tested end-to-end workflow with Claude
- Added Actions feature for tracking team commitments
- Documented complete system in README.md

## 5. Non-Functional Requirements

- **Usability**: The commands should be simple, intuitive, and easy to remember.
- **Reliability**: The file creation and summary processes should be robust and handle different input lengths and special characters.
- **Performance**: Commands should execute quickly, even with large numbers of tasks, ideas, and features.
- **Consistency**: All generated files should follow a consistent Markdown format and structure.

## 6. Future Enhancements

### Potential Integrations
- **Slack Integration**: Enhance summaries with Slack conversation digests and automatically extracted action items
- **Email Integration**: Add email digest and action item extraction from important messages
- **Calendar Integration**: Sync tasks with calendar applications (Google Calendar, Outlook)

### Additional Features
- **Search Functionality**: Add ability to search across all items by keyword, tag, or date range
- **Templates**: Create item templates for recurring tasks or standard action types
- **Bulk Operations**: Archive completed items, bulk tag updates, or status changes
- **Analytics**: Visualize productivity trends, completion rates, and time-to-completion metrics
- **Reminders**: Add automated reminders for tasks approaching due dates
- **Sub-items**: Support for breaking down tasks into sub-tasks or checklists
