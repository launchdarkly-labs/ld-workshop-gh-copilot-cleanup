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
difficulty: ""
timelimit: 600
enhanced_loading: null
---
# Lab 1: Generate a LaunchDarkly API Token

Before the LaunchDarkly Copilot agent can interact with your feature flags, it needs a way to authenticate with the LaunchDarkly API. In this challenge, you'll create an API access token with the right permissions.

1. At the bottom of the left-hand navigation panel, click on the **Organization Settings**.
![Organization Settings](../assets/ld-img-settings.png)
2. Scroll down the navigation panel and click **Authorization**.
3. Scroll down to **Access tokens** and click **Create token**.
4. In the **Name** field, enter:
```
copilot-cleanup-[[ Instruqt-Var key="projectkey" hostname="workstation" ]]
```
5. Assign the token the **Custom** base role, then select `instruqt-workshop - [[ Instruqt-Var key="projectkey" hostname="workstation" ]] Admin` under **Custom roles**.
6. Click **Save Token**
7. Copy the generated token and store it somewhere safe — you won't be able to view it again after closing the dialog.

⚠️ Treat this token like a password. You'll use it in the next challenge to configure the MCP server.

Once you have your token saved, click **Check** to continue.