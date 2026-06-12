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
- id: holu7moyfbld
  title: GitHub
  type: browser
  hostname: github
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

First, click on the [GitHub](#tab-1) tab, sign in to GitHub using the credentials assigned to your session (you'll stay signed in for the remaining challenges):

**Username:**
```text
[[ Instruqt-Var key="gh_user" hostname="workstation" ]]
```
**Password:**
```text
[[ Instruqt-Var key="gh_pass" hostname="workstation" ]]
```
**2FA code:**
```text
[[ Instruqt-Var key="gh_totp" hostname="workstation" ]]
```

> The 2FA code rotates every 30 seconds. If the one above has expired by the time GitHub prompts you, open the [Terminal](#tab2) tab and run `gh-totp` to print a fresh code.

Next, we need to clone a repo which we can work with.

1. In the GitHub tab, click on the **ld-sample-app-python** repository.
2. At the upper-right of the repo, click **Fork**, then **Create fork**.
3. Go to **Settings** → **Copilot** → **Cloud agent**.
4. In the MCP configuration section, add the following JSON — replacing the placeholder with the API token you generated in the previous challenge:
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
5. Click **Save MCP configuration**.

**Security tip:** In production, rather than hardcoding your API key, store it as a repository secret prefixed with **COPILOT_MCP_** (e.g., **COPILOT_MCP_LD_API_KEY**) and reference it via an environment variable in the config.

Once the MCP server configuration is saved, click **Check** to continue.