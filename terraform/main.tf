terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# ---------- Variables ----------

variable "account_id" {
  description = "AWS account ID where the role will be created"
  type        = string
}

variable "gcp_azp" {
  description = "The azp (authorized party) claim from the GCP service account JWT. Maps to accounts.google.com:aud."
  type        = string
}

variable "gcp_aud" {
  description = "The aud (audience) claim from the GCP JWT — the audience string you pass when requesting the token. Maps to accounts.google.com:oaud."
  type        = string
}

variable "gcp_sub" {
  description = "The sub (subject) claim from the GCP service account JWT — the numeric service account ID. Maps to accounts.google.com:sub."
  type        = string
}

# ---------- Role with trust policy ----------

data "aws_iam_policy_document" "trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = ["accounts.google.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "accounts.google.com:aud"
      values   = [var.gcp_azp]
    }

    condition {
      test     = "StringEquals"
      variable = "accounts.google.com:oaud"
      values   = [var.gcp_aud]
    }

    condition {
      test     = "StringEquals"
      variable = "accounts.google.com:sub"
      values   = [var.gcp_sub]
    }
  }
}

resource "aws_iam_role" "instruqt" {
  name                 = "InstruqtGitHubCopilotPoolRole"
  assume_role_policy   = data.aws_iam_policy_document.trust.json
  max_session_duration = 3600
}

# ---------- Pool runtime (DynamoDB + Secrets Manager) ----------
#
# The Instruqt workstation's lib/{pool,gh_auth,totp}.py scripts need exactly
# three permission slices to drive the GitHub-account pool checkout:
#   - dynamodb:Query / UpdateItem on the pool table + its two GSIs
#   - secretsmanager:GetSecretValue on every gh-copilot-workshop/* secret
#     (password, refresh-token, totp-seed, app/client-id, app/client-secret)
#   - secretsmanager:PutSecretValue on refresh-token secrets only, since
#     GitHub App refresh tokens are single-use and must be persisted on rotation

data "aws_iam_policy_document" "pool_runtime" {
  statement {
    sid    = "PoolCheckout"
    effect = "Allow"
    actions = [
      "dynamodb:Query",
      "dynamodb:UpdateItem",
    ]
    resources = [
      "arn:aws:dynamodb:us-east-1:${var.account_id}:table/gh-copilot-workshop-users",
      "arn:aws:dynamodb:us-east-1:${var.account_id}:table/gh-copilot-workshop-users/index/*",
    ]
  }

  statement {
    sid    = "ReadPoolSecrets"
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue",
    ]
    resources = [
      "arn:aws:secretsmanager:us-east-1:${var.account_id}:secret:gh-copilot-workshop/*",
    ]
  }

  statement {
    sid    = "RotateRefreshTokens"
    effect = "Allow"
    actions = [
      "secretsmanager:PutSecretValue",
    ]
    resources = [
      "arn:aws:secretsmanager:us-east-1:${var.account_id}:secret:gh-copilot-workshop/*/refresh-token-*",
    ]
  }
}

resource "aws_iam_role_policy" "pool_runtime" {
  name   = "PoolRuntimeAccess"
  role   = aws_iam_role.instruqt.id
  policy = data.aws_iam_policy_document.pool_runtime.json
}

# ---------- Output ----------

output "role_arn" {
  description = "ARN to plug into /opt/bin/credentials.sh on the GCP VM"
  value       = aws_iam_role.instruqt.arn
}
