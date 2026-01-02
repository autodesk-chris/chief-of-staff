
# A Step-by-Step Guide to Connecting Slack to Claude Code Without Admin Permissions

This guide provides a comprehensive walkthrough for connecting your Slack workspace to Claude Code using the Model Context Protocol (MCP), even without administrative permissions to install Slack Apps. The approach outlined here, recommended for its simplicity and effectiveness in such scenarios, leverages your browser's session tokens to authenticate with the Slack API. This method grants your Claude Code agent the same level of access to your Slack workspace as your user account, enabling it to read messages, summarize conversations, and perform other actions within your existing permissions.

This document will cover the entire process, from extracting the necessary authentication tokens from your web browser to configuring the MCP server in your Claude Code environment. By following these steps, you will be able to build a powerful conversation summarization agent that can interact with your Slack data in real-time.

## Understanding the Authentication Method

The primary challenge you're facing is the lack of administrative permissions to install a Slack App in your workspace. This prevents the use of standard bot tokens (`xoxb-`) that require such installation. The solution, as advised by your colleague and confirmed by our research, is to use your browser's session tokens. This method effectively allows the MCP server to act on your behalf, with the same permissions and access as your own user account.

The two tokens we will be using are:

- **`xoxc` token**: A session token that authenticates you to Slack's internal API.
- **`xoxd` token**: A cookie that maintains your session with Slack.

By using these tokens, the `slack-mcp-server` can make requests to Slack as if it were your browser, bypassing the need for a formal app installation. This is a secure and effective method for personal use, as the tokens remain on your local machine and are not exposed to the internet.

## Step 1: Extracting Your Authentication Tokens

In this step, we will retrieve the `xoxc` and `xoxd` tokens from your browser session. These tokens are necessary for the MCP server to authenticate with your Slack workspace.

### Extracting the `xoxc` Token

1.  Open your Slack workspace in a web browser (e.g., Chrome, Firefox).
2.  Open the developer console. You can do this by pressing `Ctrl+Shift+I` on Windows/Linux or `Cmd+Option+I` on macOS.
3.  In the console, you may need to type `allow pasting` and press Enter to enable pasting commands.
4.  Paste the following JavaScript code into the console and press Enter:

    ```javascript
    JSON.parse(localStorage.localConfig_v2).teams[document.location.pathname.match(/^\/client\/([A-Z0-9]+)/)[1]].token
    ```

5.  The console will output your `xoxc` token. It will be a long string starting with `xoxc-`. Copy this token and save it in a secure location, such as a password manager or a local text file.

### Extracting the `xoxd` Token

1.  With the developer console still open, navigate to the **Application** tab (in Chrome) or the **Storage** tab (in Firefox).
2.  In the left-hand menu, expand the **Cookies** section and select your Slack workspace URL.
3.  In the table of cookies, find the cookie with the name `d`.
4.  Copy the value of the `d` cookie. This is your `xoxd` token, which will be a long string starting with `xoxd-`. Save this token securely along with your `xoxc` token.

## Step 2: Setting Up the `slack-mcp-server`

Now that you have your authentication tokens, the next step is to set up the `slack-mcp-server`. This open-source server will act as the bridge between Claude Code and your Slack workspace. We will clone the server's repository and build it from the source to ensure we have the latest version.

1.  Open a terminal or command prompt on your local machine.
2.  Create a new directory for your Slack MCP setup and navigate into it:

    ```bash
    mkdir slack-mcp-setup
    cd slack-mcp-setup
    ```

3.  Clone the `slack-mcp-server` repository from GitHub:

    ```bash
    git clone https://github.com/korotovsky/slack-mcp-server.git
    ```

4.  Navigate into the cloned repository's directory:

    ```bash
    cd slack-mcp-server
    ```

5.  Build the server using the Go compiler. If you don't have Go installed, you will need to install it first. You can find installation instructions at the official Go website: [https://golang.org/doc/install](https://golang.org/doc/install)

    ```bash
    go build -o slack-mcp-server ./cmd/slack-mcp-server
    ```

After the build process is complete, you will have an executable file named `slack-mcp-server` in the current directory. This is the server that Claude Code will run.

## Step 3: Configuring Claude Code

With the `slack-mcp-server` built and your authentication tokens ready, the final step is to configure Claude Code to use the server. This is done by editing Claude Code's configuration file to add the `slack-mcp-server` as a local stdio server.

