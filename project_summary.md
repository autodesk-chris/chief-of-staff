# Project Summary - Chief of Staff Personal OS (Julie System)

**Last Updated:** 2026-06-11 (Session 29)
**Current Phase:** Phase 3.13 - 121-prep Slack thread depth (Sessions 28-29 are non-phase: Kjetil FSM drafting, planner-sync daily cadence, dishes framework, slack digest Group DM support)
**Overall Status:** Full hierarchical agent system with Slack, Confluence, M365 email triage, voice-aware Slack thread review, daily focus menu for /todo with 3-item cap and challenge logic, a local React + Tailwind dashboard served by a launchd-managed hub on localhost:8765 with click-to-tick that mutates source files, and bidirectional Microsoft Planner integration (planner-sync pulls open Planner tasks; status changes on planner-linked local tasks emit a [PLANNER_LINKED] signal so Claude pushes completion/blocked/waiting back to Planner via the m365 MCP)

---

## 1. Project Overview

**Project:** Julie - Hierarchical Agent System for Chief of Staff Personal OS
**Original Goal:** Build an intelligent personal operating system that integrates Claude Code with Obsidian for task, people, and strategy management through command-line automation.

**Current Implementation Status:**
- ✅ **Milestone 1:** Foundation + Tasks Agent + Memory + Notepad (Complete)
- ✅ **Milestone 2:** Reflection Agent + Meetings Agent (Complete)
- ✅ **Milestone 3:** Specialized Domain Agents (Complete)
- ✅ **Milestone 4:** Multi-domain Orchestration (Complete)
- ✅ **Phase 2.5:** Slack MCP Integration (Complete)
- ✅ **Phase 2.6:** Performance Conversation Prep + Git Hygiene (Complete)
- ✅ **Phase 2.7:** Bug Fix + Development Review (Complete)
- ✅ **Phase 2.8:** Strategy Agent Routing Fix (Complete)
- ✅ **Phase 2.9:** List Commands + Meeting Auto-Extraction (Complete)
- ✅ **Phase 3.0:** Slack Report + Task Auto-Creation (Complete)
- ✅ **Phase 3.1:** Full Slack Integration Suite (Complete)
- ✅ **Phase 3.2:** Slack Commitment Scanning + Confluence Integration (Complete)
- ✅ **Phase 3.3:** Email Triage Skill with M365 Integration (Complete)
- ✅ **Phase 3.4:** Thread Review Skill with Slack Draft Push (Complete)
- ✅ **Phase 3.5:** Todo Today's Options + VIP Source Unification (Complete)
- ✅ **Phase 3.6:** Todo Completion-Sync + Similar-Items Warning (Complete)
- ✅ **Phase 3.7:** Standing Meetings Mapping + Primary-Lens Meeting Prep (Complete)
- ✅ **Phase 3.8:** /todo Meeting Lookback Generalisation (Complete)
- ✅ **Phase 3.9:** /todo Focus Discipline + Workday Time Math (Complete)
- ✅ **Phase 3.10:** HTML Dashboard with Local Hub (Complete)
- ✅ **Phase 3.11:** Planner Write-Back Integration (Complete)
- ✅ **Phase 3.12:** Dashboard Meetings Sub-Block (Complete)
- ✅ **Phase 3.13:** 121-prep Slack thread depth (Complete) ← **This Session**

**Overall Status:** Full Julie agent system operational with 7 specialized agents. Comprehensive Slack integration (report, commitment scanning, 4Ps roundup, leadership update) and Confluence MCP integration for live strategy/OKR/operating model access.

---

## 2. Key Decisions Made

### Phase 2.6 Implementation Decisions (Session 11)

**1. Performance Conversation Prep as Separate Command**
- **Decision:** Create standalone trigger, not embedded in 360 workflow
- **Reasoning:** Calibration happens between 360 completion and conversation prep
- **Benefit:** Flexibility to generate conversation prep after descriptor is finalized

**2. Trigger Command: `performance conversation prep: [Name]`**
- **Decision:** Descriptive trigger over shorter alias
- **Reasoning:** Clarity and consistency with other People Agent commands
- **Alternative rejected:** Making it automatic after 360 generation

**3. Add to People Agent (not Standalone Skill)**
- **Decision:** Extend People Agent rather than create new skill
- **Reasoning:** Tight coupling with 360 review data; same context needed
- **Benefit:** Single agent handles all people/feedback workflows

**4. Slack MCP Security**
- **Decision:** Remove browser tokens, keep only bot token
- **Reasoning:** Browser tokens (xoxc/xoxd) grant full user access if exposed
- **Trade-off:** Cannot access user-to-user DM history with bot token only

**5. Git Separation: System vs Output Files**
- **Decision:** Track only Julie system files; ignore all generated output
- **Reasoning:** Output files contain personal/work data; system files are reusable
- **Implementation:** Updated .gitignore + removed 34 legacy tracked files

---

## 3. Technical Implementation

### Architecture: All Seven Agents

| Agent | Lines | Role | Commands |
|-------|-------|------|----------|
| AGENT_TASKS.md | 263 | Task/idea/feature management | new task:, update:, /todo, process notepad |
| AGENT_REFLECTION.md | 580 | Daily summaries, Slack reports, commitment scanning, 4Ps roundup, leadership updates | daily summary, session:, slack report, scan slack, 4ps roundup, leadership update |
| AGENT_MEETINGS.md | 281 | Meeting prep/processing | prep meeting:, 121:, post meeting: |
| AGENT_PEOPLE.md | 210 | Team feedback/observations | observation:, 360:, performance conversation prep: |
| AGENT_STRATEGY.md | 320 | Strategic analysis + Confluence | OKR queries, strategy questions (via strategy_agent.py + Confluence MCP) |
| AGENT_MFM.md | 310 | MFM review/summary + Confluence | mfm review:, mfm summary: (+ Confluence for strategies/bets) |
| AGENT_HIRING.md | 374 | Candidate evaluation | setup role:, screen CVs:, shortlist:, interview eval: |

### New Workflow (Phase 2.6)

**Performance Conversation Prep (~300 lines):**
- 7-step process transforming 360 reviews into conversation guides
- Timed meeting flow format (~60 minutes)
- Sections: Opening, Descriptor, Strengths, Development Areas, Path Forward, Actions, Closing
- Backup responses for difficult questions
- Works with all descriptors: High Impact, Fully Successful, Developing

### Git Tracking Architecture

**Tracked (Julie system files):**
```
.claude/personas/AGENT_*.md      # Agent personas
scripts/*.py                      # Python automation
Work/People/360_reviews/Context/  # Workflow files only
CLAUDE.md, README.md, pos         # Project docs
```

**Ignored (Generated output):**
```
Work/Inbox/                       # Tasks, ideas, features, actions
Work/People/360_reviews/*/        # Person folders (360s, conversations)
Work/Notes/, Work/4Ps/            # Personal documents
Work/Meetings/, Work/Daily_Logs/  # Meeting prep, session logs
Work/1-Notepad/                   # Notepad content
```

---

## 4. Code Changes Summary

### New Files Created (Session 13)

**scripts/strategy_agent.py**
- **Purpose:** Handle strategy queries with progressive disclosure pattern
- **Key functions:**
  - `classify_query()` - Classifies queries as broad/domain/detail
  - `handle_strategy_query()` - Returns file paths and guidance
  - `format_strategy_response()` - Formats output for CLI
- **Features:** Maps keywords to L2 domains, L3 detail types

### Modified Files (Session 13)

**scripts/parse_command.py**
- **Change:** Added strategy query handler
- **Import:** Added `from strategy_agent import format_strategy_response, handle_strategy_query`
- **Handler:** Routes strategy queries (OKR, strategy, bet keywords) to strategy_agent

