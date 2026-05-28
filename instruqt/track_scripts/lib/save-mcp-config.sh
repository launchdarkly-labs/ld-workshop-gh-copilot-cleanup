#!/usr/bin/env bash
#
# Save the LaunchDarkly entry to the assigned pool user's Copilot MCP config,
# using the GitHub App user-access token wired in by setup-workstation.
# Replaces the manual web-UI login step that Challenge 2 used to require.

set -eu

LD_API_TOKEN="${1:-${LD_API_TOKEN:-}}"
if [ -z "$LD_API_TOKEN" ]; then
    cat >&2 <<'EOF'
usage: save-mcp-config <launchdarkly-api-token>

Paste the token you generated in Challenge 1 (starts with 'api-').
EOF
    exit 1
fi

if [ -z "${GITHUB_TOKEN:-}" ]; then
    echo "GITHUB_TOKEN is not set — setup-workstation didn't run cleanly." >&2
    exit 1
fi

# Build the payload with jq so the API key is properly escaped regardless of
# what the learner pastes.
PAYLOAD=$(jq -n --arg key "$LD_API_TOKEN" '{
  mcpServers: {
    LaunchDarkly: {
      type: "local",
      tools: ["*"],
      command: "npx",
      args: ["-y", "--package", "@launchdarkly/mcp-server", "--", "mcp", "start", "--api-key", $key]
    }
  }
}')

curl -fsS -X PUT \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -H "Content-Type: application/json" \
    https://api.github.com/user/copilot/coding-agent/mcp-config \
    -d "$PAYLOAD" >/dev/null

echo "LaunchDarkly MCP entry saved for your Copilot session."
