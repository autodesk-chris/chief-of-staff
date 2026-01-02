# Product Requirements Document: Personal Operating System (MVP)

**Author:** Manus AI
**Date:** December 31, 2025

## 1. Introduction

### 1.1. Vision

To create a personal operating system that streamlines daily workflows, reduces context switching, and enhances productivity by integrating key communication and task management tools into a unified, AI-powered experience.

### 1.2. Goal

This document outlines the requirements for building a Minimum Viable Product (MVP) of a personal operating system using Claude Code and Obsidian. The MVP will focus on a core set of commands for creating tasks, ideas, and features directly from the Claude Code terminal, as well as commands for reviewing daily and weekly activity. The system is inspired by Teresa Torres' 3-layer context model and uses an "Inbox" folder structure to capture and organize all work items.

## 2. Core Architecture

The system will be built on a foundation of three core components:

### 2.1. The Two-Window Setup

- **Obsidian Window (Left)**: Serves as the central knowledge hub, storing all notes, context files, and generated summaries in a structured Markdown format. The primary workspace is the "Inbox" folder where all work items are captured and organized.
- **Claude Code Terminal (Right)**: The execution environment where commands are run to automate workflows. Claude operates from within the Inbox folder to create and manage tasks, ideas, and features.

### 2.2. Obsidian Vault Structure

A dedicated Obsidian vault will be used to store all system-related files. The structure follows Teresa Torres' model with a clear separation between context and work items:

```
Obsidian Vault/
├── LLM_Context/
│   ├── global_CLAUDE.md
│   ├── business_profile.md
│   ├── team_members.md
│   └── [other reference files]
├── Inbox/
│   ├── CLAUDE.md (project-specific instructions)
│   ├── Tasks/
│   ├── Ideas/
│   └── Features/
├── Notes/
├── Research/
└── [other folders as needed]
```

**Key Folders**:
- `LLM_Context/`: The heart of the system, containing all context files for Claude (global preferences and reference materials).
- `Inbox/`: The primary workspace containing all tasks, ideas, and features. This is where Claude operates from the terminal. The folder includes a `CLAUDE.md` file with project-specific instructions for the new commands.

### 2.3. The 3-Layer Context System

**Layer 1: Global Preferences (`~/.claude/CLAUDE.md`)**
- **Purpose**: Universal working preferences for Claude.
- **Examples**: "Always create a plan before acting," "Use bullet points for summaries."

**Layer 2: Project-Specific Instructions (`Inbox/CLAUDE.md`)**
- **Purpose**: Rules and workflows for the Inbox project (e.g., command syntax, file naming conventions).
- **Examples**: File naming conventions, integration details.

**Layer 3: Reference Context Files (`LLM_Context/`)**
- **Purpose**: Detailed, reusable context that Claude loads on demand.
- **Examples**: `business_profile.md`, `team_members.md`, `product_specs.md`.

## 3. Key Features (MVP)

The MVP will focus on five core commands: three for creating new items and two for summarizing and reviewing work. All commands operate on tasks, ideas, and features created through the new commands.

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

### 3.4. `/today` Command

- **Functionality**: Generates a daily summary of work items due today and upcoming tasks for the next week.
- **Syntax**: `/today`
- **Output**: A new Markdown file (e.g., `Inbox/today_2026-01-15.md`) with the following sections:

**Tasks Due Today**: Lists all tasks with a due date matching today.

**Tasks Due This Week**: Lists all tasks with a due date within the next 7 days (excluding today).

**Recent Ideas**: Lists all ideas created today.

**Recent Features**: Lists all features created today.

### 3.5. `/weekly` Command

- **Functionality**: Generates a summary of all activity from the past 7 days, including tasks created, ideas captured, and features proposed.
- **Syntax**: `/weekly`
- **Output**: A new Markdown file (e.g., `Inbox/weekly_summary_2026-01-15.md`) with the following sections:

**Tasks This Week**: Lists all tasks created or modified in the last 7 days, organized by due date.

**Ideas This Week**: Lists all ideas captured in the last 7 days.

**Features This Week**: Lists all features proposed in the last 7 days.

**Activity Summary**: Provides counts of total tasks, ideas, and features created during the week.

## 4. Implementation Roadmap

### Phase 1: Setup and Configuration
1.  Create the Obsidian vault and folder structure (`LLM_Context/`, `Inbox/Tasks/`, `Inbox/Ideas/`, `Inbox/Features/`).
2.  Create the `LLM_Context/global_CLAUDE.md` global context file with universal working preferences.
3.  Create the `Inbox/CLAUDE.md` project context file with instructions for the new commands.

### Phase 2: Command Implementation - Creation Commands
1.  Develop a Python script to parse the `new task`, `new idea`, and `new feature` commands.
2.  Implement the logic to create new Markdown files in the appropriate folders with the correct content and formatting.
3.  Ensure the script handles file naming (replacing spaces with underscores, sanitizing special characters).
4.  Implement frontmatter generation with `type`, `due-date`, and `tags` fields.
5.  For ideas and features, set `due-date` to `null` since they don't have due dates.
6.  For tasks, parse and include the due date from the command.
7.  Parse and include tags from the command (comma-separated input converted to YAML list format).

### Phase 3: Command Implementation - Summary Commands
1.  Develop a Python script to parse the `/today` command.
2.  Implement the logic to scan the `Inbox/Tasks/` folder and filter tasks by due date.
3.  Implement the logic to scan the `Inbox/Ideas/` and `Inbox/Features/` folders for items created today.
4.  Generate a formatted Markdown summary file.

### Phase 4: Weekly Command Implementation
1.  Develop a Python script to parse the `/weekly` command.
2.  Implement the logic to scan all folders and identify items created in the last 7 days.
3.  Organize results by item type and due date.
4.  Generate a formatted Markdown summary file with activity counts.

### Phase 5: Integration and Testing
1.  Integrate all Python scripts with Claude Code to make the commands executable from the terminal.
2.  Thoroughly test each command to ensure they create files correctly and generate accurate summaries.
3.  Test edge cases (e.g., no tasks due today, special characters in titles).

## 5. Non-Functional Requirements

- **Usability**: The commands should be simple, intuitive, and easy to remember.
- **Reliability**: The file creation and summary processes should be robust and handle different input lengths and special characters.
- **Performance**: Commands should execute quickly, even with large numbers of tasks, ideas, and features.
- **Consistency**: All generated files should follow a consistent Markdown format and structure.

## 6. Future Enhancements

- **Slack Integration**: Enhance the `/today` and `/weekly` commands to include:
  - **Slack Digest**: A summary of key conversations and action items from specified Slack channels.
  - **Slack Action Items**: Automatically extract action items from Slack messages.

- **Outlook Integration**: Enhance the `/today` and `/weekly` commands to include:
  - **Outlook Email Digest**: A summary of important emails and action items.
  - **Outlook Calendar Summary**: A list of today's meetings and any preparation materials.
