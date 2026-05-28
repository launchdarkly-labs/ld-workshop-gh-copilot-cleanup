#!/usr/bin/env bash
#
# Idempotent: creates the user-pool table + GSIs if they don't exist.
# Re-running after the table exists is a no-op.

set -euo pipefail

TABLE="${POOL_TABLE_NAME:-gh-copilot-workshop-users}"
REGION="${AWS_REGION:-us-east-1}"

if aws dynamodb describe-table --table-name "$TABLE" --region "$REGION" >/dev/null 2>&1; then
  echo "Table $TABLE already exists in $REGION; nothing to do."
  exit 0
fi

aws dynamodb create-table \
  --region "$REGION" \
  --table-name "$TABLE" \
  --billing-mode PAY_PER_REQUEST \
  --attribute-definitions \
      AttributeName=username,AttributeType=S \
      AttributeName=status,AttributeType=S \
      AttributeName=sandbox_id,AttributeType=S \
  --key-schema \
      AttributeName=username,KeyType=HASH \
  --global-secondary-indexes \
      '[
        {
          "IndexName": "status-index",
          "KeySchema": [{"AttributeName": "status", "KeyType": "HASH"}],
          "Projection": {"ProjectionType": "ALL"}
        },
        {
          "IndexName": "sandbox-index",
          "KeySchema": [{"AttributeName": "sandbox_id", "KeyType": "HASH"}],
          "Projection": {"ProjectionType": "KEYS_ONLY"}
        }
      ]'

echo "Waiting for $TABLE to become ACTIVE..."
aws dynamodb wait table-exists --table-name "$TABLE" --region "$REGION"
echo "Done."