### New Files Created (Session 11)

**Work/People/360_reviews/Context/performance_conversation_workflow.md**
- **Purpose:** Defines process for generating performance conversation prep documents
- **Key contents:** 7-step workflow, output format, quality criteria, conversation starters

### Modified Files

**.claude/personas/AGENT_PEOPLE.md**
- **Change:** Added performance conversation prep command and workflow reference
- **New section:** Performance Conversation Prep Workflow with trigger, prerequisites, process

**CLAUDE.md**
- **Change:** Updated command reference table
- **Addition:** `performance conversation prep:` added to People Agent commands

**.gitignore**
- **Change:** Comprehensive patterns for output file exclusion
- **Categories:** 360 reviews, observations, inbox items, notes, meetings, notepads

**Slack_mcp/slack-mcp-server/.env**
- **Change:** Removed xoxc/xoxd browser tokens for security
- **Kept:** xoxb bot token only

### Generated Output (Not Tracked)

- `Performance_conversation_Simen_Hellem-FY26.md` (High Impact)
- `Performance_conversation_Even_Olsted-FY26.md` (Fully Successful)
- `Performance_conversation_Katarina_Plevec-FY26.md` (Developing)

---

## 5. Commands & Setup

### New Command (Phase 2.6)

**Performance Conversation Prep:**
```bash
./pos "performance conversation prep: [Name]"
./pos "perf conversation prep: [Name]"
```

**Prerequisites:**
1. Completed 360 review file (`360_[Name]_FY26.md`)
2. Final performance descriptor confirmed (post-calibration)

### All Agent Commands

```bash
# Tasks Agent
./pos "new task: [title] due: [date] details: [text] tags: [tags]"
./pos "new idea: [title] details: [text]"
./pos "new reminder: [title] due: [date]"
./pos "new decision: [title] participants: [names] rationale: [why]"
./pos "update: [title] status: [status]"
./pos "change due date: [title] to: [YYYY-MM-DD]"
./pos "/todo"                             # Auto-extracts from meetings first
./pos "process notepad"
./pos "archive completed"
./pos "actions"                           # List all actions
./pos "decisions"                         # List all decisions
./pos "new_daily: [note]"                 # Add contribution note

# Reflection Agent
./pos "daily summary"
./pos "finalize summary: [additions]"
./pos "session: [summary]"
./pos "slack report"                     # Comprehensive Slack report with auto task creation
./pos "scan slack"                       # Scan for commitments, extract tasks/actions
./pos "4ps roundup"                      # Review team 4Ps from Slack vs MFM priorities
./pos "leadership update"                # Synthesize leadership channels into shareable update
./pos "4ps"                              # Generate weekly 4Ps draft
./pos "finalize 4ps: [content]"          # Save 4Ps to file

# Meetings Agent
./pos "prep meeting: [title]"
./pos "121: [name]"
./pos "post meeting: [title]"             # Auto-extracts actions/decisions/tasks from Granola
./pos "finalize meeting: [title]"         # Create summary after extraction

# People Agent
./pos "observation: [Name] - [observation]"
./pos "360: [Name]"
./pos "performance conversation prep: [Name]"

# Strategy Agent (fixed in Session 13)
./pos "what are the current OKRs?"
./pos "what's the monetization strategy?"
./pos "what bets are we making?"

# MFM Agent
./pos "mfm review: [squad] [month]"
./pos "mfm summary: [squad] [month]"

# Hiring Agent
./pos "setup role: [role name]"
./pos "screen CVs: [role name]"
./pos "shortlist: [name] for [role]"
./pos "interview prep: [name] for [role]"
./pos "interview eval: [name] for [role]"
```

### Git Commands Used

```bash
# Remove legacy files from tracking (keep locally)
git rm --cached -r Work/1-Notepad/ Work/4Ps/ Work/Inbox/ ...

# Verify tracked files
git ls-tree -r HEAD --name-only
```

---

## 6. Problems Solved

### Problem 1: Slack DMs Not Accessible
**Issue:** Attempted to access DMs with team members for feedback examples
**Investigation:** Discovered channels cache only had 2 DMs
**Root cause:** Bot tokens (xoxb) cannot access user-to-user DM history
**Resolution:** Documented limitation; would need user token (xoxp) for DM access

### Problem 2: Browser Tokens Exposed
**Issue:** .env file contained live browser tokens (xoxc/xoxd)
**Risk:** Full Slack access as user if file exposed
**Solution:** Removed browser tokens, verified .env in .gitignore

### Problem 3: Output Files Tracked in Git
**Issue:** 34 generated output files committed to git
**Cause:** .gitignore only prevents new files; doesn't remove already-tracked
**Solution:** `git rm --cached` to remove from tracking while keeping locally

---

## 7. Pending Items

### Known Limitations

**1. Slack MCP - DM Access**
- Bot tokens cannot access user-to-user DMs
- Would need user token (xoxp) or browser tokens for DM history

**2. Performance Conversation Prep**
- Requires completed 360 review first
- User must provide final performance descriptor

### Potential Improvements

**Short-term:**
- Add 360 Context reference files to git (assessment guide, One Orbit behaviours)
- Consider `.claude/skills/` folder if skills are created

**Medium-term:**
- Explore user token (xoxp) for Slack DM access
- Add digest commands to domain agents for processing notepads

---

## 8. User Preferences & Context

### Workflow Preferences

- **Git separation:** Only Julie system files tracked; all generated output local
- **Security conscious:** Removed browser tokens despite convenience trade-off
- **Performance descriptors:** High Impact, Fully Successful, Developing
- **Conversation prep style:** Timed meeting flow with talking points and backup questions

### Slack Configuration

**Config file:** `.slack_digest_config.json`
**Token type:** Bot token only (xoxb)
**Limitation:** Cannot access user-to-user DMs

---

## 9. Next Steps

### Immediate Actions
1. ✅ Performance conversation prep workflow created
2. ✅ Conversation preps generated for Simen, Even, Katarina
3. ✅ Slack MCP secured (browser tokens removed)
4. ✅ Git tracking cleaned up (34 files removed)
5. ✅ Pushed to GitHub

### Short-term
- Use generated conversation prep documents for performance reviews
- Consider adding 360 Context reference files to git

### Medium-term
- Add domain notepad digest commands
- Explore user token for Slack DM access if needed

---

## 10. Quick Reference

### Key File Locations

**Phase 2.9 Files:**
- `scripts/list_items.py` - List actions/decisions, change due date, daily notes
- `scripts/meeting_extractor.py` - Meeting auto-extraction workflow

**Phase 2.8 Files:**
- `scripts/strategy_agent.py` - Strategy query handler with progressive disclosure

**Phase 2.6 Files:**
- `Work/People/360_reviews/Context/performance_conversation_workflow.md` - Performance conversation workflow

**Agent Personas:**
- `.claude/personas/AGENT_TASKS.md` - Tasks Agent
- `.claude/personas/AGENT_REFLECTION.md` - Reflection Agent
- `.claude/personas/AGENT_MEETINGS.md` - Meetings Agent
- `.claude/personas/AGENT_PEOPLE.md` - People Agent (updated)
- `.claude/personas/AGENT_STRATEGY.md` - Strategy Agent
- `.claude/personas/AGENT_MFM.md` - MFM Agent

### What's Tracked in Git

```
.claude/personas/           # Agent personas
scripts/                    # Python automation
Work/People/360_reviews/Context/  # Workflow files only
CLAUDE.md, README.md, pos   # Project docs
Slack_mcp/                  # Slack MCP docs
```

### What's NOT Tracked

