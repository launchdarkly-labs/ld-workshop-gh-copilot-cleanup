#!/usr/bin/env python3
"""
Store a GitHub personal access token (PAT) for a single pool user.

Usage:
    python3 bootstrap-pat.py <username> <pat>

Re-running for the same user overwrites the existing secret. The DynamoDB
row's `pat_ref` ARN is stable across overwrites.
"""

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


def main(username: str, pat: str) -> None:
    name = f"{SECRET_PREFIX}/{username}/pat"
    payload = json.dumps({"pat": pat})
    try:
        sm.create_secret(Name=name, SecretString=payload)
    except ClientError as e:
        if e.response["Error"]["Code"] != "ResourceExistsException":
            raise
        sm.put_secret_value(SecretId=name, SecretString=payload)
    arn = sm.describe_secret(SecretId=name)["ARN"]
    ddb.update_item(
        TableName=TABLE,
        Key={"username": {"S": username}},
        UpdateExpression="SET pat_ref = :r",
        ExpressionAttributeValues={":r": {"S": arn}},
    )
    print(f"{username} -> {arn}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: bootstrap-pat.py <username> <pat>")
    main(sys.argv[1], sys.argv[2])
