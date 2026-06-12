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
- id: j7miuxhruxos
  title: LaunchDarkly
  type: browser
  hostname: launchdarkly
- id: ypvwtd2ewjpe
  title: GitHub
  type: browser
  hostname: github
- id: x6kwfduugrsc
  title: Terminal
  type: terminal
  hostname: workstation
difficulty: ""
timelimit: 600
enhanced_loading: null
---
# Lab 4: Assess a Flag for Removal Using the Copilot UI

Now that everything is configured, you'll use the LaunchDarkly agent through the GitHub Copilot UI to evaluate whether a feature flag is safe to remove.

1. In the [GitHub](tab#1) Tab, return to the repository by clicking the user avatar in the upper right corner, then click **Repositories**.
2. Click **ld-sample-app-python**, then click the **Agents** tab.
3. Click the Agents icon:
![Agents Icon](../assets/agent-icon.png)
4. Select `launchdarkly-flag-cleanup`.
4. Enter the following prompt:
```
Check if the flag  `coffee-promo-1` in the launchdarkly project `[[ Instruqt-Var key="projectKey" hostname="workstation" ]]` is safe to remove from this codebase.
```
Review the agent's response. It will query the LaunchDarkly API to check flag status across environments, look for any dependent flags, and analyze how the flag is used in the codebase.
Note the removal readiness assessment the agent provides — pay attention to whether it identifies a clear winning variant and whether any environments still have the flag actively targeted.

The agent won't make any changes yet — this challenge is about understanding what the agent checks before taking action.
Once you've reviewed the assessment output, click **Check** to continue.