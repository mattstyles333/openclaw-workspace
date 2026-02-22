---
name: 1password
description: 1Password CLI (op) with service account authentication for accessing secrets, vaults, and items programmatically.
allowed-tools: Bash(op:*)
---

# 1Password CLI Service Account

This skill provides access to 1Password using a service account token for programmatic access to vaults and secrets.

## Prerequisites

- `op` CLI installed (`/usr/bin/op` v2.32.1)
- `OP_SERVICE_ACCOUNT_TOKEN` environment variable set (configured in `~/.bashrc` and `~/.profile`)

## Authentication

The service account token is automatically loaded from the environment. No manual sign-in required.

## Vaults

Current accessible vault:
- **claw** (ID: ni2ptgvtcu43a52xwnfaquwjp4)

## Common Commands

### Vault Operations

```bash
# List all vaults
op vault list

# Get vault details
op vault get claw
```

### Item Operations

```bash
# List items in the claw vault
op item list --vault claw

# Get a specific item
op item get "Spex4less" --vault claw
op item get "www.smartclubcloud.com" --vault claw

# Read a specific field
op read "op://claw/Spex4less/password"
```

### Read Secrets

```bash
# Read a secret URI
op read "op://vault/item/field"

# Examples:
op read "op://claw/Spex4less/username"
op read "op://claw/Spex4less/password"
op read "op://claw/www.smartclubcloud.com/password"
```

### Using with Environment Variables

```bash
# Export secrets as environment variables
export S4L_PASSWORD=$(op read "op://claw/Spex4less/password")
export SMARTCLUB_PASSWORD=$(op read "op://claw/www.smartclubcloud.com/password")
```

### Run Commands with Secrets

```bash
# Run a command with secrets injected from a file
cat > /tmp/env.txt << 'EOF'
DB_PASSWORD=op://claw/Spex4less/password
EOF
op run --env-file=/tmp/env.txt -- printenv DB_PASSWORD
```

### JSON Output for Scripting

```bash
# Get item details as JSON
op item get "Spex4less" --vault claw --format json

# Extract specific fields
op item get "Spex4less" --vault claw --format json | jq -r '.fields[] | select(.label=="password") | .value'
```

## Security Notes

- Service accounts have limited permissions - only the "claw" vault is accessible
- Use `op read` and `op run` to avoid writing secrets to disk
- Never log or display secrets in plaintext