```
Work/Inbox/                 # All inbox items
Work/People/360_reviews/*/  # Person folders
Work/Notes/, Work/4Ps/      # Personal documents
Work/Meetings/              # Meeting prep
Work/Daily_Logs/            # Session logs
Work/1-Notepad/             # Notepad content
```

### Git Commit History

**Session 15 Commits:**
```
a7a7bd5 - Add Confluence MCP integration for Strategy and MFM agents (2026-03-19)
d2d24ca - Add Slack commitment scanning for task and action extraction (2026-03-19)
a7124f4 - Add 4Ps roundup, leadership update, and Slack integration for daily summary and today report (2026-03-18)
62c94a9 - Add Slack report with automatic task creation (2026-03-18)
```

**Session 14 Commits:**
```
36c3fe3 - Add meeting auto-extraction and list commands (2026-03-18)
```

**Session 13 Commits:**
```
243b305 - Add 4Ps generation workflow (2026-03-17)
29ec17b - Fix action syntax and daily summary for Claude Code workflow (2026-03-17)
b2b2452 - Fix quick wins: agent patterns and optional feature tags (2026-03-17)
68b7556 - Add Strategy Agent routing for strategy queries (2026-03-17)
```

**Session 12 Commits:**
```
1b82393 - Add Hiring Agent and skills system (2026-03-17)
d0f2563 - Fix folder path mismatch: Work/Team → Work/People (2026-03-17)
```

**Session 11 Commits:**
```
f5a3714 - Remove output files from git tracking (2026-02-25)
a840ba5 - Add performance conversation prep workflow and update gitignore (2026-02-25)
```

**Previous Commits:**
```
e89e46f - Add Milestone 3: Specialized Domain Agents
32bda0f - Add Milestone 2: Reflection Agent and Meetings Agent
0ff5c1a - Add Phase 2.4 notepad processing with preview/confirm workflow
```

---

## Session History

### Session 1-6: Milestone 1 Complete
- Foundation, Tasks Agent, Memory, Notepad Processing

### Session 7: Milestone 2 Complete
- Reflection Agent, Meetings Agent

### Session 8: Milestone 3 Complete
- People, Strategy, MFM Agents

### Session 9: Milestone 4 Complete
- Cross-domain Orchestration

### Session 10: Phase 2.5 Complete
- Slack MCP Integration

### Session 11: Phase 2.6 Complete (2026-02-25)
- Created performance conversation prep workflow (~300 lines)
- Generated conversation preps for 3 team members
- Investigated Slack MCP security and DM access limitations
- Removed browser tokens from Slack configuration
- Cleaned up git tracking (removed 34 output files)
- Updated .gitignore with comprehensive output patterns

### Session 12: Phase 2.7 Complete (2026-03-17)
- Reviewed full Julie 2.0 development status against original brief
- Identified folder path mismatch: scripts referenced `Work/Team/` but actual folder is `Work/People/`
- Fixed path references across 5 files (utils.py, CLAUDE.md, agent personas)
- Renamed `get_team_path()` to `get_people_path()` in utils.py
- Verified observation command now works correctly
- Confirmed 7 agents operational (Hiring Agent added since last session)

### Session 13: Phase 2.8 Complete (2026-03-17)
- Comprehensive testing of all 7 agents via `./pos` commands
- Compiled detailed implementation status report
- Fixed Strategy Agent routing (was detected but had no handler)
- Created `scripts/strategy_agent.py` with progressive disclosure pattern
- Updated `scripts/parse_command.py` to route strategy queries
- Strategy queries now classify as broad/domain/detail and return appropriate file paths
- **Quick wins fixes:**
  - Added `performance conversation prep:` to people_patterns in detect_agent.py
  - Added `session:` to reflection_patterns in detect_agent.py
  - Made tags optional for `new feature:` command (was required)
- **Claude Code workflow fixes:**
  - Action command now parses "Person to Action" syntax (e.g., "Sarah to review budget" extracts assignee automatically)
  - Daily summary now non-interactive - returns draft for Claude to continue conversation
  - Added `finalize summary:` command to complete daily summary workflow
- **4Ps generation workflow:**
  - Created `scripts/fourps_generator.py` for weekly 4Ps drafts
  - Gathers context: previous 4Ps, daily summaries, tasks, meetings
  - Provides Granola MCP instructions for meeting data
  - Generates draft with Priorities, Progress, Plans, Problems
  - Commands: `4ps`, `/4ps`, `finalize 4ps`
- **Total project time:** ~25 hours

### Session 14: Phase 2.9 Complete (2026-03-18)
- **List commands implemented:**
  - `actions` - List all actions with assignee and due date
  - `decisions` - List all decisions with participants
  - `change due date:` - Modify due date on existing items
  - `new_daily:` - Add contribution notes for daily summary
- **Meeting auto-extraction:**
  - `post meeting:` now triggers automatic extraction from Granola
  - Claude queries Granola, analyzes summary, extracts actions/decisions/tasks
  - Creates items automatically using existing `./pos` commands
  - `finalize meeting:` creates summary after extraction
- **`/todo` enhanced:**
  - Now extracts from all today's meetings before generating to-do list
  - Ensures meeting actions/decisions appear in to-do view
  - Uses `/todo-generate` internally after extraction
- **New files:**
  - `scripts/list_items.py` - List and date change commands
  - `scripts/meeting_extractor.py` - Meeting extraction workflow
- **Live test:** Extracted 9 actions, 6 decisions, 5 tasks from 3 meetings

### Session 15: Phase 3.0 Complete (2026-03-18) ← **Current**
- **Slack report command** (`slack report` / `/slack-report`):
  - Searches last 48h for action items via Slack MCP (mentions + direct messages)
  - Finds saved messages from last 7 days
  - Summarizes thread activity across all monitored channels
  - Dedicated paragraph summaries for 3 leadership FY27 channels
  - Automatically creates tasks for each action item (tagged: slack)
  - Tasks displayed as checklist at top of report
- **Slack feature planning:**
  - Reviewed Julie 2.0 brief for all Slack-related capabilities
  - Mapped 6 Slack capabilities to existing/new features
  - Extended 4 existing features (4Ps roundup, automate MFM, daily summary, today report)
  - Created 2 new features (Slack task extraction, leadership update)
  - Created dedicated Slack report feature
- **Configuration updates:**
  - Added channel_groups to .slack_digest_config.json (leadership, growth_team, squads)
  - Added slack report routing to detect_agent.py
  - Updated CLAUDE.md command reference
- **Live test:** Generated report with 11 actions, created 10 tasks, 3 leadership summaries

### Session 15b: Phase 3.1 Complete (2026-03-18) ← **Current**
- **4Ps roundup command** (`4ps roundup` / `team 4ps`):
  - Searches Slack for team 4Ps posts
  - Compares against MFM priorities
  - Generates team summary with alignment flags
  - Output: `Work/Inbox/Today/4ps_roundup_YYYY-MM-DD.md`
- **Leadership update command** (`leadership update` / `prep leadership update`):
  - Reads 3 leadership FY27 channels (last 7 days)
  - Queries Granola for tactical/strategic meeting transcripts
  - Synthesizes 4-6 themes with candidate topics
  - User selects and confirms before sharing to Slack
  - Output: `Work/Inbox/Today/leadership_update_YYYY-MM-DD.md`
- **Daily summary Slack integration:**
  - `get_slack_summary()` now reads slack report as primary context source
  - Falls back to legacy `Work/Slack/` export if no report exists
- **Today report Slack integration:**
  - `/todo` now includes "Slack actions" section
  - Extracts task checklist from slack report and displays in to-do view
  - Verified: 10 tasks showing in to-do document
