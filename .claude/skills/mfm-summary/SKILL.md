---
name: mfm-summary
description: >
  Process a Monthly Focus Meeting after it happens. Finds the meeting in Granola
  (confirms with user before proceeding), extracts decisions, actions, and updates
  from the pre-read, then cross-references against the MFM review prep to identify
  what was not covered from the previous MFM. Runs in two gated steps: (1) draft
  the summary in the terminal and iterate to approval before saving; (2) only once
  the summary is approved and saved, generate the Slack-ready summary and proposed
  Julie items in the terminal for confirmation. Use when "mfm summary: [squad]
  [month]", "post mfm: [squad]", "summarise the mfm", or after attending an MFM.
  NOT for pre-meeting review (use mfm-review).
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

### Step 5: Draft the summary in terminal, iterate to approval, then save

This is a two-part step and a hard gate for the rest of the skill. Do NOT generate Slack or Julie output until the summary file has been approved and saved.

1. Draft the full summary content in the terminal using the structure below. Do not save the file yet.
2. Ask the user for comment. Iterate on the draft until they approve. Expect meaningful edits on the first pass (owner reassignments, framing, deletions).
3. Only once the user has explicitly approved, save the file to `Work/Process/MFM/{Month}/{squad}_mfm_summary.md`.
4. Do not proceed to Step 6 (Slack) or Step 7 (Julie) until the summary is saved.

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

In the saved file and the Confluence page, actions name the actual delivery person, not the squad lead. This is the team-facing record, so it should reflect who is doing the work.

- [ ] [Delivery person] - [Action] ([date or week])
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

Only run this step after Step 5 has been approved and the summary file has been saved. If the summary is still in draft/iteration, do not produce Slack output yet.

Display the Slack summary in the chat for the user to copy. Do not save it to the file. Use two subheads (Key takeaways, Actions) plus a Confluence reference placeholder.

In the Slack summary, actions are attributed to the squad lead (the accountable owner), even where delivery is delegated. The Confluence/file version is the team-facing record and names the delivery person; the Slack summary is the leadership-facing record and names the accountable owner. This split is intentional.

Items that Chris owns and has already actioned should appear as a single Actions line ("Chris: already followed up - ...") rather than as a separate item. Items that were in the prep doc but did not get airtime should be surfaced in Actions as a re-ask ("[Squad lead]: re-ask of the meeting - ...") so they are not buried.

Format:

```
*[Squad] MFM - [Month]*

*Key takeaways*
* [5 short takeaways drawn from the saved doc]

*Actions*
* [Squad lead]: [Action] ([when])
* ...

Full notes in Confluence: [link to be added]
```

Guidelines for the Slack summary:
- Exclude sensitive content (personal feedback, performance observations, compensation, HR matters).
- Be specific with timing ("this week", "by Friday", "next week"). No vague phrasing.
- Keep it scannable - aim for 5 takeaways and 3-5 actions.

### Step 7: Show proposed Julie items in terminal

Only run this step after Step 5 has been approved and the summary file has been saved. Slack and Julie can be shown together in one turn once the summary is locked.

Display the proposed Julie items in the chat for the user to confirm. Do not save them to the file.

Rules:
- The assignee on every squad-derived Julie action is the squad lead. The Julie tracker is the accountable-owner view, matching the Slack summary.
- The title leads with the delivery person where delegated: `[Delivery person] to [verb] [object]`. If the squad lead is also the delivery person, use `[Verb] [object]`.
- The detail field always names the delivery person explicitly ("Owned by [lead], delivery by [name]") and captures the rationale.
- Default due date is mid-month (the Monday roughly two weeks before next MFM). Only use end-of-month for items that genuinely need the full window (proposals, multi-stage builds).
- Do NOT propose Julie items that Chris owns and has already actioned. Surface those in the Slack summary as a single callout line only.
- Do NOT propose Julie items where Chris is the owner unless he has not yet started.

Format:

```
Proposed Julie items:
1. `new action: [Delivery person] to [verb] [object]` assignee: [Squad lead] - due: [YYYY-MM-DD]
   details: Owned by [Squad lead], delivery by [Person]. [Rationale and context.]
2. ...

Confirm before I create them.
```

Only create items after the user confirms. Use `./pos "new action: ..."`.

### Step 8: Publish to Confluence

After the local file is saved, publish the summary to Confluence so the team can reference it.

**Preview first - always:**

Before calling `createConfluencePage`, show the user in the terminal:
- The exact title of the page that will be created.
- The parent folder ID (and the month folder name).
- The full markdown body that will be sent.

Ask for explicit confirmation ("Publish to Confluence? Y/N"). Do not publish without it. The user has caught content-level issues at the Slack/Julie stage before; the Confluence page is the most permanent of the three outputs and should get the same preview treatment.

**Location:**
- MFM summaries live in monthly folders inside the `fdo` space (cloudId `0e31f281-3568-4559-ae88-153abcdead38`, spaceId `641548109`).
- Known month folder IDs:
  - June 2026: `906999057`
  - July 2026: `907097357`
- Each month is a Confluence folder (parentType `folder`, not a page). Folder creation is not supported by the MCP, so new month folders must be created manually by the user.

**Process:**
1. If the target month's folder ID is in the table above, use it.
2. If not, find the folder by searching for an existing summary in that month and reading its `parentId`. CQL example: `title ~ "MFM" AND title ~ "[Month] [Year]" AND title ~ "Summary"`. Use `getConfluencePage` on a hit to read `parentId` and `parentType` (must be `folder`).
3. If no summaries exist yet for the target month, ask the user to create the folder manually and supply its ID. Once supplied, add it to the table above.
4. Show the preview (title, parent folder ID, full body) and get explicit confirmation.
5. Create the page with `createConfluencePage` using `contentFormat: "markdown"`. Title format: `[Squad] MFM - [Month] [Year] - Summary` (sentence case, with the year).
6. Capture the returned page URL.

### Step 9: Update the Slack draft with the Confluence link

After the page is published, replace the `[link to be added]` placeholder in the Slack draft with the actual Confluence URL. Push the draft again to Slack (this overwrites the prior draft in the DM thread).

**Verify the draft actually landed.** `slack_send_message_draft` silent-fails when a draft already exists for the channel: it returns `result: "Draft message is created"` regardless. The authoritative signal is the presence of `draft_id` in the response.

- If `draft_id` is present: report the channel link to Chris.
- If `draft_id` is absent: tell Chris the existing draft is blocking the push, ask him to delete or send the old draft, then retry. Do not report success on the basis of the `result` string alone.

See `[[feedback_draft_never_send]]` for the global rule.

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
