---
slug: generate-api-token
id: s9lv9nxtkwsb
type: challenge
title: Generate a LaunchDarkly API Token
teaser: Create a LaunchDarkly API access token with the appropriate permissions needed
  for the Copilot agent to read, create, and update feature flags on your behalf.
notes:
- type: text
  contents: "\U0001F4A1 LaunchDarkly supports fine-grained custom roles, so you can
    scope your API token to only the projects and environments your agent needs access
    to — a good practice for production setups."
tabs:
- id: rmpn4htbpuwv
  title: LaunchDarkly
  type: browser
  hostname: launchdarkly
- id: sgwdplekrjvp
  title: Code Editor
  type: service
  hostname: workstation
  port: 8080
- id: 7j6z1gyhitxi
  title: GitHub
  type: browser
  hostname: github
- id: xjqu5ek1yqke
  title: Coffee Shop App
  type: service
  hostname: workstation
  path: /
  port: 3000
- id: jfmj3euyanwe
  title: Terminal
  type: terminal
  hostname: workstation
difficulty: ""
timelimit: 600
enhanced_loading: null
---
# Lab 1: Generate a LaunchDarkly API Token

Before the LaunchDarkly Copilot agent can interact with your feature flags, it needs a way to authenticate with the LaunchDarkly API. In this challenge, you'll create an API access token with the right permissions.

1. In the LaunchDarkly tab and navigate to **Organization Settings** → **Authorization** → **Access Tokens**.
2. Click **Create token** and give it a descriptive name (e.g., `copilot-cleanup-[[ Instruqt-Var key="projectkey" hostname="workstation" ]]`).
3. Assign the token the **Custom** base role, then select `instruqt-workshop - [[ Instruqt-Var key="projectkey" hostname="workstation" ]] Admin` under **Custom roles**.
4. Click **Save Token**
5. Copy the generated token and store it somewhere safe — you won't be able to view it again after closing the dialog.

⚠️ Treat this token like a password. You'll use it in the next challenge to configure the MCP server.

Once you have your token saved, click **Check** to continue.