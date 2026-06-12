---
slug: add-custom-agent-profile
id: qxcgqn620uqb
type: challenge
title: Add the LaunchDarkly Custom Agent Profile
teaser: Commit the LaunchDarkly agent profile to your repository, giving GitHub Copilot
  the specialized instructions it needs to handle feature flag lifecycle workflows.
notes:
- type: text
  contents: "\U0001F4A1 Custom agent profiles are written in Markdown and act like
    a system prompt for Copilot's coding agent. The LaunchDarkly agent profile includes
    built-in guidance on how to safely identify a flag's forward value before removing
    it from code."
tabs:
- id: chyosqa7xo6q
  title: LaunchDarkly
  type: browser
  hostname: launchdarkly
- id: zrz6bl8ytqnz
  title: GitHub
  type: browser
  hostname: github
- id: yg7qem2xyxj1
  title: Terminal
  type: terminal
  hostname: workstation
difficulty: ""
timelimit: 600
enhanced_loading: null
---
# Lab 3: Add the LaunchDarkly Custom Agent Profile

The MCP server handles API communication, but the custom agent profile is what gives GitHub Copilot its specialized knowledge of LaunchDarkly workflows — things like how to evaluate flag readiness, identify forward values, and structure pull requests that preserve production behavior.

First, let's get our repo ready in our terminal.

1. Go to the [GitHub](tab#1) tab, and in the upper-right corner, click on the user avatar, then click **Settings**.
2. Click **SSH and GPG keys**, then under SSH keys, click **New SSH key**.
3. For **Title**, enter:
```text
Copilot Cleanup User
```
4. Leave **Key type** as **Authentication Key**.
5. For **Key**, enter:
```text
[[ Instruqt-Var key="git_ssh_key" hostname="workstation" ]]
```

1. Go to the [Terminal](tab#2) tab, and enter:
```text
git clone git@github.com:[[ Instruqt-Var key="gh_user" hostname="workstation" ]]/ld-sample-app-python.git && cd ld-sample-app-python
```
2. Next, enter:
```text
mkdir -p .github/agents && cd .github/agents
```
3. Now we need to download the LaunchDarkly agent profile. Enter
```text
wget https://raw.githubusercontent.com/github/awesome-copilot/refs/heads/main/agents/launchdarkly-flag-cleanup.agent.md
```
4. Now let's push this to our repo so we can start using it!
```text
git add launchdarkly-flag-cleanup.agent.md
git commit -m "Add Copilot flag cleanup agent"
git push
```

With both the MCP server configured and the agent profile committed, your repository is now fully set up to use the LaunchDarkly Copilot agent.

Click **Check** to continue.