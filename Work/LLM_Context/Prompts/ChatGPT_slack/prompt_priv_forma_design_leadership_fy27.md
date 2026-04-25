---
title: "digest-prompt-v1.1-manual"
type: "prompt"
version: "v1.1"
date: 2026-02-XX
author: "Chris Small"
tags: ["priv-forma","digest","slack","manual","obsidian"]
summary: "Manual-mode daily digest prompt for #priv-forma-design-leadership-fy27. Replace LAST_EXTRACTED_TS before running. Does NOT write memory; user must copy new last_extracted_ts from generated .md into the next run."
---

LAST_EXTRACTED_TS: **INSERT VALUE**

Consent: I will manually provide LAST_EXTRACTED_TS each run. Do NOT call any persistent memory APIs (bio.update) or store memory. Do NOT store Slack tokens, SharePoint links, or credentials. You may write the new last_extracted_ts into the Markdown frontmatter only (I will copy it into the next run).

Task:  
Summarize Slack channel #priv-forma-design-leadership-fy27 for messages strictly AFTER LAST_EXTRACTED_TS.

A valid timestamp is REQUIRED. If LAST_EXTRACTED_TS is empty or cannot be parsed, print exactly:

Error: LAST_EXTRACTED_TS missing or invalid — a valid timestamp is required. To extract the last 24 hours, provide an ISO 8601 UTC timestamp equal to (now - 24 hours).

Then STOP (do not call connectors or summarize anything).

────────────────────────────────────────  
TIMESTAMP PARSING RULES  
────────────────────────────────────────

Accept the following formats and convert to UTC ISO 8601 with trailing Z:

• ISO 8601 with trailing Z — use as-is.  
• Slack p-format (e.g., p1771003185614289) — remove leading "p", insert a dot before the last 6 digits, interpret as seconds.fraction, convert to ISO 8601 Z.  
• Slack numeric ts (seconds.fraction) — convert to ISO 8601 Z.  
• Plain date YYYY-MM-DD — interpret as YYYY-MM-DDT00:00:00Z.

If parsing fails → print the exact error above and abort.

────────────────────────────────────────  
CONNECTOR-BASED DISCOVERY → FETCH → VALIDATE ALGORITHM (MUST BE FOLLOWED)  
────────────────────────────────────────

Use the ChatGPT connector’s Slack methods (do NOT attempt raw HTTP calls). The connector method names below are examples — if your environment exposes different method names, use their equivalents (e.g., `connector.search`, `connector.fetch_thread`, `connector.fetch_message`, `connector.fetch_replies`). Follow this algorithm exactly.

**Preflight test for optional fast-path (required):**  
• Before processing all threads, run a single preflight test to check whether the connector’s `fetch_thread` operation reliably returns root + replies: call `connector.fetch_thread(channel_id, sample_thread_key)` for one known thread_key (a recent example or a supplied sample).  
• If `connector.fetch_thread` returns the root + replies with `ts == sample_thread_key` and expected metadata, mark `fast_path_ok = true`. If it errors, returns partial data, or root is missing, mark `fast_path_ok = false` and do not use the fast-path except for an optional subsequent attempt per-thread (see below). Log preflight result in debug.

1. Discovery (search post-cutoff messages first)  
    • Call the connector search operation to find **all messages** in the channel with timestamp strictly greater than LAST_EXTRACTED_TS. Example call semantics: `connector.search("in:#priv-forma-design-leadership-fy27 after:LAST_EXTRACTED_TS")`. Collect metadata (message ts, thread_ts, author, short text snippet). Gather a sufficiently large top-N (suggest 500) to cover the interval. Include both root messages and replies.
    
2. Derive thread keys  
    • For every returned message compute `thread_key` as: `thread_key = message.thread_ts if present else message.ts`.  
    • Build `unique_thread_keys = unique(thread_key values)`.
    
