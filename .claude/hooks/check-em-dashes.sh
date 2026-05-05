#!/bin/bash
# Hook: Block Write and Edit operations that contain em dashes (— or –)
# This enforces the "no em dashes" rule from Global Claude Preferences.
# Em dashes are U+2014 (—) and en dashes are U+2013 (–).

# Read the tool input from stdin
input=$(cat)

# Extract the content being written/edited
# For Write tool: check "content" field
# For Edit tool: check "new_string" field
content=$(echo "$input" | jq -r '.tool_input.content // .tool_input.new_string // empty' 2>/dev/null)

# If no content found, allow the operation
if [ -z "$content" ]; then
  exit 0
fi

# Check for em dashes (—) and en dashes (–)
if echo "$content" | grep -qP '[\x{2014}\x{2013}]' 2>/dev/null || echo "$content" | grep -q '[—–]'; then
  echo "BLOCKED: Em dash (—) or en dash (–) detected in the content. Rewrite using regular hyphens (-) or restructure the sentence. This is enforced by the global style rule: no em dashes in output."
  exit 2
fi

exit 0
