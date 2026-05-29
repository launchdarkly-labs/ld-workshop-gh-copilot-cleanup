---
slug: configure-mcp-server
id: c55jrpjxnpcl
type: challenge
title: Configure the LaunchDarkly MCP Server
teaser: Add the LaunchDarkly MCP server configuration to your GitHub repository so
  GitHub Copilot can communicate with the LaunchDarkly API during coding agent sessions.
notes:
- type: text
  contents: "\U0001F4A1 The Model Context Protocol (MCP) is an open standard that
    allows AI models to securely connect to external tools and data sources. LaunchDarkly's
    MCP server is one of many integrations being built on top of this emerging standard."
tabs:
- id: rd4fixqustjg
  title: LaunchDarkly
  type: browser
  hostname: launchdarkly
- id: sqd2uwnxljlt
  title: Code Editor
  type: service
  hostname: workstation
  port: 8080
- id: holu7moyfbld
  title: GitHub
  type: browser
  hostname: github
- id: sjc64h9pkzva
  title: Coffee Shop App
  type: service
  hostname: workstation
  path: /
  port: 3000
- id: xqqhvfakydup
  title: Terminal
  type: terminal
  hostname: workstation
difficulty: ""
timelimit: 600
enhanced_loading: null
---
# Lab 2: Configure the LaunchDarkly MCP Server

GitHub Copilot communicates with LaunchDarkly through a Model Context Protocol (MCP) server. In this challenge, you'll wire that connection up in your Copilot settings.

First, sign in to GitHub using the credentials assigned to your session (you'll stay signed in for the remaining challenges):
**Username:** `[[ Instruqt-Var key="gh_user" hostname="workstation" ]]`
**Password:** `[[ Instruqt-Var key="gh_pass" hostname="workstation" ]]`
**2FA code:** `[[ Instruqt-Var key="gh_totp" hostname="workstation" ]]`

> The 2FA code rotates every 30 seconds. If the one above has expired by the time GitHub prompts you, open the **Terminal** tab and run `gh-totp` to print a fresh code.

In the GitHub tab, go to **Settings** → **Copilot** → **Cloud agent**.

In the MCP configuration section, add the following JSON — replacing the placeholder with the API token you generated in the previous challenge:

```javascript
{
  "mcpServers": {
    "LaunchDarkly": {
      "type": "local",
      "tools": ["*"],
      "command": "npx",
      "args": [
        "-y",
        "--package",
        "@launchdarkly/mcp-server",
        "--",
        "mcp",
        "start",
        "--api-key",
        "api-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
      ]
    }
  }
}
```

Click **Save MCP Configuration**.

**Security tip:** In production, rather than hardcoding your API key, store it as a repository secret prefixed with **COPILOT_MCP_** (e.g., **COPILOT_MCP_LD_API_KEY**) and reference it via an environment variable in the config.

Once the MCP server configuration is saved, click **Check** to continue.