3. Fetch full threads (PRIMARY: root-first + replies; OPTIONAL fast-path)  
    **PRIMARY root-first (MANDATORY):** For each `thread_key` in `unique_thread_keys`, do the following:
    

a. **Fetch root explicitly:** Call `connector.fetch_message(channel_id, thread_key)` to fetch the root message.  
• If this returns 404 or a permission error, record `Note: root message for thread <thread_key> missing (deleted or permission issue)` and continue to fetch replies if possible.

b. **Fetch replies:** Call `connector.fetch_replies(channel_id, thread_key)` to fetch replies.  
• If `connector.fetch_replies` is unavailable, call `connector.search("in:#priv-forma-design-leadership-fy27 thread_ts:thread_key")` to collect replies.  
• If the connector paginates replies, fetch all pages until exhaustion. Sort messages by `ts` ascending for consistent context.

c. **Assemble & verify:** Assemble `[root + replies]`. Confirm that a message with `ts == thread_key` is present; if not present but the explicit root fetch returned a valid root, prepend it. If root is missing and cannot be fetched, mark `root_missing=true` and surface that in the final output.

d. **Retries & backoff:** Attempt the full-thread assembly up to **3 total attempts** (initial + 2 retries) with exponential backoff + jitter. Respect any `Retry-After` returned by the connector. Suggested delays: 1s ± jitter, 2s ± jitter (or 1s, 2s, 4s with jitter).

e. **Concurrency:** Cap concurrent thread fetches (recommended 5–10 parallel) to reduce risk of rate limiting.

f. **Error surfacing:** If assembly fails after retries, record `Fetch error for thread <thread_key>: <error summary>` and include that line in the digest; do not silently omit the thread.

**OPTIONAL fast-path (only if fast_path_ok is true):**  
• If the preflight test marked `fast_path_ok = true`, you may call `connector.fetch_thread(channel_id, thread_key)` as an optimization. However, **always perform a root presence check** (verify a message with `ts == thread_key` is present). If the fast-path response is partial or root is missing, immediately fall back to the PRIMARY root-first flow for that thread. Log per-thread which path was used in the debug block.

4. Summarize full threads  
    • For each assembled thread (root + replies), summarize the **entire thread**. Synthesize a concise 2–6 word title (do not use literal root text). Summaries must reflect the full thread context — not just post-cutoff replies.
    
5. Order & limit  
    • Determine the timestamp of the most recent message **in each assembled thread** and order threads by that newest-message timestamp descending.  
    • Include up to **12** threads. If more than 12 match, include the 12 most recent and append: “…and X more new threads (not shown) — rerun if you want full list.”
    
6. last_extracted_ts behavior  
    • Set `last_extracted_ts` in frontmatter to **(latest processed message timestamp + 1 second)** in UTC ISO 8601 Z.
    

────────────────────────────────────────  
VALIDATION (MANDATORY)  
────────────────────────────────────────

After assembling the draft digest but before returning it, perform this validation:

1. Re-run the connector search: `connector.search("in:#priv-forma-design-leadership-fy27 after:LAST_EXTRACTED_TS")` and collect metadata (ts, thread_ts). Call these `validation_results`.
    
2. For every message in `validation_results` compute `thread_key` and confirm that `thread_key` is present among `unique_thread_keys` used to assemble threads.
    
3. If any `thread_key` is missing, fetch the missing thread(s) immediately (one retry allowed using the primary root-first method), incorporate them, and **re-run validation once**.
    
4. If after the retry any validation messages remain missing, append this visible warning at the top of the chat output:  
    `Validation warning: N messages after LAST_EXTRACTED_TS were not included — manual review required.`
    

Include a concise debug block (visible to the user) showing: LAST_EXTRACTED_TS used, number of messages returned by the validation search, number of unique thread_keys discovered from that search, number of threads fetched and included, the most recent processed message timestamp, and for each thread a `root_found: true|false` and `path_used: primary_root_first|fast_path` entry and any fetch errors.

