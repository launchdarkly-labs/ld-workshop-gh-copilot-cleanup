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
- id: zzbjqpojw3dz
  title: LaunchDarkly
  type: browser
  hostname: launchdarkly
- id: kr8wwna5isjl
  title: Code Editor
  type: service
  hostname: workstation
  port: 8080
- id: xughtkr7exzx
  title: GitHub
  type: browser
  hostname: github
- id: vg002rpnuj20
  title: Coffee Shop App
  type: service
  hostname: workstation
  path: /
  port: 3000
- id: ggxg3xlghh63
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
Remove the feature flag `coffee-promo-1` in the project 'kevin-c-sample-app' and update the code to use the true variant.
```
4. The agent will:
	* Identify the correct forward value (the variant to preserve)
	* Remove all flag references from the codebase
	* Open a pull request with the changes
5. Navigate to your repository's Pull Requests tab and open the PR the agent created.
6. Review the diff to confirm that the code now reflects the winning variant directly, with no remaining flag checks.

Once you've reviewed the pull request, click **Check** to continue.