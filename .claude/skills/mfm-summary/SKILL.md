---
name: mfm-summary
description: >
  Process a Monthly Focus Meeting after it happens. Finds the meeting in Granola
  (confirms with user before proceeding), extracts decisions, actions, and updates
  from the pre-read, then cross-references against the MFM review prep to identify
  what was not covered from the previous MFM. Produces a structured summary file
  (without Slack block or Julie items), then shows the Slack-ready summary and
  proposed Julie items in the terminal for confirmation. Use when "mfm summary:
  [squad] [month]", "post mfm: [squad]", "summarise the mfm", or after attending
  an MFM. NOT for pre-meeting review (use mfm-review).
---

# MFM summary

Process a Monthly Focus Meeting after it happens. Combines the Granola meeting transcript with the MFM review prep to produce a complete post-meeting summary.

## Trigger phrases

- `mfm summary: [squad] [month]`
- `post mfm: [squad] [month]`
- "summarise the mfm"
- "what came out of the mfm?"

## Process

### Step 1: Find MFM prep/review

Look for existing MFM review output at: `Work/Process/MFM/{Month}/{squad}_mfm_review.md`

If found, load it - this contains the dimensional analysis, key questions, and concerns raised pre-meeting. If not found, note this and continue without cross-referencing.

### Step 2: Find the meeting in Granola

1. Search Granola: `mcp__granola__list_meetings(time_range="this_week")` or `last_week`.
2. Match by squad name or "monthly focus meeting" in the title.
3. Present the match to the user and confirm before proceeding:
   - Show: meeting title, date, duration, attendees
   - Ask: "Is this the right meeting?"
   - If multiple matches, show options and ask which one.
   - If no match, ask the user for the meeting date or offer manual input.
4. Once confirmed, get the full summary and transcript via Granola MCP.

### Step 3: Extract key content from transcript

From the Granola transcript and summary, extract:
- Decisions made - what was decided, rationale, who made it.
- Actions assigned - owner, action, timing.
- Changes from the pre-read - anything that shifted in allocation, scope, or sequencing.
- Follow-up items - things needing further work.
- Key takeaways - the most important signals to carry into the next month and into other squads.

### Step 4: Cross-reference with MFM prep

If the MFM review was loaded in Step 1, surface only:
- Not covered from previous MFM - questions, concerns, or commitments from the prep that did not get airtime. This is the high-value output.

Do not include an "addressed" recap or a "new items surfaced" section in the saved file. Anything genuinely new and important belongs in the Key takeaways section at the top.

### Step 5: Generate the saved summary file

Create file at: `Work/Process/MFM/{Month}/{squad}_mfm_summary.md`

Use the following structure exactly. Sentence case for headings. No bold inside bullets or prose. Use single quotes for emphasis or referenced terms; double quotes only for direct quotes from the meeting.

```markdown
# MFM summary: [Squad] - [Month] [Year]

Date: [Meeting date and time]
Attendees: [List]
Pre-read: [Link to Confluence page]
Prep doc: [Relative link to mfm_review.md if present]
Granola: [Link to Granola note]

## Key takeaways

- [5-7 punchy takeaways covering: focus, capacity allocation reality, dependencies and mitigation, orchestration vs build patterns, risks acknowledged, methodology decisions (e.g. proxy metrics, V1 scoping bar), open threads for next month. Each should be standalone and carry signal that is useful outside the squad too.]

## Decisions made

1. [Decision] - [rationale or context, single line]
2. ...

## Actions

- [ ] [Owner] - [Action] ([date or week])
- [ ] ...

## Updates from pre-read

| From pre-read | Landed at |
| --- | --- |
| [Plan element from pre-read] | [How it actually landed] |
| ... | ... |

## Not covered from previous MFM

- [Question/commitment from prep that did not get airtime] - [why it matters, suggested follow-up]
- ...

## Follow-up required

- [Person or topic] - [What needs to happen, when]
- ...
```

Do not include a Slack summary block or a Julie items list in the saved file. Those go to the terminal only.

If no MFM prep was available, omit the "Not covered from previous MFM" section entirely.

### Step 6: Show Slack-ready summary in terminal

Display the Slack summary in the chat for the user to copy. Do not save it to the file. Use two subheads (Key takeaways, Actions) plus a Confluence reference placeholder.

Format:

```
*[Squad] MFM - [Month]*

*Key takeaways*
* [5 short takeaways drawn from the saved doc]

*Actions*
* [Owner]: [Action] ([when])
* ...

Full notes in Confluence: [link to be added]
```

Guidelines for the Slack summary:
- Exclude sensitive content (personal feedback, performance observations, compensation, HR matters).
- Be specific with timing ("this week", "by Friday", "next week"). No vague phrasing.
- Keep it scannable - aim for 5 takeaways and 3-5 actions.

### Step 7: Show proposed Julie items in terminal

Display the proposed Julie items in the chat for the user to confirm. Do not save them to the file.

Format:

```
Proposed Julie items:
1. `new action: [title]` assignee: [Person] - due: [YYYY-MM-DD]
2. ...

Confirm before I create them.
```

Only create items after the user confirms. Use `./pos "new action: ..."` for actions with an assignee, `./pos "new task: ..."` for items owned by Chris.

### Step 8: Publish to Confluence

After the local file is saved, publish the summary to Confluence so the team can reference it.

**Location:**
- Parent folder for all MFM summaries: `843778273` in the `fdo` space (cloudId `0e31f281-3568-4559-ae88-153abcdead38`, spaceId `641548109`).
- Each month gets its own subfolder under that parent (e.g. June, July). The subfolder is itself a Confluence folder, not a page.

**Process:**
1. Use `getConfluencePageDescendants(pageId="843778273")` or a CQL query to find an existing folder for the target month under `843778273`.
2. If a folder for the month exists, use its ID as the `parentId`. Confirm the folder ID with the user before creating the page.
3. If no folder exists for the month, ask the user to create it manually (folder creation is not supported by the MCP) and provide its ID, or fall back to using `843778273` directly and flag that the month folder needs creating.
4. Create the page with `createConfluencePage` using `contentFormat: "markdown"`. Title format: `[Squad] MFM - [Month] [Year] - Summary` (sentence case, with the year).
5. Capture the returned page URL.

### Step 9: Update the Slack draft with the Confluence link

After the page is published, replace the `[link to be added]` placeholder in the Slack draft with the actual Confluence URL. Push the draft again to Slack (this overwrites the prior draft in the DM thread).

### Step 10: Confirm and offer next steps

1. Confirm the local file location, the Confluence page URL, and the Slack draft channel.
2. Save a memory entry summarising the key decisions for trend tracking across months.

## Style rules

- Sentence case for headings and titles.
- No em dashes. Use a regular hyphen or restructure.
- Bold is only for headings. Do not use bold inside bullets or prose paragraphs.
- Quotes: double quotes only when quoting what someone actually said; single quotes for emphasis, referenced terms, or hypothetical phrasing.
- Continuous single-line paragraphs and bullets (no hard breaks within prose).

## Error handling

- Granola meeting not found: ask the user for a meeting date, offer to search a different time range, or accept manual input.
- MFM prep not found: continue without cross-referencing, omit the "Not covered from previous MFM" section.
- Confluence unavailable: not needed for the summary; this skill works from Granola.
