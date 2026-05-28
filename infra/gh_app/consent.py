#!/usr/bin/env python3
"""
One-time per pool user: walk the GitHub App's device-flow consent screen, capture
the resulting refresh token, persist it in Secrets Manager, and link the DynamoDB
row to its ARN.

Run from operator laptop with admin AWS credentials. Sign in to GitHub in your
browser as the pool user you're about to enroll BEFORE you start the script, or
sign in when prompted at the verification URL.

Usage:
    python3 consent.py launchdarkly-user-01
"""

import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request

import boto3

# python.org's macOS installer ships without trusted CA roots wired into the
# system keychain; using certifi (which boto3 already pulls in) keeps the
# script self-contained regardless of how the operator installed Python.
try:
    import certifi
    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CTX = ssl.create_default_context()

REGION = os.environ.get("AWS_REGION", "us-east-1")
TABLE = os.environ.get("POOL_TABLE_NAME", "gh-copilot-workshop-users")
SECRET_PREFIX = os.environ.get("POOL_SECRET_PREFIX", "gh-copilot-workshop")
CLIENT_ID_SECRET = f"{SECRET_PREFIX}/app/client-id"

DEVICE_CODE_URL = "https://github.com/login/device/code"
TOKEN_URL = "https://github.com/login/oauth/access_token"

ddb = boto3.client("dynamodb", region_name=REGION)
sm = boto3.client("secretsmanager", region_name=REGION)


def _post_form(url: str, fields: dict) -> dict:
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, context=_SSL_CTX) as resp:
        return json.loads(resp.read())


def _resolve_secret(secret_id: str) -> str:
    """
    Read a secret value. Supports both plain SecretString and key/value (JSON)
    secrets — for the latter we extract the value whose key matches the last
    path segment of the secret name. e.g. `gh-copilot-workshop/app/client-id`
    -> looks for key `client-id` in the JSON.
    """
    raw = sm.get_secret_value(SecretId=secret_id)["SecretString"]
    try:
        parsed = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return raw
    if isinstance(parsed, dict):
        key = secret_id.rstrip("/").split("/")[-1]
        if key in parsed:
            return parsed[key]
    return raw


def _upsert_refresh_secret(username: str, refresh_token: str) -> str:
    name = f"{SECRET_PREFIX}/{username}/refresh-token"
    # Store as key/value JSON to match the convention used for app/* secrets.
    payload = json.dumps({"refresh-token": refresh_token})
    try:
        sm.create_secret(Name=name, SecretString=payload)
    except sm.exceptions.ResourceExistsException:
        sm.put_secret_value(SecretId=name, SecretString=payload)
    return sm.describe_secret(SecretId=name)["ARN"]


def _link_row(username: str, arn: str) -> None:
    ddb.update_item(
        TableName=TABLE,
        Key={"username": {"S": username}},
        UpdateExpression="SET refresh_token_ref = :r",
        ExpressionAttributeValues={":r": {"S": arn}},
    )


def _ensure_pool_row(username: str) -> None:
    """Pre-flight: bail before doing anything irreversible (device flow approval,
    secret rotation) if the DDB row for this user isn't ready yet."""
    try:
        resp = ddb.get_item(TableName=TABLE, Key={"username": {"S": username}})
    except ddb.exceptions.ResourceNotFoundException:
        sys.exit(
            f"DynamoDB table {TABLE!r} does not exist in {REGION}.\n"
            f"Run infra/dynamodb/create-table.sh and infra/dynamodb/bootstrap-users.py first."
        )
    if "Item" not in resp:
        sys.exit(
            f"No pool row for {username!r} in {TABLE!r}.\n"
            f"Add it via infra/dynamodb/bootstrap-users.py before running consent.py."
        )


def link_only(username: str) -> None:
    """Attach an already-stored refresh token to the (now-existing) DDB row.
    Used to recover from a consent run that captured the token but failed to
    link, without forcing the operator to re-approve the App."""
    _ensure_pool_row(username)
    secret_name = f"{SECRET_PREFIX}/{username}/refresh-token"
    try:
        arn = sm.describe_secret(SecretId=secret_name)["ARN"]
    except sm.exceptions.ResourceNotFoundException:
        sys.exit(f"no refresh-token secret at {secret_name}; run consent.py without --link-only first")
    _link_row(username, arn)
    print(f"Linked {username} -> {arn}")


def main(username: str) -> None:
    _ensure_pool_row(username)
    client_id = _resolve_secret(CLIENT_ID_SECRET)

    print("Requesting device code...")
    code = _post_form(DEVICE_CODE_URL, {"client_id": client_id})
    if "error" in code:
        sys.exit(f"device code request failed: {code}")

    print()
    print(f"  Open: {code['verification_uri']}")
    print(f"  Code: {code['user_code']}")
    print()
    print(f"Sign in to GitHub as {username} (in a private window if you're")
    print("already signed in as someone else), enter the code above, and")
    print("approve the App's permissions.")
    print()

    interval = max(int(code.get("interval", 5)), 5)
    deadline = time.time() + int(code.get("expires_in", 900))

    while time.time() < deadline:
        time.sleep(interval)
        resp = _post_form(
            TOKEN_URL,
            {
                "client_id": client_id,
                "device_code": code["device_code"],
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            },
        )
        err = resp.get("error")
        if err == "authorization_pending":
            continue
        if err == "slow_down":
            interval += 5
            continue
        if err in {"expired_token", "access_denied"}:
            sys.exit(f"consent flow ended: {err}")
        if err:
            sys.exit(f"unexpected error: {resp}")

        refresh_token = resp.get("refresh_token")
        if not refresh_token:
            sys.exit(f"no refresh_token in response: {resp}")

        arn = _upsert_refresh_secret(username, refresh_token)
        _link_row(username, arn)
        print(f"Stored refresh token for {username} at {arn}")
        return

    sys.exit("timed out waiting for user to authorize")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[2] == "--link-only":
        link_only(sys.argv[1])
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        sys.exit("usage: consent.py <pool-username> [--link-only]")
