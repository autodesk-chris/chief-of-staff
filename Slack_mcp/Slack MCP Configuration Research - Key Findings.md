# Slack MCP Configuration Research - Key Findings

## Overview
There are multiple approaches to connect Slack MCP with Claude Code, each with different token requirements and permission levels.

## Token Types and Authentication Methods

### 1. **Browser Session Tokens (Recommended for User Access)**
- **xoxc token**: Browser session token (starts with `xoxc-`)
- **xoxd token**: Slack browser cookie (starts with `xoxd-`)
- **Pros**: No admin permissions needed, works with user's existing access
- **Cons**: Requires extracting from browser console
- **Use case**: Reading messages, searching, analyzing conversations you can already access

### 2. **User OAuth Token (xoxp)**
- **Token format**: Starts with `xoxp-`
- **Pros**: More secure than browser tokens, standard OAuth flow
- **Cons**: Still requires workspace permissions to install app
- **Use case**: Alternative to browser tokens if available

### 3. **Bot Token (xoxb)**
- **Token format**: Starts with `xoxb-`
- **Pros**: Can be created without admin installation (if app already exists)
- **Cons**: Limited access (only invited channels, no search functionality)
- **Use case**: Limited read-only access to specific channels

### 4. **Configuration Token (Your Current Token)**
- **Token format**: `xoxe.xoxp-1-...`
- **Status**: This is an app-level configuration token
- **Limitation**: Not suitable for MCP server authentication directly
- **Action**: Use browser tokens instead (xoxc + xoxd)

## Your Situation Analysis

**Your Constraints:**
- ✅ Have Client ID, Client Secret, Signing Secret
- ✅ Have a configuration token (xoxe.xoxp-1-...)
- ❌ Cannot install bot to workspace (no admin permissions)
- ✅ Can access Slack web client

**Recommended Approach:**
Use **browser session tokens (xoxc + xoxd)** - this is the simplest path given your limitations.

## How to Extract Browser Tokens

### Getting xoxc Token:
1. Open Slack workspace in browser
2. Press `Ctrl+Shift+I` (or `F12`, or `Cmd+Option+I` on Mac)
3. Go to **Console** tab
4. Type: `allow pasting` and press Enter
5. Paste this code and press Enter:
   ```javascript
   JSON.parse(localStorage.localConfig_v2).teams[document.location.pathname.match(/^\/client\/([A-Z0-9]+)/)[1]].token
   ```
6. Copy the returned token (starts with `xoxc-`)

### Getting xoxd Token:
1. In Developer Tools, go to **Application** tab (or **Storage** in Firefox/Safari)
2. Click **Cookies** in the sidebar
3. Find cookie named `d`
4. Copy its value (starts with `xoxd-`)

## Configuration for Claude Code

### Option A: Using Speakeasy's slack-mcp-server (Recommended)

**Installation:**
```bash
mkdir slack-mcp-setup
cd slack-mcp-setup
git clone https://github.com/korotovsky/slack-mcp-server.git
cd slack-mcp-server
go build -o slack-mcp-server ./cmd/slack-mcp-server
```

**Claude Code Configuration (.mcp.json or via CLI):**
```json
{
  "mcpServers": {
    "slack": {
      "command": "PATH_TO_MCP_SERVER/slack-mcp-server",
      "args": ["-transport", "stdio"],
      "env": {
        "SLACK_MCP_XOXC_TOKEN": "your-xoxc-token-here",
        "SLACK_MCP_XOXD_TOKEN": "your-xoxd-token-here",
        "SLACK_MCP_USERS_CACHE": "PATH_TO_MCP_SERVER/.users_cache.json",
        "SLACK_MCP_CHANNELS_CACHE": "PATH_TO_MCP_SERVER/.channels_cache.json"
      }
    }
  }
}
```

**Or via CLI:**
```bash
claude mcp add --transport stdio slack --env SLACK_MCP_XOXC_TOKEN=your-xoxc-token --env SLACK_MCP_XOXD_TOKEN=your-xoxd-token -- /path/to/slack-mcp-server -transport stdio
```

### Option B: Using Composio's Setup Script

**Pros**: Fully automated, handles OAuth flow
**Cons**: Requires additional setup through Composio platform

**Steps:**
1. Go to https://mcp.composio.dev
2. Search for "Slack"
3. Copy the setup script from Claude tab
4. Paste and run in terminal within Claude Code config directory
5. Follow OAuth prompts

## Available Tools After Connection

Once connected, you can:
- Read messages from channels or threads
- Search messages by keyword
- List conversations and users
- Fetch user information
- Add reactions to messages
- Post messages (if enabled)
- Create reminders
- Schedule messages

## Your Colleague's Advice Explained

Your colleague mentioned "two temporary tokens" - they were referring to:
1. **xoxc token** (browser session token)
2. **xoxd token** (browser cookie)

These are "temporary" in the sense that they're tied to your browser session, but they work reliably for MCP server authentication.

## Next Steps for You

1. **Extract xoxc and xoxd tokens** from your Slack browser session
2. **Clone the slack-mcp-server** repository
3. **Build the server** locally
4. **Add to Claude Code** with the tokens in environment variables
5. **Restart Claude Code** and test connection
6. **Build your summarization agent** using the available MCP tools

## Important Notes

- These browser tokens are tied to your user account and permissions
- You can only access channels/messages you already have access to
- Tokens should be treated as sensitive credentials (like passwords)
- The MCP server runs locally, so tokens don't leave your machine
- If you need to revoke access, just delete the tokens from your configuration
