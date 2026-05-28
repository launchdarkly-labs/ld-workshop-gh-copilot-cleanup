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
- id: jk9fx4dcuv4d
  title: LaunchDarkly
  type: browser
  hostname: launchdarkly
- id: ikyucf6lcxxx
  title: Code Editor
  type: service
  hostname: workstation
  port: 8080
- id: ey6iyce4gwyh
  title: GitHub
  type: browser
  hostname: github
- id: 7l5kmbo3p5kx
  title: Coffee Shop App
  type: service
  hostname: workstation
  path: /
  port: 3000
- id: ypcqdnpe4bwv
  title: Terminal
  type: terminal
  hostname: workstation
difficulty: ""
timelimit: 600
enhanced_loading: null
---
# Lab 3: Add the LaunchDarkly Custom Agent Profile

The MCP server handles API communication, but the custom agent profile is what gives GitHub Copilot its specialized knowledge of LaunchDarkly workflows — things like how to evaluate flag readiness, identify forward values, and structure pull requests that preserve production behavior.

1. In the Terminal tab, enter `cd /opt/python/ld-sample-app-python`.
2. Next, enter `mkdir -p .github/agents`, then `cd .github/agents`.
3. Now we need to download the LaunchDarkly agent profile. Enter `wget https://raw.githubusercontent.com/github/awesome-copilot/refs/heads/main/agents/launchdarkly-flag-cleanup.agent.md`.
4. This environment, you won't be able to commit this file to the repo, but when you run this in your environment, make sure you commit to your repo's default branch at this point.

With both the MCP server configured and the agent profile committed, your repository is now fully set up to use the LaunchDarkly Copilot agent.

Click **Check** to continue.