────────────────────────────────────────  
ERROR HANDLING & EDGE CASES  
────────────────────────────────────────

• If a thread fetch fails after retries, include `Fetch error for thread <thread_key>: <error>` in the digest.  
• If the thread root is deleted or inaccessible, include `Note: root message for thread <thread_key> missing (deleted or permission issue). Summary based on replies only.`  
• If threads are extremely long or paginated, use chunked summarization: summarize chunks then synthesize chunk summaries into a final thread summary, and note chunking in the debug block.  
• Include all messages that share identical timestamps.  
• Do NOT store any user credentials or secrets.  
• If the connector’s method names differ, use equivalent connector operations and document the method names used in the debug block.

────────────────────────────────────────  
OUTPUT FORMAT — PRODUCE A THEN B (SINGLE PLAIN-TEXT MESSAGE ONLY)  
────────────────────────────────────────

**Important: Your entire response must be a single plain-text message. Do NOT use code blocks, do NOT split into multiple messages, and do NOT use Markdown code fences.** The response must contain A then B in order, exactly as described.

A — Executive Summary (chat output FIRST)

• The FIRST line of your reply must be exactly:  
Daily briefing (short):

• Then, for each qualifying thread (max 12 by recency), include this exact block, separated by a blank line (no code fences):

• Separate each thread block with a blank line.  
• Do NOT prefix titles with Slack mentions.  
• Title must be synthesized (not raw root text).  
• Decisions for Chris must be derived ONLY from messages strictly after LAST_EXTRACTED_TS.  
• If >12 threads, append: “…and X more new threads (not shown) — rerun if you want full list.”

B — Obsidian Markdown Digest

Immediately after the executive summary (still in the same single plain-text message), include:

---

## channel: priv-forma-design-leadership-fy27  
last_extracted_ts: <NEW_ISO_8601_UTC_Z>  
generated_at: <CURRENT_ISO_8601_UTC_Z>

# Slack Digest — priv-forma-design-leadership-fy27

For each included thread, use exactly this structure (repeat for each thread, still in the same single message):

---

Title:

Poster:

Summary:  
• Bullet 1 — key theme or issue introduced  
• Bullet 2 — important development or context  
• Bullet 3 — notable perspectives or tensions  
• Bullet 4 — implications or decisions discussed  
• Bullet 5 — progress or status update  
• Bullet 6–10 — additional important context (if needed)

Action for Chris:  
• Explicit action derived ONLY from post-cutoff messages or "No action"

Suggested next step:  
• Clear recommended next step Chris may consider strategically

Mentions:  
• List all direct mentions of <@U082ASVFE9Y> after the cutoff or "None"

Link:  
• Slack permalink to the root post

---

At the end of the digest (still within the same single message), include the debug block (visible to the user):

Debug: LAST_EXTRACTED_TS used: <...>; #validation messages: <...>; #unique thread_keys discovered: <...>; #threads fetched and included: <...>; most recent processed message timestamp: <...>. Per-thread: list `thread_key`, `root_found: true|false`, `path_used: primary_root_first|fast_path`, pages_fetched: , and any `fetch_errors: <error_summary>`.

────────────────────────────────────────  
SPECIAL RULES & FINAL CHECKS  
────────────────────────────────────────

• Actions, blockers, or decisions for Chris (<@U082ASVFE9Y>) MUST be derived ONLY from messages strictly after LAST_EXTRACTED_TS. Do not surface pre-cutoff items as current actions unless reiterated post-cutoff.  
• If a thread root was deleted or inaccessible, still synthesize a title from replies. Mark the root missing visibly.  
• If the prompt rules are unclear, **fetch more context** rather than summarizing from partial data.  
• The assistant must not call raw HTTP APIs; use connector methods only. If the connector’s method names differ, use equivalent connector operations and document the method names used in the debug block.  
• The entire assistant response must be one single plain-text message and must begin with the line: Daily briefing (short): — no exceptions.




