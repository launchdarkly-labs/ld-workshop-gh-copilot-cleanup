---
slug: assess-flag-removal
id: l1aaedro0dz6
type: challenge
title: Assess a Flag for Removal Using the Copilot UI
teaser: Use the LaunchDarkly agent in the GitHub Copilot UI to evaluate whether a
  specific feature flag is ready to be removed, without making any code changes yet.
notes:
- type: text
  contents: "\U0001F4A1 One of the most common causes of flag cleanup mistakes is
    removing a flag before checking whether it's still being actively targeted in
    any environment. The LaunchDarkly agent cross-references flag status across all
    environments before recommending removal."
tabs:
- id: yke7st3iayjj
  title: LaunchDarkly
  type: browser
  hostname: launchdarkly
- id: cefmhiqilg6k
  title: Code Editor
  type: service
  hostname: workstation
  port: 8080
- id: w8obaowwr6ov
  title: GitHub
  type: browser
  hostname: github
- id: sn6bwvgrimpo
  title: Coffee Shop App
  type: service
  hostname: workstation
  path: /
  port: 3000
- id: 8jpt6go5lexj
  title: Terminal
  type: terminal
  hostname: workstation
difficulty: ""
timelimit: 600
enhanced_loading: null
---
# Lab 4: Assess a Flag for Removal Using the Copilot UI

Now that everything is configured, you'll use the LaunchDarkly agent through the GitHub Copilot UI to evaluate whether a feature flag is safe to remove.

First, sign in to the GitHub tab with the account assigned to your session (you'll stay signed in for Challenge 5):
**Username:** `[[ Instruqt-Var key="gh_user" hostname="workstation" ]]`
**Password:** `[[ Instruqt-Var key="gh_pass" hostname="workstation" ]]`

1. In the GitHub Tab, click the **Agents** tab.
2. Click the Agents icon () and select `launchdarkly-flag-cleanup`.
3. Enter the following prompt:
```
Check if the flag 'coffee-promo-1' is safe to remove from the codebase.
```
Review the agent's response. It will query the LaunchDarkly API to check flag status across environments, look for any dependent flags, and analyze how the flag is used in the codebase.
Note the removal readiness assessment the agent provides — pay attention to whether it identifies a clear winning variant and whether any environments still have the flag actively targeted.

The agent won't make any changes yet — this challenge is about understanding what the agent checks before taking action.
Once you've reviewed the assessment output, click **Check** to continue.