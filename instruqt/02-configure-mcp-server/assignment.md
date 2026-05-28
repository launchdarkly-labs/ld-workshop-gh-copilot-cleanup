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

GitHub Copilot communicates with LaunchDarkly through a Model Context Protocol (MCP) server. In this challenge, you'll register that connection on your Copilot coding agent.

The configuration normally lives under **Settings → Copilot → Coding agent** in the GitHub UI. For this lab your workstation is already authenticated as the assigned pool user, so we'll save it from the terminal with a single command.

In the **Terminal** tab, run:

```bash
save-mcp-config <your-launchdarkly-api-token>
```

Replace `<your-launchdarkly-api-token>` with the token you copied at the end of Challenge 1 (it starts with `api-`). The helper builds this JSON and `PUT`s it to the GitHub Copilot MCP config endpoint on your behalf:

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
        "<your-launchdarkly-api-token>"
      ]
    }
  }
}
```

You can verify the entry was saved at any point with:

```bash
gh api /user/copilot/coding-agent/mcp-config
```

**Security tip:** In production, rather than embedding the API key in the config, store it as a repository secret prefixed with **COPILOT_MCP_** (e.g., **COPILOT_MCP_LD_API_KEY**) and reference it from the config via an environment variable.

Once the helper reports success, click **Check** to continue.