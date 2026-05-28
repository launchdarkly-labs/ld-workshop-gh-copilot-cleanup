# Pool TTL sweeper

A 5-minute scheduled Lambda that releases stale checkouts. Without this,
a workstation that dies mid-session (kernel panic, platform restart, learner
closes the tab during a 2-hour track) would leave its row locked until the
next operator notices.

## What it does

Queries the `status-index` GSI for rows where `status = "checked_out"`,
filters to those whose `expires_at < now()`, and conditionally releases each
one. The condition `expires_at < :now AND status = :checked` makes the sweep
race-safe: if `cleanup-workstation` fires between our scan and our update,
the conditional fails and we leave the row alone.

`expires_at` is written by `setup-workstation` as
`checked_out_at + POOL_LOCK_TTL_SECS` (default 7200 = 2h, matches the track's
`timelimit`).

## Deploy

```bash
AWS_REGION=us-east-1 ./infra/sweeper/deploy.sh
```

Idempotent. Re-running updates the Lambda code in place (e.g. after editing
`sweeper.py`). The IAM role, inline policy, schedule, and EventBridge
permission are all reconciled to the desired state on each run.

## Configuration (env vars)

| Var | Default | Purpose |
| --- | --- | --- |
| `AWS_REGION` | `us-east-1` | Region for table + Lambda + rule |
| `POOL_TABLE_NAME` | `gh-copilot-workshop-users` | Target table |
| `SWEEPER_FUNCTION_NAME` | `gh-copilot-workshop-sweeper` | Lambda name |
| `SWEEPER_ROLE_NAME` | `gh-copilot-workshop-sweeper` | IAM role name |
| `SWEEPER_RULE_NAME` | `gh-copilot-workshop-sweeper-schedule` | EventBridge rule name |
| `SWEEPER_SCHEDULE` | `rate(5 minutes)` | Any EventBridge schedule expression |

## Verify it's working

Manually invoke once after deploy:

```bash
aws lambda invoke --region us-east-1 \
    --function-name gh-copilot-workshop-sweeper /tmp/out.json
cat /tmp/out.json   # {"released": N, "stuck_without_ttl": 0}
```

Tail logs:

```bash
aws logs tail /aws/lambda/gh-copilot-workshop-sweeper --region us-east-1 --follow
```

## Tear down

```bash
aws events remove-targets --region us-east-1 --rule gh-copilot-workshop-sweeper-schedule --ids sweeper-target
aws events delete-rule    --region us-east-1 --name gh-copilot-workshop-sweeper-schedule
aws lambda delete-function --region us-east-1 --function-name gh-copilot-workshop-sweeper
aws iam delete-role-policy --role-name gh-copilot-workshop-sweeper --policy-name gh-copilot-workshop-sweeper-inline
aws iam delete-role        --role-name gh-copilot-workshop-sweeper
```