- **Files modified:**
  - `scripts/daily_summary.py` - slack report as context source
  - `scripts/todo.py` - Slack actions section in to-do list
  - `scripts/detect_agent.py` - routing for 4ps roundup, leadership update
  - `AGENT_REFLECTION.md` - two new workflow sections (~180 lines)
  - `CLAUDE.md` - updated command reference

### Session 15c: Phase 3.2 Complete (2026-03-19) ← **Current**
- **Slack commitment scanning** (`scan slack` / `slack tasks`):
  - Searches user's messages for commitment language ("I'll", "will do", "let me", etc.)
  - Scans team channels for commitments assigned to others ("[Name] to...")
  - Standalone mode: presents for user confirmation before creating
  - Integrated into slack report as Step 4 (auto-creates alongside mentions)
  - Filters out hypotheticals, past tense, and questions
- **Confluence MCP integration:**
  - Strategy agent: 7 key pages mapped (operating model, strategic narrative, product strategy, AI strategy, 5-year roadmap, strategy template, operating rhythm)
  - MFM agent: search for squad strategies and bets during MFM review prep
  - CloudId: `0e31f281-3568-4559-ae88-153abcdead38`, space: `fdo`
  - Progressive loading: local files first, Confluence for latest/live data
  - CLAUDE.md: new Confluence section with page IDs and quick access patterns
- **Julie 2.0 brief status:** All items implemented except MFM Slack notifications (skipped by user request)
- **Files modified:**
  - `AGENT_STRATEGY.md` - Confluence knowledge access section (~100 lines)
  - `AGENT_MFM.md` - Confluence access for MFM context
  - `AGENT_REFLECTION.md` - commitment scanning workflow + scan slack command
  - `detect_agent.py` - routing for scan slack / slack tasks
  - `CLAUDE.md` - Confluence section + scan slack command

### Session 16: Phase 3.3 Complete (2026-06-01) ← **Current**
- **New skill `email-triage`** built on the M365 MCP to classify the unread inbox into priority tiers and route low-priority and action-required mail into dedicated Outlook folders.
- **Tier model:**
  - Tier 1 (VIP): Carl Christensen, Amy Bunszel, Patrick Aragon always; Julie Sylvain when direct
  - Tier 2 (Important): people.md senders, direct-to-you, or Concur approval signals
  - Tier 4: CC-only and sender not in people.md → `Triage-cc`
  - Tier 5: Noise pattern → `Triage - noise`
- **Action Required override:** Tier 1/2 emails with action signals route to `Action required` folder so the inbox stays scannable until cleaned up
- **Body-read rules** for senders that need inspection:
  - Concur (`*@concursolutions.com`): approval signals → action required; charge-submission reminders (`EmailReminderService`) always to noise
  - Gamma/Egencia: receipt signals → `Triage - receipts and travel`; ambiguous → surface "Where to file?"
  - Workday (`*@myworkday.com`): "ACTION REQUIRED" in subject → action required
  - Confluence / SharePoint / Office docs notifications: @mention or action signal in body → action required
  - Autodesk Learning Central → `Triage - learning`
- **Uncertainty rule:** sender doesn't match a pattern or body check is inconclusive → surface in "Where to file?" rather than guess
- **State tracking:** `Work/.state/email_triage.json` persists last-run timestamp so each run picks up only new mail
- **People directory expanded** with 6 contacts:
  - External: Kevin Collins (Ecofold)
  - Leadership: Patrick Aragon (Amy's Chief of Staff), Julie Sylvain (Carl's Chief of Staff)
  - New "Autodesk stakeholders (non-Forma-Design)" section: Ken Nussbaum (Head of Forma Design Sales), James Wedding (Forma Sales Lead), Richard Bao
- **Live test:** processed 6 unread emails. 2 → `Action required` (Workday contract decision, Confluence @mentions), 3 → `Triage - noise`, 1 stayed in inbox (Forma Design CMS meeting invite), 0 ambiguous.
- **Files:**
  - `.claude/skills/email-triage/SKILL.md` (new, ~190 lines)
  - `Work/LLM_Context/Contacts/people.md` (+21 lines)
  - `Work/.state/email_triage.json` (new state file)
- **Triggers:** "triage inbox", "triage email", "process inbox", "clean inbox", "email triage"
- **Outlook folders required** as child folders of Inbox: `Action required`, `Triage-cc`, `Triage - noise`, `Triage - receipts and travel`, `Triage - learning`
- **Commit:** `5144abd Add email-triage skill with tier-based routing and action-required folder`

### Session 17: Phase 3.4 Complete (2026-06-01) ← **Current**
- **New skill `thread-review`** built on the Slack MCP to analyse a single Slack thread end-to-end and draft a voice-aware response.
- **Trigger:** `review thread: [URL]` (plus natural language fallbacks: "what should I do with this thread", "next steps for this thread")
- **Process:**
  1. Parse Slack URL, fetch full thread via `slack_read_thread`
  2. Establish participant set - members (posters, direct @-addresses, DM recipients) vs narrative references
  3. Load five voice/style memory files explicitly (writing style, leadership signature, feedback style, strategic working style, commissioner vs consultant)
  4. Decode reactions/emojis as first-class signal (standard + custom workspace emojis, weighted by sender seniority)
  5. Map thread (topic, trajectory, positions, state, loose threads)
  6. Recommend ONE next move with one-or-two-sentence rationale
  7. Draft response - succinct default, voice-aware, two-filter alignment rule (member AND unresolved POV)
  8. Present four-section output (Topic / Positions / Recommended next move / Draft response)
  9. Offer to push as Slack draft (y / edit / n)
- **Two-filter alignment rule:** a person is only tagged for alignment if (a) they are a member of THIS thread and (b) they have an unresolved POV that needs addressing. Carl signing off via reactions → don't re-tag. Line referenced in narrative context → don't tag despite strong views.
- **Membership heuristic:** narrative @-mentions ("there was a discussion between @X and @Y") do NOT qualify; direct-address @-mentions ("@X, what do you think?") do qualify.
- **Mandatory disclaimer footer** on every drafted response: `_Drafted with Claude. If the tone misses, that's the robot. Read for intent._`
- **Slack draft push** uses `mcp__slack__slack_send_message_draft` with `thread_ts` set - creates a real attached draft in Slack's "Drafts & Sent" without sending. Handles `draft_already_exists` by surfacing not overwriting.
- **Live test:** ran against the FSM (First Strike Moment) alignment thread in `#priv-forma-design-leadership-fy27`. Correctly decoded Carl's `100`+`agree` reactions as deliberate sign-off, correctly excluded Line (narrative reference), correctly tagged Hans and Khushal for alignment. Draft pushed successfully.
- **Files:**
  - `.claude/skills/thread-review/SKILL.md` (new, ~215 lines)
- **Commit:** `15648c3 Add thread-review skill: Slack thread analysis with voice-aware draft response`

### Session 29: Slack digest Group DM + todo Pinned trigger (2026-06-11) ← **Current**
- **Triggered by a daily-digest-for-a-channel ask.** Chris linked a Slack URL (`C0B2566FP0D`) and asked whether existing Julie capability covered it. Reviewed `slack report`, `thread-review`, and channel groups - none produced the lightweight "should I review this more closely" per-channel signal he wanted. Decision: extend existing `slack report` rather than build a new `channel-digest` skill (kept surface area smaller)
- **Identified the linked channel is a Group DM, not a public channel.** Pavlov/Trig conversation with Arne and Mark on cohort setup and instrumentation. This matters because the existing report's Step 1 `to:<@user>` search doesn't work the same way on Group DMs, but `slack_read_channel` does
- **Three edits shipped:**
  - `.slack_digest_config.json`: added `C0B2566FP0D` with new `"type": "group_dm"` field as a discriminator for future per-type handling
  - `.claude/personas/AGENT_REFLECTION.md`: added a Group DM handling note in Step 3 - skip the `to:<@user>` search for `type: group_dm` entries (every message is implicitly to the user), produce a standalone digest section per Group DM with topic summary + key takeaways + actions/asks
  - `.claude/skills/todo/SKILL.md`: added a second Pinned item in Step 3 - checks for `Work/Inbox/Today/slack_report_YYYY-MM-DD.md` and surfaces `not yet run today` or `ran today HH:MM, re-run if you want a fresh sweep` with the trigger command inline. Daily digest is now one click away from the morning todo view
