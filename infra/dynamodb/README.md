# GitHub Copilot workshop user pool

A small AWS-side fixture that lets concurrent Instruqt sessions check out a
GitHub account from a fixed pool of 12, without ever double-assigning.

## Table

`gh-copilot-workshop-users` (PAY_PER_REQUEST)

| Attribute        | Type | Notes |
| ---------------- | ---- | ----- |
| `username`       | S    | Partition key. GitHub login (e.g. `launchdarkly-user-01`). |
| `status`         | S    | `available` or `checked_out`. GSI hash key. |
| `password_ref`   | S    | Secrets Manager ARN for the account password. |
| `refresh_token_ref` | S | Secrets Manager ARN for the GitHub App refresh token. Set by `infra/gh_app/consent.py`. |
| `totp_seed_ref`  | S    | Secrets Manager ARN for the GitHub TOTP base32 seed. Set by `bootstrap-totp.py`. |
| `pat_ref`        | S    | Secrets Manager ARN for the user's GitHub PAT (classic or fine-grained). Set by `bootstrap-pat.py`. |
| `sandbox_id`     | S    | Instruqt `$_SANDBOX_ID` of the holder. Removed on release. GSI hash key. |
| `checked_out_at` | N    | Unix ts. Removed on release. |
| `expires_at`     | N    | Unix ts. Removed on release. Used by the TTL sweeper. |

### Global secondary indexes

- `status-index` — `HASH: status`. Used at checkout to query for `available` rows.
- `sandbox-index` — `HASH: sandbox_id`. Used at release to find the row this sandbox is holding.

Both are sparse: when a row is released, `sandbox_id` is removed, so it stops
appearing in `sandbox-index`. Likewise `status-index` always reflects current
state because the attribute is rewritten on every transition.

## Checkout protocol

Atomic via `UpdateItem` with a conditional. From the workstation:

1. Query `status-index` for `status = available`, limit 12.
2. Shuffle the candidates client-side (avoids thundering-herd on row 1).
3. For each candidate, attempt `UpdateItem` with
   `ConditionExpression: status = "available"`.
4. First success wins. `ConditionalCheckFailedException` means someone beat us
   to that row — move on to the next candidate.
5. If every candidate is contended, the pool is exhausted; fail loudly.

The helper that implements this is `instruqt/track_scripts/lib/pool.py`.

## Release protocol

On `cleanup-workstation`:

1. Query `sandbox-index` for `sandbox_id = $_SANDBOX_ID`.
2. For each row (should be exactly one), `UpdateItem` to set `status =
   available` and `REMOVE sandbox_id, checked_out_at, expires_at`. Condition on
   `sandbox_id = :sid` so we never release a row we don't own.

Release is best-effort — `cleanup-workstation` calls it with `|| true`. The
sweeper below is the safety net.

## TTL sweeper

Workstations can die without `cleanup-workstation` running (kernel panic,
Instruqt platform restart, learner closes the tab during a 2-hour track).
A scheduled Lambda runs every 5 minutes and:

```
SCAN status = "checked_out" AND expires_at < now()
  → UpdateItem SET status="available" REMOVE sandbox_id, checked_out_at, expires_at
    CONDITION expires_at < :now
```

`expires_at` is set to `checked_out_at + POOL_LOCK_TTL_SECS` (default 2h, set
to match the track's `timelimit`). The sweeper isn't built yet — file a
follow-up before going to production.

## IAM

The workstation needs a single IAM principal whose access key is delivered via
Instruqt secrets (`AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` — already
declared in `instruqt/config.yml`). Least-privilege policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PoolCheckout",
      "Effect": "Allow",
      "Action": ["dynamodb:Query", "dynamodb:UpdateItem"],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:ACCOUNT_ID:table/gh-copilot-workshop-users",
        "arn:aws:dynamodb:us-east-1:ACCOUNT_ID:table/gh-copilot-workshop-users/index/*"
      ]
    },
    {
      "Sid": "ReadPoolSecrets",
      "Effect": "Allow",
      "Action": ["secretsmanager:GetSecretValue"],
      "Resource": ["arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:gh-copilot-workshop/*"]
    },
    {
      "Sid": "RotateRefreshTokens",
      "Effect": "Allow",
      "Action": ["secretsmanager:PutSecretValue"],
      "Resource": ["arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:gh-copilot-workshop/*/refresh-token-*"]
    }
  ]
}
```

`PutSecretValue` is required because GitHub App refresh tokens are single-use:
each call to the token endpoint with `grant_type=refresh_token` invalidates the
old token and returns a fresh one, which must be written back before the access
token is handed to anything else. See `infra/gh_app/README.md`.

## Provisioning

- `create-table.sh` — idempotent `aws` CLI script to create the table and both
  GSIs.
- `bootstrap-users.py` — reads a CSV of `(username,password)`, creates the
  Secrets Manager secrets, inserts the 12 DynamoDB rows. Run once.

Both are intentionally shell/python rather than Terraform — the workshop's
existing Terraform module (`/opt/ld/terraform-ld-student`) runs per-sandbox.
Pool infra is global and provisioned once, so it doesn't belong there.
Conversion to Terraform is a low-cost follow-up if you'd rather have a single
source of truth.
