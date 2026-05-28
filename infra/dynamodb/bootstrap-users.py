#!/usr/bin/env python3
"""
One-shot bootstrap: read a CSV of (username,password), create a Secrets Manager
secret per user, and insert/refresh the DynamoDB pool row.

Usage:
    python3 bootstrap-users.py users.csv

CSV format (header required):
    username,password
    launchdarkly-user-01,LaunchDarkly-Lab-01
    ...

Re-running is safe:
  - If the secret already exists, its value is updated via PutSecretValue.
  - If the row already exists, only password_ref is rewritten; status / lock
    fields are left untouched so an in-flight checkout isn't disturbed.
"""

import csv
import json
import os
import sys

import boto3
from botocore.exceptions import ClientError

REGION = os.environ.get("AWS_REGION", "us-east-1")
TABLE = os.environ.get("POOL_TABLE_NAME", "gh-copilot-workshop-users")
SECRET_PREFIX = os.environ.get("POOL_SECRET_PREFIX", "gh-copilot-workshop")

ddb = boto3.client("dynamodb", region_name=REGION)
sm = boto3.client("secretsmanager", region_name=REGION)


def upsert_secret(name: str, key: str, value: str) -> str:
    """Stored as key/value JSON to match the rest of gh-copilot-workshop/*."""
    payload = json.dumps({key: value})
    try:
        sm.create_secret(Name=name, SecretString=payload)
    except ClientError as e:
        if e.response["Error"]["Code"] != "ResourceExistsException":
            raise
        sm.put_secret_value(SecretId=name, SecretString=payload)
    return sm.describe_secret(SecretId=name)["ARN"]


def upsert_row(username: str, password_arn: str) -> None:
    try:
        ddb.update_item(
            TableName=TABLE,
            Key={"username": {"S": username}},
            UpdateExpression="SET password_ref = :p, #s = if_not_exists(#s, :avail)",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={
                ":p": {"S": password_arn},
                ":avail": {"S": "available"},
            },
        )
    except ClientError as e:
        print(f"failed to upsert row for {username}: {e}", file=sys.stderr)
        raise


def main(csv_path: str) -> None:
    with open(csv_path, newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            username = row["username"].strip()
            password = row["password"]
            secret_name = f"{SECRET_PREFIX}/{username}/password"
            arn = upsert_secret(secret_name, "password", password)
            upsert_row(username, arn)
            print(f"  {username} -> {arn}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: bootstrap-users.py <users.csv>", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1])
