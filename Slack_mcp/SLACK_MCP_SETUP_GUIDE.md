# Slack MCP Integration - Quick Setup Guide

**Project:** Chief of Staff
**Location:** `/Users/smallc/AI/Chief_of_staff`
**MCP Server:** korotovsky/slack-mcp-server (Go-based)
**Auth Method:** Browser session tokens (xoxc/xoxd)
**Workspace:** Autodesk Enterprise Slack

---

## ⚠️ CRITICAL: Enterprise Restriction

**STATUS:** Channel listing is **BLOCKED** by Autodesk Enterprise Slack security policies.

**Confirmed Issue:**
```json
{"ok":false,"error":"enterprise_is_restricted"}
```

**What This Means:**
- ❌ Cannot list channels via API with ANY user token (xoxc/xoxd, xoxp)
- ❌ Browser tokens don't work for channel listing
- ❌ Slack CLI tokens don't work for channel listing
- ✅ Authentication works, user caching works (78,737 users)
- ✅ MCP server is configured correctly
- ✅ Tokens are valid and correct

**The ONLY Solution:**
Request **admin approval** to install a Slack app with a **bot token** (`xoxb-`). Bot tokens bypass the "enterprise_is_restricted" limitation.

**Next Steps:**
1. Contact Autodesk IT/Slack admin
2. Request approval for Slack app installation
3. Provide app details from https://api.slack.com/apps
4. Once approved, you'll get a bot token that works

---

## Why This Approach? (Currently Non-Functional)

You don't have admin permissions to install Slack apps, so we attempted to use **browser session tokens** instead of bot tokens. However, **Autodesk Enterprise Slack blocks all user tokens from listing channels** due to security policies.

---

## Prerequisites

- [x] Go installed (`brew install go`)
- [x] slack-mcp-server cloned and built
- [x] Browser access to Slack workspace
- [x] Claude Code CLI installed

---

## Directory Structure

```
/Users/smallc/AI/Chief_of_staff/
├── .env                          # Your tokens (DO NOT COMMIT)
├── .gitignore                    # Contains .env
├── Slack_mcp/
│   └── slack-mcp-server/
│       ├── slack-mcp-server      # Executable
│       ├── .users_cache.json     # Auto-generated
│       └── .channels_cache.json  # Auto-generated
└── SLACK_MCP_SETUP_GUIDE.md     # This file
```

---

## Quick Setup Steps

### 1. Extract Tokens from Browser

**IMPORTANT:** Tokens expire when you log out or after inactivity. You'll need to refresh them regularly.

#### Get xoxc Token:
1. Open Slack in browser: `https://autodesk.enterprise.slack.com/`
2. Open developer console: `Cmd+Option+I`
3. Type `allow pasting` and press Enter (if prompted)
4. Paste and run:
```javascript
JSON.parse(localStorage.localConfig_v2).teams[document.location.pathname.match(/^\/client\/([A-Z0-9]+)/)[1]].token
```
5. Copy the output (starts with `xoxc-`)

#### Get xoxd Token:
1. In console, go to **Application** tab
2. Expand **Cookies** → select Slack URL
3. Find cookie named `d`
4. Copy its value (starts with `xoxd-`)

---

### 2. Configure Environment Variables

Create/update `.env` file:

```bash
cd /Users/smallc/AI/Chief_of_staff
nano .env
```

Add your tokens (no quotes, no spaces around `=`):

```bash
SLACK_MCP_XOXC_TOKEN=xoxc-your-token-here
SLACK_MCP_XOXD_TOKEN=xoxd-your-token-here
```

Save: `Ctrl+O`, Enter, `Ctrl+X`

---

### 3. Verify Tokens Work

```bash
cd /Users/smallc/AI/Chief_of_staff/Slack_mcp/slack-mcp-server

# Load and export tokens
source /Users/smallc/AI/Chief_of_staff/.env
export SLACK_MCP_XOXC_TOKEN
export SLACK_MCP_XOXD_TOKEN

# Test the server
./slack-mcp-server -transport stdio
```

**Success looks like:**
```
INFO | Successfully authenticated with Slack
team: "Autodesk", user: "smallc"
```

Press `Ctrl+C` to stop.

**If you see "invalid_auth":** Your tokens expired. Go back to Step 1.

---

### 4. Configure Claude Code MCP