- **Design choice: per-channel last-digest tracking deferred.** Chris initially picked "since last digest" for the window question, then reverted to "add to slack report config" with the existing 48h fixed lookback. Per-channel timestamp state would have required a Python code change to whatever drives the report; not worth it for one Group DM. Revisit if the digest list grows materially or the 48h window starts producing repeats
- **Commit:** `abd6773 Slack digest: add Pavlov Group DM + todo Pinned trigger`

### Session 28: Kjetil FSM thread + misc updates (2026-06-11)
- **Drafted leadership guidance for Kjetil on Building Design FSM.** Picked up the May 26 leadership thread (`What does 'experiencing Forma's value' for the first time mean?`) where Carl/Hans/Khushal aligned on the three-tier framework (FSM = first data-driven answer to a design question; KUI = complete loop once; Upgrade trigger = repeated loops). Kjetil had asked for substance beyond the playbook's "pick one and measure". Drafted reply pushed as a Slack draft into `#forma-squad-building-design` thread: three definitions + three sets of guiding questions (FSM candidates, KUI observability, Upgrade trigger framing) + four-lens ranking framework for choosing among candidates (strategic fit, user pull, reachability, measurability) with a "would they tell a colleague" tiebreaker
- **Pattern 2 positive example logged.** Caught that quoting Khushal back as leadership consensus could read as leading/presumptuous in the public thread - first asked for a neutral header, then dropped the section entirely when the revised framing still wasn't landing. Appended to `Work/LLM_Context/Personal/growth_patterns.md` (not committed - lives locally)
- **Misc commit bundle (8 files, `ee9f79a`).** Not session-driven, but bundled and pushed at session end:
  - `planner-sync` + `todo` SKILL.md: cadence shifted from weekly (>6 days) to daily (>20h). Reasoning: weekly was leaving stale tasks invisible to /todo's selection menu when Planner moved faster than the sync
  - New `Work/LLM_Context/Frameworks/dishes_framework.md`: cooking metaphor (dish/recipe/ingredient) for outcome-based delivery. Dish = use case the user pays for; recipe = workflow; ingredients = capabilities
  - New `Work/Decisions/decision_Designer-per-squad_expectation_reset.md`: from the 10 June org model resource allocation sync with Julie
  - New `Work/People/Projects/Glint action plan.md`: project planning file
  - State file updates (email_triage, planner_sync) from routine skill runs
- **Commit:** `ee9f79a Misc updates: planner-sync to daily, dishes framework, new decision/project docs`

### Session 27: Phase 3.13 Complete (2026-06-11)
- **Problem surfaced during Even 121 prep:** the skill's Slack context gathering relied on `slack_search_public_and_private` results alone, which truncate context to 1-2 adjacent messages. Real signal was hiding in thread replies - decisions, pushback, owners, "who owes whom a reply". The Even prep had to be regenerated after the user asked "do you check the replies attached to conversations?"
- **Fix:** added two new steps to `121-prep/SKILL.md` Step 1:
  1. **Slack channel activity (last 7 days):** broaden beyond DMs to capture threads the person started or was tagged in across channels
  2. **Slack threads - REQUIRED follow-up:** for any surfaced message with `Reply count > 0`, call `slack_read_thread` and extract who responded with what position, what was decided, what's still open, and whether Chris owes someone a reply
- **Behaviour change confirmed in-session.** Re-running thread reads on the Even 121 surfaced: Chris owes Even feedback on the recipe/dishes doc ("Looking forward to reviewing the above" was unanswered); Chris owes Maria an example on the technical-discovery thread; Unified Project thread converged on concrete fixes (NoHubs `trial` branch, polling trial state, remove invite modal). None of this was visible from the search snippets
- **Files:**
  - `.claude/skills/121-prep/SKILL.md` (+11 lines, new "Slack channel activity" and "Slack threads - REQUIRED follow-up step" subsections in Step 1)
