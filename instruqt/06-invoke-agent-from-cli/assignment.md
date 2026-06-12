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
- id: cvqhyjqbtujy
  title: LaunchDarkly
  type: browser
  hostname: launchdarkly
- id: adke6bagyhem
  title: GitHub
  type: browser
  hostname: github
- id: zo3fakbkzygb
  title: Terminal
  type: terminal
  hostname: workstation
difficulty: ""
timelimit: 600
enhanced_loading: null
---
# Lab 6: Invoke the Agent from the Copilot CLI

The Copilot UI is convenient, but the CLI lets you trigger flag cleanup workflows without leaving your terminal. In this final challenge, you'll install the GitHub Copilot CLI and use it to invoke the LaunchDarkly agent directly.

Let's go ahead and switch to the [Terminal](tab#2) tab.

1. Make sure you're in the repo folder:
```bash
cd ~/ld-sample-app-python
```
2. Invoke the LaunchDarkly agent directly with a prompt:
```bash
copilot --agent=launchdarkl-flag-cleanup --prompt "Remove the feature flag 'coffee-promo-1' in the launchdarkly project '[[ Instruqt-Var key="projectKey" hostname="workstation" ]]' and update the code to use the true variant."
```
4. Alternatively, launch the CLI in interactive mode and use the slash command to select the agent:
```bash
copilot
/agent launchdarkly-flag-cleanup
```
5. Observe that the agent performs the same flag evaluation and cleanup workflow as in the UI — querying flag status, analyzing code usage, and creating a pull request.

Congratulations! You've completed the track. You now have a fully configured LaunchDarkly agent that lets you manage feature flag lifecycle using natural language — both from the GitHub UI and your terminal.

Once you've successfully run a CLI-triggered agent task, click **Check** to finish.