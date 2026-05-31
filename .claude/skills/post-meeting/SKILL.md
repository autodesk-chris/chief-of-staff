---
name: post-meeting
description: >
  Process a meeting after it happens - find in Granola, extract key takeaways,
  actions, decisions, and observations, create items in Julie, save a structured
  summary with Slack-ready format. Use when "summarise my meeting with [person]",
  "post meeting: [title]", "meeting notes for [person]", "what came out of my
  meeting". NOT for meeting prep (use the Meetings agent).
---

# Post-meeting summary

Process a meeting after it happens. Finds the meeting in Granola, extracts key takeaways, actions, decisions, and observations, creates items in Julie, saves a structured summary, and generates a Slack-ready version for sharing.

## Trigger phrases

Natural language - activate when the user says things like:
- "summarise my meeting with [person]"
- "review the [meeting name]"
- "post-meeting notes for [meeting]"
- "process the [meeting name] meeting"
- "what came out of my meeting with [person]?"
- "meeting summary for [person/title]"
- `post meeting: [title]`

## Process

### Step 1: Find the meeting in Granola

1. Use the person name or meeting title from the user's request
2. Search Granola: `mcp__granola__list_meetings(time_range="this_week")` or `last_week` if not found
3. If multiple matches, show options and ask which one
4. Get the full summary: `mcp__granola__get_meetings(meeting_ids=["<id>"])`
5. If the summary is thin or user wants deeper analysis, get the transcript: `mcp__granola__get_meeting_transcript(meeting_id="<id>")`

### Step 2: Determine meeting type and save location

**121s with direct reports or manager:**
- Check if the person is in `Work/LLM_Context/Squads/Squads_overview.md` (direct report) or is Chris's manager (Carl)
- Save to: `Work/People/121s/[person_name]/121_YYYY-MM-DD.md` (direct reports) or `Work/People/[person_name]/121/[descriptive_title]_YYYY-MM-DD.md` (manager/others)
- Create the folder if it doesn't exist

**All other meetings:**
- Save to: `Work/Meetings/YYYY-MM-DD_Meeting_Title.md`

### Step 3: Extract and structure content

From the Granola summary (and transcript if available), extract:

1. **Key takeaways** (3-5 bullets) - main insights, important context, decisions and their reasoning
2. **Actions** - person responsible, what they need to do, timing
3. **Decisions** - what was decided, rationale, who made it
4. **Observations** - feedback about team members (positive or developmental)

### Step 4: Create the summary file

Use this format:

```markdown
# [Meeting Title] - YYYY-MM-DD

**Attendees:** Names
**Type:** [121 / Strategy / Budget / Operations / Team]

## Key takeaways
- Takeaway 1
- Takeaway 2
- Takeaway 3

## Actions
- [Person]: [Action] (by [timing])
- [Person]: [Action] (by [timing])
- You: [Action] (by [timing])

## Decisions
- [Decision] - [brief rationale]

## Observations
- [Person] - [observation]

---
**Slack-ready summary:**
Takeaways
* [Key takeaway 1]
* [Key takeaway 2]
* [Key takeaway 3]

Actions:
* [Person 1]
    * [Action] (by [timing])
    * [Action] (by [timing])
* [Person 2]
    * [Action] (by [timing])

---
Processed by Meetings Agent
```

### Step 5: Create items in Julie

For each extracted item, create via `./pos`:

- **Actions assigned to others:** `./pos "new action: [action title] assignee: [Person] details: [context from meeting] due: [date]"`
- **Tasks for Chris:** `./pos "new task: [task title] details: [context from meeting] due: [date]"`
- **Decisions:** `./pos "new decision: [decision] participants: [names] rationale: [why]"`
- **Observations:** `./pos "observation: [Person] - [feedback text]"`

**Before creating items:** Check if the user has already created these items earlier in the conversation. Don't duplicate.

### Step 6: Present the output

1. Show the Slack-ready summary format in the conversation (Takeaways + Actions grouped by person) - this is the primary output the user sees in the terminal
2. Confirm the file was saved and where
3. List items created (actions, tasks, decisions, observations)
4. Offer: "Want me to send the Slack summary to [person/channel]?"

## Guidelines

- **Exclude sensitive content from Slack summaries:** Personal feedback, performance observations, compensation, HR matters
- **Be specific with timing:** "by Friday", "this week", "end of month" - not vague
- **Focus on outputs not discussion:** What was decided and who does what, not a play-by-play of the conversation
- **Slack format:** Use bullets (*) not dashes, include person names with actions, keep it standalone (readers may not have context)
- **Don't ask permission for file reading** - just gather context automatically
- **Do confirm before sending Slack messages**

## Call reflection (121s only)

After completing the summary for a 121 meeting, check if `Work/LLM_Context/Personal/growth_patterns.md` exists. If it does, and a transcript is available, run a quick check of the conversation against Chris's known patterns (over-explaining, giving answers vs asking questions, airtime imbalance, doubling down on influencing). Flag anything noticed, as per the call-reflection skill.
