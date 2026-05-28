# GitHub App consent + token refresh

Once per pool user, run `consent.py` to capture a refresh token. At session
start, `instruqt/track_scripts/lib/gh_auth.py` trades the refresh token for a
short-lived access token (and stores the rotated refresh token back).

## App metadata (recorded for ops)

- App ID: `3897656`
- Installation ID: `136376199` (org-wide install in `launchdarkly-training`)
- Device flow: enabled (no callback URL needed)

Secrets in AWS Secrets Manager (`us-east-1`). All entries are stored as
**key/value** secrets where the key matches the last segment of the secret
name (e.g. the secret `gh-copilot-workshop/app/client-id` has JSON body
`{"client-id": "Iv23li..."}`). The resolver in `pool.py` / `gh_auth.py` /
`consent.py` auto-extracts on this convention.

| Secret name | Key | Contents |
| --- | --- | --- |
| `gh-copilot-workshop/app/client-id` | `client-id` | App OAuth client ID |
| `gh-copilot-workshop/app/client-secret` | `client-secret` | App OAuth client secret |
| `gh-copilot-workshop/app/private-key` | `private-key` | App private key PEM (reserved for future installation-token use) |
| `gh-copilot-workshop/<username>/password` | `password` | Pool user's GitHub password (created by `bootstrap-users.py`) |
| `gh-copilot-workshop/<username>/refresh-token` | `refresh-token` | Pool user's App refresh token (created by `consent.py`) |

## Per-user consent (one-time)

```bash
cd infra/gh_app
python3 -m venv .venv && source .venv/bin/activate
pip install boto3
for u in launchdarkly-user-{01..12}; do
    echo "=== $u ==="
    python3 consent.py "$u"
    read -p "Press enter when ready to enroll the next user..."
done
```

The script prints a verification URL and an 8-character code. Open the URL in
a private/incognito window, sign in as the pool user, paste the code, approve
the App. The script writes the resulting refresh token to Secrets Manager and
links its ARN into the DynamoDB row's `refresh_token_ref` attribute.

Refresh tokens are valid for 6 months but **rotate on every use** — the
workstation-side helper writes the new one back at every session start, so as
long as the workshop runs at least once every 6 months per account, you never
need to re-consent. If a user goes dormant, just rerun `consent.py` for them.

## Token refresh (per session, automated)

`instruqt/track_scripts/lib/gh_auth.py refresh <username>` reads the current
refresh token, calls GitHub's token endpoint with `grant_type=refresh_token`,
writes back the rotated refresh token, and prints the access token on stdout.
`pool.py checkout` invokes it as part of the atomic checkout so the lock is
only useful when paired with a working token.

## Reset / revocation

To force a user off the workshop:

```bash
# Revoke the App's authorization for that user
gh auth login    # as that user, in a private window
gh api -X DELETE /applications/<client_id>/grant   # nukes the refresh token

# Remove the stored secret
aws secretsmanager delete-secret \
    --secret-id gh-copilot-workshop/<username>/refresh-token \
    --force-delete-without-recovery
```

Rerun `consent.py` afterward to re-enroll.
