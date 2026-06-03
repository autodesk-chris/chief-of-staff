---
name: email-triage
description: Triage unread inbox into priority tiers (VIP, Important, CC, Noise) and route low-priority emails into dedicated folders. Surfaces action-required items into a dedicated folder so the rest of the inbox stays scannable. Uses people.md as the source of truth for inner-circle senders, treats names in the Leadership section of people.md as VIPs (currently Carl Christensen, Amy Bunszel, Patrick Aragon, Julie Sylvain, Andrew Anagnost), reads Concur/Gamma/Egencia/Workday/Help_Wolken emails for approval, action, or receipt signals, and surfaces ambiguous senders for direction. Supports an auto mode for scheduled (cron) runs that skips the move confirmation. Use when "triage inbox", "triage email", "process inbox", "clean inbox", "email triage", or with "auto" suffix for unattended runs. NOT for sending or drafting email (use m365 tools directly).
---

# Email triage

Classify unread inbox into priority tiers, surface what matters, route low-priority mail and action-required items into folders.

## Sources

- **People directory:** `Work/LLM_Context/Contacts/people.md`. Source of truth for Tier 2 names. Re-read every run; do not hardcode.
- **State file:** `Work/.state/email_triage.json`. Last-run timestamp.
- **Outlook folders (must already exist as child folders of Inbox):**
  - `Inbox/VIP` (Tier 1 emails, unless Action Required override applies)
  - `Inbox/Action required` (Tier 1 or 2 items where action is required)
  - `Inbox/Triage-cc`
  - `Inbox/Triage - noise`
  - `Inbox/Triage - receipts and travel`
  - `Inbox/Triage - learning`

## Subject-based universal overrides

These rules apply **before** the tier model and override sender-based routing. A VIP email matching one of these still gets the override destination.

### Force to noise (even from VIP/priority senders)

Match by subject:
- Begins with `Accepted:`, `Declined:`, `Tentative:`, `Canceled:`, or `Cancelled:` (meeting response confirmations)

Meeting acceptances are pure clutter regardless of sender. Move to `Triage - noise`.

### Force to stay in inbox (override VIP routing)

Match by subject:
- Contains "Pedaling into the weekend" (recurring informal email from Amy that should be visible in inbox, not buried in VIP folder)

Add more entries here as recurring informal/weekly emails from VIPs are identified.

## Tier model

| Tier | Definition | Default destination |
|---|---|---|
| 1 (VIP) | All names in `## Leadership` section of people.md (excluding Chris Small); Julie Sylvain demoted to Tier 2 unless in To: field | `VIP` folder (unless Action Required override applies) |
| 2 (Important) | (a) Sender in people.md, OR (b) you are in To: field (direct), OR (c) Concur with approval/action signal, OR (d) Julie Sylvain when CC'd | Stay in inbox (unless Action Required override applies) |
| 4 (CC-only) | You are in CC, sender not in people.md, not a noise pattern | `Triage-cc` after confirmation |
| 5 (Noise) | Matches a noise pattern (see below) | `Triage - noise` after confirmation |

### Special-case senders

