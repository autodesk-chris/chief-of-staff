
# priv-forma-daily-digest

Purpose: Daily Slack digest for #priv-forma-design-leadership-fy27. Stores canonical prompt, runs, and metadata.

How to run:
1. Open `prompts/digest-prompt-v1.md` in ChatGPT (this project).
2. Run the prompt. If memory key `priv-forma-last_extracted_ts` exists it will be used; otherwise the assistant defaults to the last 24 hours.
3. The assistant will produce an executive summary in chat and output a .md block. Save as `runs/priv-forma-design-leadership-fy27-YYYY-MM-DD.md` and move to Obsidian.

Memory:
- Key: `priv-forma-last_extracted_ts`
- Stored value: ISO 8601 UTC timestamp of the most recent message extracted.
- To reset: run the assistant and ask it to forget `priv-forma-last_extracted_ts` or delete the key in chat.

Versioning:
- When you edit the prompt, create `digest-prompt-v2.md` and update this README changelog.

Security:
- Do not store credentials or private tokens in memory or in these files.

