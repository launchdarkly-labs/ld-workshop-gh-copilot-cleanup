#!/usr/bin/env python3
"""
RFC 6238 TOTP for the workshop pool. Reads the per-user base32 seed from
Secrets Manager and prints the current 6-digit code.

Usage:
    python3 -m totp current <username>

Implemented in stdlib only (hmac + struct + base64) so the workstation
image needs no extra pip install beyond boto3, which is already required
by pool.py / gh_auth.py.
"""

import base64
import hashlib
import hmac
import json
import os
import struct
import sys
import time

import boto3

REGION = os.environ.get("AWS_REGION", "us-east-1")
SECRET_PREFIX = os.environ.get("POOL_SECRET_PREFIX", "gh-copilot-workshop")


def _resolve_secret(sm, secret_id: str) -> str:
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


def totp(secret_b32: str, *, now: int | None = None, step: int = 30, digits: int = 6) -> str:
    if now is None:
        now = int(time.time())
    counter = now // step
    key = base64.b32decode(secret_b32.replace(" ", "").upper(), casefold=True)
    digest = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (
        (digest[offset] & 0x7F) << 24
        | (digest[offset + 1] & 0xFF) << 16
        | (digest[offset + 2] & 0xFF) << 8
        | (digest[offset + 3] & 0xFF)
    )
    return str(code % (10 ** digits)).zfill(digits)


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] != "current":
        sys.exit("usage: python3 -m totp current <username>")
    username = sys.argv[2]
    sm = boto3.client("secretsmanager", region_name=REGION)
    seed = _resolve_secret(sm, f"{SECRET_PREFIX}/{username}/totp-seed")
    print(totp(seed))


if __name__ == "__main__":
    main()