- **Same-session prep artefact:** `Work/People/121s/Even/2026-06-11_Even_121_prep.md` (4-topic discussion-led agenda; not committed - lives outside the repo's commit pattern for 121 prep docs)
- **Commit:** `1386b3f 121-prep: require slack_read_thread for surfaced threads`

### Session 26: Phase 3.12 Complete (2026-06-10)
- **Meetings sub-block on the dashboard.** Added a `### Meetings` subsection inside `## Pinned` in today's todo .md. The dashboard renderer reads the subsection and surfaces it as a labeled sub-block within the existing Pinned tile (no new tile, keeps the 12-col grid intact)
- **Design choice: .md as source, dashboard as view.** Meetings live in the markdown so they're visible in Obsidian and survive `/todo-generate` regenerations via the existing skill-curated-sections preservation. Renderer is a pure read - no calendar fetch at render time, no extra auth surface
- **Files:**
  - `.claude/skills/todo/SKILL.md` (Step 3 now writes `### Meetings` after Pinned items; format `HH:MM-HH:MM Title (organiser/context) - prep: [reason]` in Chris's local clock; skip all-day placeholders and self-blocks; omit subsection when empty)
  - `Work/Notes/julie_2/Dashboard/todo/render.py` (gitignored; extracts `Pinned > subs > Meetings` into a `meetings` array; JSX renders a "Meetings" sub-label + items below the pinned list when non-empty)
- **Same-session todo flow improvements (not phase work, captured for traceability).** Bulk task re-dates via direct frontmatter edit when `./pos update:` requires a status; per-direct-report notepad entries for 360 review sharing (created Joe's notepad as it didn't exist)
- **Commit:** `02c96cd todo dashboard: add Meetings sub-block to Pinned tile`

### Session 25: Phase 3.11 Complete (2026-06-09)
- **Problem:** Planner-sync was one-way (Planner → local). When Chris marked a planner-linked task complete locally, Planner stayed open. Concrete miss: "Fix capacity/strategy data" was completed in the local todo on 2026-06-08 but still showed `percentComplete: 0` when the API was queried 24h later
- **Design choice: local-first with a relayed push.** Python writes the local file; Claude pushes to Planner via the m365 MCP. The Python script has no Graph API credentials, so it emits a `[PLANNER_LINKED]` action line in `./pos` output and Claude (always in the loop because `./pos` runs in Claude Code) reads the signal and makes the MCP call. Rejected alternatives: fuzzy auto-matching at task creation (too magic), pure mirror without local files (loses rich context), bidirectional sync with conflict resolution (over-engineered for current usage)
- **Status-aware action signal.** Completed → mark Planner 100% + optional dated comment prepended to description. Blocked/waiting → append a dated note (`YYYY-MM-DD BLOCKED: reason`), don't change percentComplete (Planner has no native blocked state). Other statuses (active, in-progress, on-hold, archived) do NOT emit the signal - no push happens
- **New `link:` command.** `./pos "link: TITLE planner-id: XYZ"` fuzzy-matches a local task and adds `planner-id:` to its frontmatter. Solves the case where a Planner task and a local task were created independently and need to be connected after the fact
- **Bug fix (pre-existing, surfaced by the smoke test).** `update:` handler was passing the matched title to `update_item_status` without the matched file_path, causing the function to reconstruct the filename from the title and fail when the actual file name differed (e.g. `task_Fix_capacity_strategy_data.md` vs the full title with special chars). Now passes `file_path` through
- **Files:**
  - `scripts/create_item.py` (new `get_planner_id` and `link_planner_id_to_file` helpers)
  - `scripts/parse_command.py` (new `parse_link_command` and `link:` handler; `[PLANNER_LINKED]` emission from `update:` handler; pass-through fix for matched file_path)
  - `CLAUDE.md` (new "Planner write-back on status changes" section documenting the `[PLANNER_LINKED]` protocol so future Claude sessions act on it consistently)
- **Smoke test:** `./pos "update: Fix capacity/strategy data status: completed"` → signal fired correctly. Push step intentionally not executed (user opted not to commit a Planner-side change during testing)
- **Commit:** `4bedecc planner write-back: push completion/blocked/waiting from local to Planner`

### Session 24: Phase 3.10 Complete (2026-06-08)
- **Local HTML dashboard for the daily todo.** Single-page React + Tailwind + Geist UI rendered from today's todo .md, served by a small local hub. Bauhaus design (no shadows, hairline borders, rounded-sm, 10px tracked labels) per build brief at `Work/Notes/julie_2/Dashboard/Todo Dashboard - Build Brief & Code Handoff.md`
- **Layout (12-col grid):** Pinned (3) + Focus today (3) + Due today (6) hero row; This week (9, 4 day columns) + Reminders (3, Geist Mono numbered) middle row; Open actions full-width with By person / By date toggle, per-tile clickable overdue/upcoming pill filters, deterministic avatar colors, click-to-expand action rows
- **Multi-dashboard hub.** `Work/Notes/julie_2/Dashboard/_hub.py` is a stdlib HTTP server that auto-discovers any sibling folder with a `render.py` exposing META/render()/optional toggle(). Routes: `GET /` lists all dashboards, `GET /<name>/` renders one, `POST /<name>/toggle` mutates state. Adding a new dashboard = drop a folder. No hub restart needed (modules reload on every request)
- **launchd-managed.** `_hub.plist` registered at `~/Library/LaunchAgents/com.chris.dashboard-hub.plist`. Auto-starts at login, restarts on crash, binds to `127.0.0.1:8765` only. Logs at `~/Library/Logs/dashboard-hub.log`. Verified running (`launchctl list | grep dashboard-hub`)
- **Click-to-tick.** Checkboxes on Due today, Reminders, Tasks-this-week, and expanded Open actions. Frontend posts `{lineNumber, checked}` to `/todo/toggle`. Backend calls `./pos "update: TITLE status: completed"` to update source files via existing fuzzy match, then flips `[ ]` to `[x]` in the .md. Optimistic UI with rollback on failure
- **Same-day persistence fix (the two bugs the user caught).** `scripts/todo.py get_items_from_folder()` was filtering all completed items, dropping ticked items on regen. Fixed to keep items completed today. `generate_todo()` was rebuilding the .md from scratch and wiping skill-curated sections; added `extract_sections_from_md()` to preserve Pinned + Focus today + Yesterday's overview verbatim across same-day regenerations. New day generates fresh; same day preserves state
- **Focus items as commitments.** New SKILL.md Step 6.5: after writing Focus today, ensure each focus item has a task due today - re-date an existing matching task or create a new tracking task (batched user confirmation per the existing `feedback_confirm_before_creating_items` rule). Re-runs `/todo-generate` so the new tasks appear in Due today
- **Project structure for the dashboard (gitignored, lives in `Work/Notes/julie_2/Dashboard/`):**
  - `_hub.py` (multi-dashboard HTTP server)
  - `_hub.plist` (launchd manifest)
  - `README.md` (install/uninstall/restart instructions)
  - `todo/render.py` (todo dashboard parser + JSX renderer)
- **New memory:** `reference_julie2_dashboard_folder.md` codifying the convention that all dashboard artifacts live in `Work/Notes/julie_2/Dashboard/`
- **Files (visible in repo):**
  - `scripts/todo.py` (preservation + completed-today retention)
  - `scripts/parse_command.py` (rebuild hook points at the new render.py location)
  - `.claude/skills/todo/SKILL.md` (new Step 6.5)
- **Commit:** `870d01a todo: preserve skill-curated sections + ensure focus items land in due today`

---

### Session 23: Phase 3.9 Complete (2026-06-08)
- **Problem:** `/todo` Step 5 surfaced ~19 options and let the user pick freely. Predictable failure mode is over-selection - the Focus today list became a wish list, not a forcing function. Also assumed self-blocks were unavailable time, shrinking the day artificially
- **Three rules added** based on Chris's working pattern:
  1. **Workday = 08:30-18:00 (9.5h)**, self-blocks are work time (strategic / meeting prep / lunch 12:30-14:00), Monday subtracts an additional 2h for the weekly prep block (email triage, 4Ps writing, /todo run, week planning)
  2. **Cap Focus today at 3 items**, default mix 1 strategic (4Ps) + 2 tactical (sized S/M/L)
  3. **Challenge logic before write:** if picks > 3, if no strategic chosen, if sized minutes > available focus time, or if meetings >60% of workday - skill must surface the gap and ask for revision, not just save
- **`.claude/skills/todo/SKILL.md` Step 5 rewrite:** added "Compute available focus time" block, re-bucketed menu into Strategic / Meetings / Tactical, size-tagged tactical items, added Step 5.5 challenge logic before Step 6 write
- **Monday 4Ps reminder relocation:** removed the standalone `## Monday reminder: weekly 4Ps` section from `scripts/todo.py` (it sat after the auto-created task and before Overdue tasks). Now appears as a second Pinned bullet on Mondays via SKILL.md, alongside the 2h weekly prep block - keeps all Pinned signal in one scannable section
- **Two new memory files** to make the rules durable across sessions:
  - `feedback_workday_pattern.md` (workday hours, blocks, Monday prep convention)
  - `feedback_todo_focus_rules.md` (cap, mix, challenge triggers)
  - MEMORY.md index updated
- **Bulk task hygiene** done at start of session: 6 updates including 1 conversion (task → action assigned to Anders) and 2 deletes (10% prep per area no longer needed; old confirm-Anders task replaced by the action). Date moves: Lavinia/Hans chat to 11 Jun, Glint follow-up and capacity/strategy data fix to today, Trig presentation reminder to 22 Jun
- **Today's todo regenerated under the new rules:** available focus time 6.0h (9.5h - 1.5h Tactical - 2h Monday prep), Focus today reduced from 4 items to 3 (Trig deep work, ship D&C Home strategy to Richard/Ilai, fix capacity/strategy data)
- **Files:**
  - `.claude/skills/todo/SKILL.md` (Step 5 rewrite + new Step 5.5 + Monday Pinned additions)
  - `scripts/todo.py` (Monday reminder section removed)
  - `~/.claude/projects/-Users-smallc-AI-Chief-of-staff/memory/feedback_workday_pattern.md` (new)
  - `~/.claude/projects/-Users-smallc-AI-Chief-of-staff/memory/feedback_todo_focus_rules.md` (new)
  - `~/.claude/projects/-Users-smallc-AI-Chief-of-staff/memory/MEMORY.md` (index updated)
- **Commits:**
  - `1ba7b93 todo skill: cap focus at 3, add workday time math and challenge logic`
  - `b07cc1f todo skill: move Monday 4Ps reminder into Pinned section`

---

### Session 22: Phase 3.8 Complete (2026-06-08)
- **Problem identified mid-`/todo`:** on Sunday 2026-06-07 the workflow scanned literally yesterday (Saturday, empty) and silently dropped Friday's two meetings. Existing `feedback_monday_meetings.md` memory only codified the Monday-to-Friday case; gaps from weekends, post-holiday returns, and PTO weren't handled
- **`scripts/parse_command.py` /todo branch:** Granola-side scan now walks back up to 7 days from yesterday and stops at the first date with meetings. Skips empty dates (weekends, holidays, PTO). Confirms before creating items per `feedback_confirm_before_creating_items`
- **`scripts/todo.py` `get_previous_working_day`:** rewritten to scan `Work/Daily_Logs/` for the most recent date with a `daily_summary_*.md` or `claude_sessions_*.md` file (proxy for "a day Chris actually worked"). Falls back to Monday-to-Friday rule if no log file found in 7-day window. Verified: Sun 6/7 returns Fri 6/5, correctly skips empty Sat 6/6
- **Memory:** rewrote `feedback_monday_meetings.md` to generalise from "Mondays look back to Friday" to "most recent active day, skip weekends/holidays/PTO". MEMORY.md index updated to match
- **Friday gaps closed:** verified Forma Futures Contest Strategy fully processed (4 decisions + 12 actions). Mairead 121 was partially processed (US Comm Mgr hiring, design competition captured) but the 121 log hadn't been updated past 2026-04-27 and London June 16-17 working sessions weren't captured anywhere. Wrote 5 June 121 log entry and created `task_Lock_prep__agenda_for_London_June_16-17_sessions_with_Mairead.md`
- **Bonus task captured:** investigated FY27Q2 Portfolio Optimization & Reinvestment requirement via Confluence (pages 869665006 + 880967681); created focused task for Chris's section of the pre-read (10% give-back, 8 Growth squads = 29 heads, two tables + 8-min in-room slot)
- **Files:**
  - `scripts/parse_command.py` (/todo lookback walk)
  - `scripts/todo.py` (`get_previous_working_day` rewrite)
  - `~/.claude/projects/-Users-smallc-AI-Chief-of-staff/memory/feedback_monday_meetings.md` (generalised)
  - `~/.claude/projects/-Users-smallc-AI-Chief-of-staff/memory/MEMORY.md` (index updated)
  - `Work/People/121s/Mairead/121_log.md` (5 June entry, private, not tracked)
  - 2 new tasks in `Work/Inbox/Tasks/` (private, not tracked)
- **Commit:** `e236214 julie /todo: look back to most recent active day, not literal yesterday`

---

### Session 21: Content + Pattern Logging (2026-06-07)
- **Strategic Accounts MFM summary applied the focused format** (validates the Session 20 mfm-summary skill rewrite): key takeaways, decisions, actions with owners and due dates, pre-read delta table, not-covered list. Cut the previous narrative summary and Slack block; tightened from 100 lines to 68
- **Growth pattern - Commissioner positive example:** appended a third positive case to `growth_patterns.md` covering three clean outcome-and-bar moves in the Strategic Accounts MFM (prep doc asked Anders to restate output-shaped outcomes without prescribing rewrites; in the meeting set outcomes and asked Sid/Robin to fill in the method; left adoption-ownership note for Anders to draft). Same shape as Joe IDP and Maria recaps - name the outcome and quality bar, leave the how to the recipient
- **Mairead 121 prep generated via 121-prep skill** (file in private `Work/People/121s/Mairead/`, not tracked). Iterated to focus on her two priorities (US hire + US market understanding), with design competition as reflection-only and goals/OKRs/strategy/AI strategy review pushed to the London 16-17 working sessions
- **Files:**
  - `Work/Process/MFM/June/strategic_accounts_mfm_summary.md` (rewrite)
  - `Work/LLM_Context/Personal/growth_patterns.md` (Strategic Accounts MFM positive example)
- **Commit:** `4847a61 strategic-accounts MFM: focused summary + Commissioner pattern example`

---

### Session 20: Phase 3.7 Complete (2026-06-05)
- **Standing meetings reference mapping:** new `Work/LLM_Context/Admin/standing_meetings.md` lookup file keyed by meeting title, with fields for aliases, cadence, owner, Slack channel, core attendees, purpose, recurring topics, prep style, and prior prep location
- **AGENT_MEETINGS.md primary-lens rule:** when `prep meeting:` runs and the title fuzzy-matches a mapping entry, the entry becomes the PRIMARY source for context-gathering, not a supplement. The entry's `Purpose`, `Recurring topics`, and `Prep style` scope every downstream Granola/Slack/decisions query. Generic sweeps only happen when no entry matches
- **Cadence-driven soft lookback:** the entry's `Cadence` drives the channel/DM/Granola review window (weekly = ~7 days, biweekly = ~14, monthly = ~30). Soft anchor, not a hard rule - extends if a thread spans further
- **Seeded with People Allocation Weekly Sync** as entry #1 (channel C0A7E7PFJ6M, weekly Thursdays 13:00 CET, owned by Julie Sylvain)
- **Full prep→meeting→post-meeting cycle exercised** on People Allocation sync (2026-06-04): prep generated through the new lens correctly narrowed to Q3 consultant funding (Julie's actual agenda), post-meeting summary built from Granola transcript, 4 tasks + 3 decisions created (Filip Hagen renewed Q3, Autodesk Assistant deferred to Q4, Tamira XF support routed via next funding conversation)
- **Growth pattern:** appended Pattern 3 positive example to `growth_patterns.md` - accepted Julie's pushback on the hiring-acceleration framing (real bottleneck is candidate processing via Memo Services, not sourcing) without re-pitching. Classic Pattern 3 inverse
- **Files:**
  - `Work/LLM_Context/Admin/standing_meetings.md` (new)
  - `.claude/personas/AGENT_MEETINGS.md` (primary-lens block under Step 2 of Pre-Meeting Workflow)
  - `Work/LLM_Context/Personal/growth_patterns.md` (Pattern 3 positive example)
  - `Work/Meetings/Prep/2026-06-04_People_Allocation_Weekly_Sync_prep.md`
  - `Work/Meetings/2026-06-04_People_Allocation_Weekly_Sync.md`
  - 3 decision files in `Work/Decisions/`
- **Commits:**
  - `e899a79` (standing-meetings infra, bundled with MFM skills refactor)
  - `5f409f2 Q3 consultant decisions and Pattern 3 positive example from People Allocation sync`

---

### Session 19: Phase 3.6 Complete (2026-06-04)
- **Todo completion-sync fix:** ticking `[x]` in any todo file now propagates to the underlying task file on the next `/todo` run, regardless of when the run happens
- **Three coordinated changes in `scripts/todo.py` + `scripts/create_item.py`:**
  1. `generate_todo()` now scans the **most recent prior todo on disk** (not just today's file) for `[x]` items before generating the new list. Covers the common case where boxes are ticked at end of day and `/todo` is next run the following morning
  2. `get_items_from_folder()` filters out items where `status` is `completed` or `archived` so the new list is clean - completed items drop out instead of sitting at the top with a check mark
  3. `update_item_status()` accepts an explicit `file_path` parameter. Previously rebuilt the filename from the title, which fails when title and filename don't round-trip (e.g. `task_Glint_next_steps.md` holds "Reminder: Follow up Julie re Glint resource"). The sync now passes the path that fuzzy-match already found
- **Net flow:** tick `[x]` → next `/todo` runs sync against prior file → source task files updated to `status: completed` → generator skips them → fresh list, no ghosts. Yesterday's todo file remains untouched as a historical snapshot
- **No cron/auto refresh:** confirmed via `crontab -l`, no `LaunchAgents`, no `scheduled_tasks` config. `/todo` is purely user-triggered, so the sync-then-filter flow is the entire loop. No manual/auto modes needed
- **Email-triage rule addition:** `Updated invitation:` subject prefix added to the Force-to-noise universal overrides. Outlook organiser-update notifications are redundant with the calendar entry itself, so they auto-route to noise alongside `Accepted:`/`Declined:`/`Tentative:`/`Cancelled:`
- **Similar-items warning expansion:** `create_item.py` warning now shows the full `file://` path of the matched item and the full details text (no 120-char truncation). User can verify the match before deciding whether to create a new item or update the existing one
- **Files:**
  - `scripts/todo.py` (prior-todo sync block, completed/archived filter, file_path passthrough)
  - `scripts/create_item.py` (file_path param on update_item_status, full path + full details in warning)
  - `.claude/skills/email-triage/SKILL.md` (Updated invitation: rule)
- **Commit:** `a8bf95b todo: sync ticked items from prior todo, hide completed items, expand similar-items warning`

---

### Session 18: Phase 3.5 Complete (2026-06-03)
- **Todo skill upgrade:** added Steps 5-6 to `/todo` for an interactive "Today's options" menu that surfaces what Chris should focus on today vs leave for later
- **Five sources gathered:**
  1. This week's 4Ps priorities (latest file in `Work/Inbox/4Ps/[Month]/`, fallback to prior week if not yet written)
  2. Today's meetings via m365 calendar with "prep needed" flag for VIP 1:1s, MFM, leadership sync
  3. Slack DMs from VIPs (last 5 days, unanswered by Chris)
  4. Slack @mentions in shared channels for VIPs + direct reports (last 5 days, unreplied)
  5. Tasks from `./pos /todo` output (overdue, due today, due in <=3 days)
- **Bucketed numbered menu** displayed in terminal; user picks by number (or `all` / `none`). Selected items written as `## Focus today` section in the todo file, inserted immediately after Pinned. Each item gets a source tag, e.g. `[4Ps]`, `[Meeting prep]`, `[Carl]`, `[Task]`
- **VIP source unification:** email-triage no longer hardcodes the 4 VIPs. Both skills now parse `## Leadership` from `Work/LLM_Context/Contacts/people.md` as the single source of truth. Add or remove a name in Leadership once, both skills track it. Patrick's always-Tier-1 and Julie's conditional-Tier-1 nuances preserved
- **Direct reports model:** people.md role field now uses `, direct report` suffix to mark Chris's directs (Joseph Price, Even Olstad, Anders Wester, Mairead Morgan). Parsed dynamically by the todo skill - no separate file
- **Cost note:** new /todo flow adds ~9 Slack scans + 1 calendar pull + 1 4Ps read per run (~30-60s slower). Acceptable given daily ritual frequency. Tier 2 (wider squad) explicitly excluded from the Slack scan to keep the cost bounded
- **Files:**
  - `.claude/skills/todo/SKILL.md` (Steps 5-6 added, frontmatter description updated)
  - `.claude/skills/email-triage/SKILL.md` (Tier 1 row, workflow step 4, frontmatter description)
  - `Work/LLM_Context/Contacts/people.md` (direct-report markers; Leadership table positioned as VIP source)
- **Commit:** `954a4d4 todo + email-triage: add Today's options menu, unify VIP source via people.md Leadership`

---

## Development Status Summary (Session 20)

### Fully Working
- ✅ **Tasks Agent:** new task, new idea, new reminder, new decision, update, change due date, /todo, archive completed, process notepad, actions list, decisions list, new_daily
- ✅ **People Agent:** observation, 360 review (creates template)
- ✅ **Meetings Agent:** prep meeting, 121, post meeting (auto-extraction), finalize meeting
- ✅ **MFM Agent:** mfm review, mfm summary
- ✅ **Hiring Agent:** setup role, screen CVs (validates folders)
- ✅ **Reflection Agent:** session logging, daily summary, 4Ps generation, Slack report, scan slack, 4Ps roundup, leadership update
- ✅ **Strategy Agent:** OKR/strategy/bet queries with progressive disclosure + Confluence MCP

### Key Enhancement (Session 15)
- `slack report` generates comprehensive Slack report with auto task creation + commitment scanning
- `scan slack` standalone commitment extraction with user confirmation
- `4ps roundup` reviews team 4Ps from Slack against MFM priorities
- `leadership update` synthesizes leadership channels + meetings into shareable update
- `/todo` includes Slack actions section; daily summary uses slack report as context
- Strategy + MFM agents have live Confluence access for OKRs, strategies, bets, operating model

### Key Enhancement (Session 17)
- `review thread: [URL]` analyses any Slack thread, decodes emoji/reaction signal, and drafts a voice-aware response with optional one-step push to Slack drafts
- Two-filter alignment rule (member + unresolved POV) prevents tagging non-participants or already-aligned members
- Mandatory Claude disclaimer footer on every drafted response

### Key Enhancement (Session 18)
- `/todo` now surfaces a bucketed numbered menu of "Today's options" pulled from this week's 4Ps priorities, today's meetings, VIP/direct-report Slack signals (last 5 days), and tasks due today/overdue/next 3 days
- User selects items by number; selections written as `## Focus today` section in the todo file after Pinned
- VIP membership unified: email-triage + todo both parse `## Leadership` in people.md instead of hardcoding names. Single source of truth
- Direct reports modelled in-line on people.md role field (`, direct report` suffix) - no separate directs file to maintain

### Key Enhancement (Session 19)
- Ticking `[x]` in any todo file now syncs to the underlying task on the next `/todo` run: prior-day file is scanned, source frontmatter is updated to `status: completed`, and completed items are filtered out of the new list
- `update_item_status()` now accepts an explicit `file_path` so the sync uses the fuzzy-matched path rather than rebuilding the filename from the title (titles don't always round-trip to filenames)
- Email-triage adds `Updated invitation:` to Force-to-noise universal overrides; Outlook organiser-update notifications auto-route to noise
- `create_item.py` similar-items warning shows the full `file://` path and full untruncated details so the user can verify the match before deciding whether to create or update

### Key Enhancement (Session 20)
- New `Work/LLM_Context/Admin/standing_meetings.md` mapping turns recurring meetings into a lookup keyed by title (aliases, cadence, owner, Slack channel, attendees, purpose, recurring topics, prep style)
- `prep meeting:` now uses the mapping as the primary lens when matched: purpose/topics/prep-style scope every downstream Granola/Slack/decisions query rather than running generic sweeps. Falls back to default discovery when no entry matches
- Soft cadence-driven lookback (weekly ~7d, biweekly ~14d, monthly ~30d) aligns channel/DM/Granola review window to meeting rhythm. Extensible if a thread spans further
- Seeded with People Allocation Weekly Sync entry #1; full cycle exercised end-to-end (prep, attend, post-meeting summary, item creation)

### Partially Working / Known Issues
- None currently

### Not Implemented (from Julie 2.0 Brief)
- ✅ `actions` list command (Session 14)
- ✅ `change due date:` command (Session 14)
- ✅ `new_decision:` and `decisions` list (Session 14)
- ✅ `new_daily` contribution notes (Session 14)
- ✅ Meeting transcript auto-extraction (Session 14)
- ✅ Slack report with action extraction and task creation (Session 15)
- ✅ Leadership FY27 dedicated summaries (Session 15)
- ✅ 4Ps team roundup from Slack vs MFM priorities (Session 15)
- ✅ Leadership update workflow with synthesis + confirmation before sharing (Session 15)
- ✅ Daily summary reads slack report as context (Session 15)
- ✅ Today report includes Slack actions section (Session 15)
- ✅ Slack commitment scanning - scan slack / slack tasks (Session 15)
- ✅ Confluence MCP integration for Strategy + MFM agents (Session 15)
- ❌ MFM Slack notifications (reminders + team sharing - skipped by user request)

---

**End of Project Summary**