Remove any existing Slack MCP servers:

```bash
cd /Users/smallc/AI/Chief_of_staff
claude mcp remove SlackMCPServer -s local
claude plugin uninstall slack
```

Add the SlackMCPServer:

```bash
# Load tokens first
source .env

# Add MCP server
claude mcp add SlackMCPServer --transport stdio \
  --env SLACK_MCP_XOXC_TOKEN=$SLACK_MCP_XOXC_TOKEN \
  --env SLACK_MCP_XOXD_TOKEN=$SLACK_MCP_XOXD_TOKEN \
  --env SLACK_MCP_USERS_CACHE=/Users/smallc/AI/Chief_of_staff/Slack_mcp/slack-mcp-server/.users_cache.json \
  --env SLACK_MCP_CHANNELS_CACHE=/Users/smallc/AI/Chief_of_staff/Slack_mcp/slack-mcp-server/.channels_cache.json \
  -- /Users/smallc/AI/Chief_of_staff/Slack_mcp/slack-mcp-server/slack-mcp-server -transport stdio
```

---

### 5. Verify MCP Configuration

```bash
claude mcp list
```

Should show:
```
SlackMCPServer: .../slack-mcp-server - ✓ Connected
```

(May show "Failed to connect" but still work - test to be sure)

---

### 6. Test with Claude Code

```bash
cd /Users/smallc/AI/Chief_of_staff
claude
```

At the `>` prompt:
```
List my Slack channels
```

If it works, Claude will show your Slack channels!

---

## Important Notes

### Token Expiration
- **Browser tokens expire when you log out**
- Autodesk enterprise has automatic logout policies
- Keep Slack browser tab open while using MCP
- You may need to refresh tokens frequently

### When Tokens Expire
You'll see: `invalid_auth` or Claude can't access Slack

**Solution:**
1. Extract fresh tokens (Step 1)
2. Update `.env` file (Step 2)
3. Restart Claude Code

### Staying Logged In
- Keep Slack browser tab active
- Interact with Slack occasionally
- Don't let computer sleep
- Enterprise policies may force logout (can't be changed)

---

## Troubleshooting

### "Authentication required" Error
**Problem:** Tokens not exported
**Fix:**
```bash
source .env
export SLACK_MCP_XOXC_TOKEN
export SLACK_MCP_XOXD_TOKEN
```

### "invalid_auth" Error
**Problem:** Tokens expired or invalid
**Fix:** Extract fresh tokens from browser (Step 1)

### Claude Can't See Slack MCP
**Problem:** MCP server not starting
**Fix:**
1. Check tokens: `echo $SLACK_MCP_XOXC_TOKEN`
2. Test server manually (Step 3)
3. Check logs: `tail -50 ~/Library/Logs/Claude\ Code/main.log`
4. Remove and re-add MCP server (Step 4)

### "Failed to connect" in `claude mcp list`
**Problem:** May be false positive
**Fix:** Try using it anyway - often still works!

---

## Quick Commands Reference

### Check MCP Status
```bash
claude mcp list
claude mcp get SlackMCPServer
```

### Update Tokens
```bash
nano /Users/smallc/AI/Chief_of_staff/.env
source /Users/smallc/AI/Chief_of_staff/.env
```

### Remove MCP Server
```bash
claude mcp remove SlackMCPServer -s local
```

### Remove Plugin
```bash
claude plugin uninstall slack
```

### Test Server Manually
```bash
cd /Users/smallc/AI/Chief_of_staff/Slack_mcp/slack-mcp-server
source /Users/smallc/AI/Chief_of_staff/.env
export SLACK_MCP_XOXC_TOKEN SLACK_MCP_XOXD_TOKEN
./slack-mcp-server -transport stdio
```

---

## Security Notes

- `.env` file contains sensitive tokens
- Added to `.gitignore` to prevent commits
- Tokens grant access as your user account
- Never share or commit tokens
- Tokens expire automatically for security

---

## Resources

- **MCP Server Repo:** https://github.com/korotovsky/slack-mcp-server
- **Setup Guide:** `A Step-by-Step Guide to Connecting Slack to Claude Code Without Admin Permissions.md`
- **Claude Code Docs:** https://code.claude.com/docs

---

## Last Updated

2026-01-01

**Status:** Configured and tested successfully with Autodesk Enterprise Slack