1.  Open Claude Code.
2.  Navigate to **Settings > Developer > Edit Config**.
3.  This will open the `claude_desktop_config.json` file in your default text editor.
4.  Add the following JSON object to the `mcpServers` section of the file. If the `mcpServers` section does not exist, you can create it.

    ```json
    {
      "mcpServers": {
        "SlackMCPServer": {
          "command": "/path/to/your/slack-mcp-setup/slack-mcp-server/slack-mcp-server",
          "args": ["-transport", "stdio"],
          "env": {
            "SLACK_MCP_XOXC_TOKEN": "YOUR_XOXC_TOKEN",
            "SLACK_MCP_XOXD_TOKEN": "YOUR_XOXD_TOKEN",
            "SLACK_MCP_USERS_CACHE": "/path/to/your/slack-mcp-setup/slack-mcp-server/.users_cache.json",
            "SLACK_MCP_CHANNELS_CACHE": "/path/to/your/slack-mcp-setup/slack-mcp-server/.channels_cache.json"
          }
        }
      }
    }
    ```

5.  **Important:** You need to replace the placeholder values in the JSON configuration:
    -   `"/path/to/your/slack-mcp-setup/slack-mcp-server/slack-mcp-server"`: Replace this with the absolute path to the `slack-mcp-server` executable you built in the previous step.
    -   `"YOUR_XOXC_TOKEN"`: Replace this with the `xoxc` token you extracted.
    -   `"YOUR_XOXD_TOKEN"`: Replace this with the `xoxd` token you extracted.
    -   `"/path/to/your/slack-mcp-setup/slack-mcp-server/.users_cache.json"` and `"/path/to/your/slack-mcp-setup/slack-mcp-server/.channels_cache.json"`: Replace these with the absolute paths to the cache files within your `slack-mcp-server` directory.

6.  Save the `claude_desktop_config.json` file.
7.  Restart Claude Code for the changes to take effect.

After restarting, Claude Code will automatically start the `slack-mcp-server` in the background and connect to it. You can verify the connection by opening a new chat in Claude Code and typing `/mcp` to see the list of connected MCP servers. You should see `SlackMCPServer` in the list.

## Step 4: Testing the Connection

To verify that the Slack MCP server is properly connected to Claude Code:

1.  Open Claude Code and start a new chat.
2.  Type `/mcp` and press Enter. This command will display all connected MCP servers.
3.  You should see `SlackMCPServer` listed in the output.
4.  Try a simple command to test the connection, such as asking Claude to list the channels in your Slack workspace:

    ```
    List all the channels in my Slack workspace.
    ```

If Claude Code successfully retrieves a list of channels, your Slack MCP server is properly configured and connected.

## Troubleshooting Common Issues

### Issue: "Failed to connect" Error

**Possible Causes:**
- The path to the `slack-mcp-server` executable is incorrect.
- The `xoxc` or `xoxd` tokens are invalid or expired.
- The Go build process failed or the executable was not created.

**Solutions:**
1. Double-check the absolute path to the `slack-mcp-server` executable in your configuration file.
2. Verify that your tokens are correct by extracting them again from your browser.
3. Try rebuilding the server: `go build -o slack-mcp-server ./cmd/slack-mcp-server`
4. Check the Claude Code logs for more detailed error messages. On macOS, logs are typically found at `~/Library/Logs/Claude Code/`. On Windows, check `%LocalAppData%/Claude Code/logs/`.

### Issue: Tokens Are Expired

Slack browser tokens can expire after extended periods of inactivity. If you encounter authentication errors:

1. Extract new `xoxc` and `xoxd` tokens from your browser following the steps in **Step 1**.
2. Update the tokens in your `claude_desktop_config.json` file.
3. Restart Claude Code.

### Issue: Limited Access to Channels

If Claude Code can only access certain channels and not others:

1. Verify that your user account has access to those channels in Slack.
2. The MCP server will only allow access to channels that your user account can access.
3. If you need access to additional channels, request access from the channel owner or workspace administrator.

## Additional Resources

For more information about the Slack MCP server and its capabilities, refer to the following resources:

- **GitHub Repository**: [https://github.com/korotovsky/slack-mcp-server](https://github.com/korotovsky/slack-mcp-server)
- **Claude Code Documentation**: [https://code.claude.com/docs/en/mcp](https://code.claude.com/docs/en/mcp)
- **Model Context Protocol (MCP) Overview**: [https://www.anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol)

## Next Steps

Once your Slack MCP server is successfully connected to Claude Code, you can start building your conversation summarization agent. Refer to the **Slack Conversation Summarization Agent** document for detailed instructions on creating and using the agent.
