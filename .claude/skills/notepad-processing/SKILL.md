---
name: notepad-processing
description: >
  Process the central notepad into structured items and domain-specific notepads.
  Classifies content as actionable (tasks, actions, reminders, features, decisions)
  or strategic (routes to domain notepads). Use when "process notepad", "process
  my notes", or similar. Confirms before creating items.
---

# Notepad processing

Frictionless capture to structured processing to organized storage.

## Trigger

When user says "process notepad", "process my notes", or runs `./pos "process notepad"`.

## Three-stage workflow

### 1. Capture (ongoing)

- Write anything to `Work/1-Notepad/Notepad.md`
- No structure needed, no categorization needed
- Just brain dump - mix of actionable and strategic thinking
- Central notepad is for fast, frictionless capture

### 2. Process (this skill)

- Run: `./pos "process notepad"`
- Script splits notepad into sections
- Classifies each section as actionable or strategic
- Checks memory for duplicate tasks
- **Shows classification results and asks for confirmation**
- Creates tasks/actions/reminders/features/decisions from actionables
- Routes strategic thinking to domain-specific notepads
- Archives processed content with timestamp
- Clears central notepad

### 3. Digest (future phases)

- Review domain notepads when working in that area
- Strategy work: `Work/Notes/Strategy/notepad.md`
- People work: `Work/People/notepad.md`
- Meeting prep: `Work/Meetings/Prep/notepad.md`
- Ideas: `Work/Inbox/Ideas/notepad.md`
- Domain agents will have "digest" commands to process their notepads

## Classification logic

### Actionable (creates items)

- **Tasks:** Clear action with deliverable ("Review...", "Prepare...", "Schedule...")
- **Actions:** Work assigned to someone ("[Person] needs to...")
- **Reminders:** Things not to forget ("Remember to...", "Don't forget...")
- **Features:** Julie improvements ("I want Julie to...")
- **Decisions:** Decisions made ("Decided to...", "Decision:")

### Strategic (routes to domain notepads)

- **Strategy:** OKRs, product strategy, high-level planning
- **People:** Team observations, 121 topics, feedback thoughts
- **Meetings:** Meeting prep ideas, discussion topics
- **Ideas:** Incomplete exploratory thoughts

## Key principles

- Conservative extraction (better to route to strategic than create wrong item)
- User confirmation before creating items
- Memory integration for duplicate detection
- Preserve original notepad in Archive/ with timestamp
- Central notepad cleared and ready for new capture

## File locations

- Central notepad: `Work/1-Notepad/Notepad.md`
- Archive: `Work/1-Notepad/Archive/notepad_YYYY-MM-DD_HHMM.md`
- Domain notepads: `Work/Notes/Strategy/`, `Work/People/`, `Work/Meetings/Prep/`, `Work/Inbox/Ideas/`
