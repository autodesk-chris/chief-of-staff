# Chief of Staff - Personal OS

A personal operating system that streamlines daily workflows by integrating task management, idea capture, and feature planning into a unified, AI-powered experience.

## Overview

This system integrates with Obsidian and Claude Code to provide:
- Quick command-line capture of tasks, ideas, and features
- Automatic organization in your Obsidian vault
- Daily and weekly summaries of your work
- AI-powered workflow automation

## Features

### Creation Commands
- `new task` - Create a new task with due date and tags
- `new idea` - Capture ideas quickly with tags
- `new feature` - Document feature requests with details
- `observation` - Record observations about team members

### Summary Commands
- `/today` - Generate a daily summary of tasks, ideas, and features
- `/weekly` - Generate a weekly activity report

## Architecture

Built on three core components:
1. **Obsidian Vault** - Central knowledge hub for storing all notes and work items
2. **Claude Code Terminal** - Execution environment for automation commands
3. **3-Layer Context System** - Global preferences, project instructions, and reference files

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/autodesk-chris/chief-of-staff.git
   cd chief-of-staff
   ```

2. **Requirements:**
   - Python 3.6 or higher
   - Obsidian (optional, for viewing your vault)

3. **Open your Obsidian vault:**
   - Point Obsidian to the `Work/` folder in this project
   - Your tasks, ideas, and features will appear automatically

## Usage

### Quick Start

Use the `./pos` command to interact with your Personal OS:

```bash
# Create a task
./pos "new task: Buy groceries due: 2026-01-10 details: Get milk and bread tags: personal, shopping"

# Capture an idea
./pos "new idea: Improve dashboard UI details: Redesign the analytics view tags: product, ui"

# Document a feature request
./pos "new feature: Dark mode support details: Add dark theme to the app tags: ui, frontend"

# Generate today's summary
./pos "/today"

# Generate weekly summary
./pos "/weekly"
```

### Command Syntax

**Create a Task:**
```bash
./pos "new task: [Title] due: [YYYY-MM-DD] details: [Description] tags: [tag1, tag2]"
```
- `due:` - Optional due date in YYYY-MM-DD format
- `details:` - Optional description
- `tags:` - Optional comma-separated tags

**Create an Idea:**
```bash
./pos "new idea: [Title] details: [Description] tags: [tag1, tag2]"
```

**Create a Feature:**
```bash
./pos "new feature: [Title] details: [Description] tags: [tag1, tag2]"
```

**Create an Observation:**
```bash
./pos "observation: [Name] - [Observation] details: [Description] tags: [tag1, tag2]"
./pos "I have feedback: [Name] - [Feedback] tags: [tag1, tag2]"
```

**Generate Summaries:**
```bash
./pos "/today"    # Daily summary
./pos "/weekly"   # Weekly summary
```

## Project Structure

```
Chief_of_staff/
├── pos                    # Main command interface
├── CLAUDE.md             # Project context for Claude
├── scripts/
│   ├── create_item.py    # Create tasks/ideas/features
│   ├── summary.py        # Generate summaries
│   ├── parse_command.py  # Parse natural language commands
│   └── utils.py          # Helper functions
└── Work/                 # Obsidian vault
    ├── Inbox/
    │   ├── Tasks/        # All tasks
    │   ├── Ideas/        # All ideas
    │   ├── Features/     # All features
    │   └── Actions/      # Team actions
    ├── Team/             # Team feedback
    │   ├── Observations/ # Team member observations
    │   └── 360_[name]_FY26.md  # 360 reviews
    ├── LLM_Context/      # Reference files for Claude
    ├── Notes/
    └── Research/
```

## File Format

All items are stored as Markdown files with YAML frontmatter:

**Task Example:**
```markdown
---
type: task
due-date: 2026-01-15
tags: [work, urgent]
---
# Task: Complete Q1 Report

## Details

Compile sales data and create presentation slides.
```

**Idea Example:**
```markdown
---
type: idea
tags: [product, ux]
due-date: null
---
# Idea: Improve onboarding flow

## Details

Add interactive tutorial for new users.
```

**Observation Example:**
```markdown
---
type: observation
team-member: Sarah Johnson
date: 2026-01-03
tags: [leadership]
---
# Observation: Sarah Johnson - 2026-01-03

## Details

Excellent communication skills during presentation.
```

## Status

✅ MVP Complete - Ready to use!
