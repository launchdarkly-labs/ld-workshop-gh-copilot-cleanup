---
slug: remove-flag-open-pr
id: 7jerdlxmslze
type: challenge
title: Remove a Flag and Open a Pull Request
teaser: Instruct the LaunchDarkly agent to fully clean up a feature flag — removing
  all references from the codebase and opening a pull request that locks in the correct
  production behavior.
notes:
- type: text
  contents: "\U0001F4A1 Flag debt is a real problem at scale. Studies have found that
    long-lived feature flags are one of the leading sources of unintended complexity
    in codebases. Automating cleanup with an agent like this can significantly reduce
    the time flags spend lingering past their useful life."
tabs:
- id: 1wikgup293oz
  title: LaunchDarkly
  type: browser
  hostname: launchdarkly
- id: v7lfgavakwfh
  title: GitHub
  type: browser
  hostname: github
- id: ktr4zm41npqb
  title: Terminal
  type: terminal
  hostname: workstation
difficulty: ""
timelimit: 600
enhanced_loading: null
---
# Lab 5: Remove a Flag and Open a Pull Request

With confidence that a flag is ready for removal, you'll now instruct the LaunchDarkly agent to do the actual cleanup — removing the flag references from code and opening a pull request that preserves production behavior.

1. Return to the GitHub Instruqt tab, and make sure you're still on the **Agents** within GitHub.
2. Click the Agents icon () and select `launchdarkly-flag-cleanup`.
3. Enter a prompt to trigger the full cleanup workflow, for example:
```
Remove the feature flag `coffee-promo-1` in the launchdarkly project `[[ Instruqt-Var key="projectKey" hostname="workstation" ]]` and update the code to use the true variant.
```
4. The agent will:
	* Identify the correct forward value (the variant to preserve)
	* Remove all flag references from the codebase
	* Open a pull request with the changes
5. Navigate to your repository's Pull Requests tab and open the PR the agent created.
6. Review the diff to confirm that the code now reflects the winning variant directly, with no remaining flag checks.

Once you've reviewed the pull request, click **Check** to continue.