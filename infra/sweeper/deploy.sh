#!/usr/bin/env bash
#
# Idempotent: creates / updates the sweeper Lambda, its IAM role, and the
# EventBridge schedule that fires it every 5 minutes. Safe to re-run on
# code changes — it just updates the existing function.

set -euo pipefail

FUNCTION_NAME="${SWEEPER_FUNCTION_NAME:-gh-copilot-workshop-sweeper}"
ROLE_NAME="${SWEEPER_ROLE_NAME:-gh-copilot-workshop-sweeper}"
RULE_NAME="${SWEEPER_RULE_NAME:-gh-copilot-workshop-sweeper-schedule}"
TABLE="${POOL_TABLE_NAME:-gh-copilot-workshop-users}"
REGION="${AWS_REGION:-us-east-1}"
SCHEDULE="${SWEEPER_SCHEDULE:-rate(5 minutes)}"

SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd "$SCRIPT_DIR"

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# ---------- IAM role ----------

TRUST=$(cat <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
EOF
)

POLICY=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Sweep",
      "Effect": "Allow",
      "Action": ["dynamodb:Query", "dynamodb:UpdateItem"],
      "Resource": [
        "arn:aws:dynamodb:${REGION}:${ACCOUNT_ID}:table/${TABLE}",
        "arn:aws:dynamodb:${REGION}:${ACCOUNT_ID}:table/${TABLE}/index/*"
      ]
    },
    {
      "Sid": "Logs",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:${REGION}:${ACCOUNT_ID}:*"
    }
  ]
}
EOF
)

if ! aws iam get-role --role-name "$ROLE_NAME" >/dev/null 2>&1; then
    echo "Creating IAM role $ROLE_NAME..."
    aws iam create-role --role-name "$ROLE_NAME" \
        --assume-role-policy-document "$TRUST" >/dev/null
    echo "Waiting 10s for IAM eventual-consistency..."
    sleep 10
fi
aws iam put-role-policy --role-name "$ROLE_NAME" \
    --policy-name "${ROLE_NAME}-inline" \
    --policy-document "$POLICY"
ROLE_ARN=$(aws iam get-role --role-name "$ROLE_NAME" --query 'Role.Arn' --output text)

# ---------- package ----------

rm -f sweeper.zip
zip -qj sweeper.zip sweeper.py

# ---------- lambda ----------

if aws lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" >/dev/null 2>&1; then
    echo "Updating Lambda code..."
    aws lambda update-function-code --region "$REGION" \
        --function-name "$FUNCTION_NAME" \
        --zip-file fileb://sweeper.zip >/dev/null
else
    echo "Creating Lambda $FUNCTION_NAME..."
    aws lambda create-function --region "$REGION" \
        --function-name "$FUNCTION_NAME" \
        --runtime python3.12 \
        --role "$ROLE_ARN" \
        --handler sweeper.lambda_handler \
        --zip-file fileb://sweeper.zip \
        --timeout 30 \
        --environment "Variables={POOL_TABLE_NAME=$TABLE}" >/dev/null
fi
LAMBDA_ARN=$(aws lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" \
    --query 'Configuration.FunctionArn' --output text)

# ---------- EventBridge schedule ----------

aws events put-rule --region "$REGION" \
    --name "$RULE_NAME" \
    --schedule-expression "$SCHEDULE" \
    --state ENABLED >/dev/null
aws events put-targets --region "$REGION" \
    --rule "$RULE_NAME" \
    --targets "Id=sweeper-target,Arn=$LAMBDA_ARN" >/dev/null

# Permit EventBridge to invoke the Lambda. add-permission is not idempotent
# — second call returns ResourceConflictException — so swallow that case.
aws lambda add-permission --region "$REGION" \
    --function-name "$FUNCTION_NAME" \
    --statement-id allow-eventbridge \
    --action lambda:InvokeFunction \
    --principal events.amazonaws.com \
    --source-arn "arn:aws:events:${REGION}:${ACCOUNT_ID}:rule/${RULE_NAME}" \
    >/dev/null 2>&1 || true

rm -f sweeper.zip

echo
echo "Deployed."
echo "  function: $FUNCTION_NAME"
echo "  schedule: $SCHEDULE"
echo "  rule:     $RULE_NAME"
echo "  role:     $ROLE_NAME"
