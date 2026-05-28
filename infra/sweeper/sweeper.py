"""
Sweeps stale checkouts off the pool. Released rows are returned to
`status = available`. Invoked by EventBridge on a 5-minute schedule.

A row is stale when `status == "checked_out"` and `expires_at < now()`.
The release is a conditional UpdateItem with `expires_at < :now` so we
never clobber a row that's been legitimately refreshed in the gap between
our scan and our update.
"""

import logging
import os
import time

import boto3
from botocore.exceptions import ClientError

REGION = os.environ.get("AWS_REGION", "us-east-1")
TABLE = os.environ.get("POOL_TABLE_NAME", "gh-copilot-workshop-users")

ddb = boto3.client("dynamodb", region_name=REGION)
log = logging.getLogger()
log.setLevel(logging.INFO)


def lambda_handler(event, context):  # noqa: ARG001
    now = int(time.time())
    swept = 0
    stuck_without_ttl = 0

    paginator = ddb.get_paginator("query")
    pages = paginator.paginate(
        TableName=TABLE,
        IndexName="status-index",
        KeyConditionExpression="#s = :checked",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":checked": {"S": "checked_out"}},
    )

    for page in pages:
        for item in page.get("Items", []):
            username = item["username"]["S"]
            exp = item.get("expires_at", {}).get("N")
            if not exp:
                # Should not happen with current setup-workstation, but be
                # defensive: a row stuck in checked_out with no TTL would
                # never be reclaimed otherwise.
                log.warning("row %s is checked_out with no expires_at; skipping", username)
                stuck_without_ttl += 1
                continue
            if int(exp) >= now:
                continue

            try:
                ddb.update_item(
                    TableName=TABLE,
                    Key={"username": {"S": username}},
                    UpdateExpression=(
                        "SET #s = :avail "
                        "REMOVE sandbox_id, checked_out_at, expires_at"
                    ),
                    ConditionExpression="expires_at < :now AND #s = :checked",
                    ExpressionAttributeNames={"#s": "status"},
                    ExpressionAttributeValues={
                        ":avail": {"S": "available"},
                        ":checked": {"S": "checked_out"},
                        ":now": {"N": str(now)},
                    },
                )
                swept += 1
                log.info("released stale lock for %s (expired at %s, now %s)", username, exp, now)
            except ClientError as e:
                if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                    # The row was refreshed or released between our scan and
                    # our update. That's the happy path — leave it alone.
                    continue
                raise

    log.info("sweep complete: released=%d, stuck_without_ttl=%d", swept, stuck_without_ttl)
    return {"released": swept, "stuck_without_ttl": stuck_without_ttl}
