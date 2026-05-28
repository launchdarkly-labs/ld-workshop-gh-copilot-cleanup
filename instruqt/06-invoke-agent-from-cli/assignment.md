---
slug: invoke-agent-from-cli
id: 0ljb6azj5ago
type: challenge
title: Invoke the Agent from the Copilot CLI
teaser: Install the GitHub Copilot CLI and use it to trigger the LaunchDarkly agent
  directly from your terminal, running the same flag cleanup workflows without ever
  leaving your development environment.
notes:
- type: text
  contents: "\U0001F4A1 The Copilot CLI supports both interactive and non-interactive
    modes, making it easy to incorporate flag cleanup into scripts, CI pipelines,
    or your own internal developer tooling."
tabs:
- id: ublkvv7zagev
  title: LaunchDarkly
  type: browser
  hostname: launchdarkly
- id: k7k4yfdccc2d
  title: Code Editor
  type: service
  hostname: workstation
  port: 8080
- id: 0p2knpsudimi
  title: GitHub
  type: browser
  hostname: github
- id: xqtx7350qyg7
  title: Coffee Shop App
  type: service
  hostname: workstation
  path: /
  port: 3000
- id: 31szwejwod7u
  title: Terminal
  type: terminal
  hostname: workstation
difficulty: ""
timelimit: 600
enhanced_loading: null
---
# Lab 6: Invoke the Agent from the Copilot CLI

The Copilot UI is convenient, but the CLI lets you trigger flag cleanup workflows without leaving your terminal. In this final challenge, you'll install the GitHub Copilot CLI and use it to invoke the LaunchDarkly agent directly.

1. Install the GitHub Copilot CLI:
```bash
npm install -g @github/copilot
```
2. Authenticate the CLI with your GitHub account if prompted.
3. Invoke the LaunchDarkly agent directly with a prompt:
```bash
copilot --agent=launchdarkly --prompt "Remove the feature flag legacy-checkout-flow and update code to use the winning variant"
```
4. Alternatively, launch the CLI in interactive mode and use the slash command to select the agent:
```bash
copilot
/agent launchdarkly
```
5. Observe that the agent performs the same flag evaluation and cleanup workflow as in the UI — querying flag status, analyzing code usage, and creating a pull request.

Congratulations! You've completed the track. You now have a fully configured LaunchDarkly agent that lets you manage feature flag lifecycle using natural language — both from the GitHub UI and your terminal.

Once you've successfully run a CLI-triggered agent task, click **Check** to finish.