- **Patrick Aragon** (Amy's Chief of Staff): always Tier 1. He speaks for Amy.
- **Julie Sylvain** (Carl's Chief of Staff): Tier 1 if directly addressed (in To:), else Tier 2.

## Action Required override

Any Tier 1 or Tier 2 email where action is required is routed to `Action required` folder instead of staying in inbox. This lets the user differentiate action items from FYI mail at a glance until the inbox is cleaned up.

**Order of evaluation**: sender-specific rules (Concur, Workday, Gamma, Egencia, Learning) are checked FIRST. Generic action signals only apply when no sender-specific rule matched. This prevents recurring-nag senders (like Concur charge-submission reminders) from leaking into Action Required because their subject line contains "ACTION REQUIRED".

**Generic action signals** (applied only when no sender-specific rule matched):
- Subject contains "ACTION REQUIRED" (case-insensitive)
- Body contains: "requires your approval", "pending your approval", "action required", "approve" + button/link, "submitted for your approval", "needs your decision", "please review by", "respond by", "your input needed"

**Sender-specific routing to Action Required**:
- Concur (`*@concursolutions.com`) with approval signal (NOT charge-submission reminders, see Concur rule)
- Workday (`*@myworkday.com`) with "ACTION REQUIRED" in subject (see Workday rule)
- Confluence / SharePoint / Office notifications with a direct @mention or action signal in body (see Collaboration platforms rule)

Tier 4 and Tier 5 emails are NOT routed to Action Required even if they contain these phrases. Folder destinations for those tiers take priority for cleanup.

## Auto mode (unattended runs)

When the trigger phrase includes "auto" (e.g. "triage inbox auto", "auto triage", "email triage auto") or the skill is invoked from a scheduled job, the skill runs without confirmation prompts:

- Still presents the full digest in chat (for audit log / on-screen review)
- Moves VIP, Tier 4, Tier 5, Receipts, Learning, and Action Required emails immediately without asking "proceed with moves?"
- Items in "Where to file?" section stay in inbox and are surfaced in the digest. They are NEVER auto-moved.
- State file updates as normal after the run

Auto mode is intended for scheduled runs (e.g. 6am cron) when no one is available to confirm. For interactive use, prefer the standard mode with the digest + confirmation step.

## Body-read rules

For these senders, call `read_email` to inspect body or recipients before classifying.

### Concur (any `*@concursolutions.com` sender)

Covers `AutoNotification@concursolutions.com`, `EmailReminderService@concursolutions.com`, and any other concursolutions.com sender.

**Balances Due exception (always Action Required)**: Concur emails with subject containing "Balances Due to Autodesk" OR "Immediate Action Required: Balances" route to **`Action required`** regardless of other rules. These are real outstanding payment obligations, not recurring nags.

**Always-Noise exclusion**: Concur reminders about submitting *your own* charges go to `Triage - noise` even if the subject contains "ACTION REQUIRED". These are recurring nags, not real action items. Match on either:
- Sender = `EmailReminderService@concursolutions.com` AND subject does NOT contain "Balances Due", OR
- Subject or body contains "charges" combined with "submit" / "to be submitted" / "need to submit" / "need to be submitted" AND does NOT contain "Balances Due"

**Otherwise**, check body or subject for **approval signals** (someone else needs your approval):
- "requires your approval"
- "pending your approval"
- "submitted for your approval"
- "approve" + button/link (asking you to approve)
- "you are the next approver"

Result:
- Approval signal found: route to **`Action required`** (Tier 2)
- Not found: route to **`Triage - noise`**

### Gamma and Egencia

Check body for **receipt signals**:
- "receipt"
- "invoice"
- "payment confirmation"
- "your transaction"
- "thank you for your payment"
- currency + amount pattern (e.g. $123.45, EUR 50.00, GBP 30, kr 500)

Result:
- Signal found: route to **`Triage - receipts and travel`**
- Not found: **surface in "Where to file?" section**. Do not auto-move.

### Any sender: payment confirmation in subject

If the subject contains "payment confirmation", "payment received", "your receipt", "your invoice", or "order confirmation", route to **`Triage - receipts and travel`** regardless of sender (no body read needed).

### Workday (`*@myworkday.com`)

Check subject for "ACTION REQUIRED" (case-insensitive):
- Present: route to **`Action required`** (Tier 2)
- Absent: route to **`Triage - noise`** (kudos, surveys, training reminders, FYI alerts)

### Help_Wolken / Autodesk help desk (`Help_*@autodesk.com`)

Covers `Help_SN_PRD@autodesk.com` and any `Help_*@autodesk.com` sender (Autodesk internal help/ticket system).

Always **read the body** to check for approval requests or pending actions. Look for:
- "approval required" / "requires your approval" / "pending your approval"
- "action required" / "your action is needed"
- "nomination" + "awaiting"
- "please approve" / "approve this request"
- Subject containing "Awaiting Your Approval"

Result:
- Approval/action signal found: route to **`Action required`** (Tier 2)
- Not found: **stay in inbox** (do NOT route to noise; user wants visibility on help desk tickets)

### Collaboration platforms (Confluence, SharePoint, Office docs, OneDrive)

Notifications from collaboration tools often surface real action items (a direct @mention asking for input on a doc, page, or sheet). Always read the body before classifying.

**Senders covered**:
- Confluence: `confluence@atlassian.autodesk.com`
- SharePoint / OneDrive: `no-reply@sharepointonline.com`, `*@sharepointonline.com`
- Microsoft Office notifications: `no-reply@notify.microsoft.com`, `*@notify.microsoft.com`, `office365-comments@notify.microsoft.com`
- Microsoft Forms / Lists / Planner: any `*.notify.microsoft.com` sub-domain

Check body or subject for **direct mention / action signals**:
- "@Chris Small" or "@chris.small" (direct @ mention)
- "mentioned you" / "you were mentioned" / "@mentions"
- "assigned to you" / "task assigned"
- "needs your input" / "your input needed"
- "comment for you" / "left a comment for you"
- "please review" / "review by"
- "approve this page" / "approval request"
- "respond to" (in the context of a comment or mention)

Result:
- Signal found: route to **`Action required`** (Tier 2)
- Not found: route to **`Triage - noise`** (generic page-edit alerts, watcher digests, FYI activity)

## Learning folder rule

Sender domain or name contains "Autodesk Learning Central" (or `learningcentral` in the address) goes to **`Triage - learning`**. No body check.

## Noise patterns (Tier 5)

Match by sender or subject:
- Confluence without @mention or action signal: `confluence@atlassian.autodesk.com` (after body check, see Collaboration platforms rule)
- SharePoint / Office notifications without action signal: `*@sharepointonline.com`, `*@notify.microsoft.com` (after body check)
- Concur without approval/action signal: any `*@concursolutions.com` sender (after body check)
- Workday without ACTION REQUIRED in subject: `*@myworkday.com` (after subject check)
- Jira: senders containing `@*.atlassian.net` or Jira automation
- Calendar confirmations: subject begins `Accepted:`, `Declined:`, `Tentative:`
- Slack digests: `noreply@slack.com`, subjects "Daily summary" / "What you missed"
- Recruitment platform alerts: SmartRecruiters, Greenhouse, LinkedIn Recruiter
- Marketing / mass mail: `List-Unsubscribe` header present, sender not in people.md
- Generic automated sender prefixes: `info@*`, `support@*`, `notifications@*`, `notification@*`, `noreply@*`, `no-reply@*`, `donotreply@*`. Excludes Help_Wolken (`Help_*@autodesk.com`), which has its own rule above and stays in inbox.
- Miro updates: `daily@updates.miro.com`, `*@updates.miro.com`, `The Miro Team`
- Conference registration / event marketing: subject contains "registration is open", "register now", "ITF 2026", "tuesday tidbits", "register today", "save your seat", "join us at" (combined with sender NOT in people.md). If uncertain, leave in inbox rather than auto-move.

## Uncertainty rule

If a sender doesn't match a known pattern, or a body check is inconclusive, **surface the email in the "Where to file?" section and wait for direction**. Never guess. If the user gives a routing answer for a recurring sender, offer to add a rule to this SKILL.md at end of session.

## Workflow

1. **Load state**: read last-run timestamp from `Work/.state/email_triage.json`. Default to 24h ago if missing or empty.
2. **Resolve folder IDs**: call `list_child_folders` with `parentFolderId = inbox` to get IDs for `VIP`, `Action required`, `Triage-cc`, `Triage - noise`, `Triage - receipts and travel`, `Triage - learning`. If any are missing, stop and ask the user to create them as sub-folders of Inbox.
3. **Pull unread**: `list_emails` with `after = last_run`, `unreadOnly = true`, `top = 100`. Paginate if more.
4. **Parse people directory**: extract names from all squad tables (User Engagement, First Strike, Strategic Accounts, Marketing), External contacts, Autodesk stakeholders, and Leadership sections of `people.md`. Build the VIP set from `## Leadership` (excluding Chris Small); build the Tier 2 set from the other sections.
5. **First-pass classify** each email by sender / recipient rules.
6. **Body reads**: for Concur, Gamma, Egencia, Workday, Confluence, SharePoint, and Microsoft Office notification senders, call `read_email` and apply body / subject checks.
7. **Apply Action Required override** for Tier 1 and Tier 2 emails with action signals.
8. **Present digest** grouped by section (see output format).
9. **Confirm before moving** (skipped in auto mode): ask "move VIP, Action required, Tier 4, Tier 5, Receipts, Learning now? (y / n / specify keeps)". In auto mode, present the digest then proceed directly to moves without asking.
10. **Move emails** using `update_email` with `moveToFolder` set to the target folder ID.
11. **Update state**: save current UTC timestamp to `Work/.state/email_triage.json` (only after a successful run).

## Output format

```
# Inbox triage - {ISO timestamp}
Unread since: {last-run timestamp}
Total processed: {n}

## Tier 1 (VIP) - {n}
- **Carl Christensen**: {subject} ({direct|cc}, {time})
  - {1-line summary}
  - Action required: yes/no
  - Suggested: Do | Defer | Delegate | Drop

## Tier 2 (Important) - {n}
- **{Sender} ({squad/role if known from people.md})**: {subject} ({direct|cc})
  - {1-line summary}
  - Action required: yes/no
  - Suggested: {action}

## Where to file? - {n} (needs your direction)
- **{Sender}**: {subject}
  - {1-line summary}
  - Suggest: Action required | Receipts | Noise | Keep in inbox?

## To move ({total n})
- To `VIP` ({n}): {sender}: {subject}, ...
- To `Action required` ({n}): {sender}: {subject}, ...
- To `Triage-cc` ({n}): {sender}: {subject} (x{count}), ...
- To `Triage - noise` ({n}): Confluence: {n} | Concur (no action): {n} | Workday (no action): {n} | Slack digest: {n} | ...
- To `Triage - receipts and travel` ({n}): Gamma: {n}, Egencia: {n}
- To `Triage - learning` ({n}): Autodesk Learning Central: {n}

Proceed with moves? (y / n / specify keeps)
```

## Action language (Four D's)

For Tier 1-2 items, suggest one of:
- **Do**: quick reply (<2 min) or single decision
- **Defer**: needs focus block; capture as task if not already tracked
- **Delegate**: flag suggested owner (often from people.md)
- **Drop**: safe to archive

## Safety rules

- Never auto-move Tier 2 emails except into `Action required` (per the override rule). Tier 1 emails route to `VIP` (or to `Action required` if the override applies).
- If a Tier 4/5 candidate looks important on closer look (customer name, contract keyword, legal/PR/security/breach mention), bump to Tier 2 and flag for attention.
- Always present the digest and confirm before moving.
- Update the state timestamp only after a successful run, never on partial failure.
- For unfamiliar receipt-platform senders, surface with "Where to file?". Don't assume.
