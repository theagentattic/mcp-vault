# Claude-Vault CLI

Bash CLI scripts for session-based HashiCorp Vault management.

## Overview

The Claude-Vault CLI provides secure, session-based access to HashiCorp Vault with:
- **OIDC + MFA authentication** with 60-minute token expiry
- **Zero persistent credentials** - tokens stored only in memory
- **Comprehensive audit logging** - complete operation trail
- **Input validation** - prevents path traversal and command injection
- **Service-oriented design** - optimized for managing Docker service secrets

## Installation

### Quick Install (Recommended)

```bash
# Install latest release
curl -fsSL https://github.com/weber8thomas/claude-vault/releases/latest/download/install.sh | sudo bash

# Or install to ~/.local/bin (no sudo)
curl -fsSL https://github.com/weber8thomas/claude-vault/releases/latest/download/install.sh | PREFIX="$HOME/.local/bin" bash
```

### Manual Installation

```bash
git clone https://github.com/weber8thomas/claude-vault.git
cd claude-vault
sudo ./install.sh
```

## Usage

### Authentication

```bash
# Login (starts 60-minute session)
source claude-vault login

# Check session status
claude-vault status

# Logout (revoke token)
source claude-vault logout
```

### Managing Secrets

```bash
# List all services
claude-vault list

# List secrets for a service
claude-vault list jellyfin

# Get secret values
claude-vault get jellyfin

# Set secrets (interactive mode)
claude-vault set myapp KEY=value ANOTHER_KEY=value

# Inject secrets to .env file
claude-vault inject jellyfin
# Creates: jellyfin/.env with secrets from Vault
```

## Available Commands

| Command | Description |
|---------|-------------|
| `login` | Authenticate via OIDC + MFA (60-min session) |
| `status` | Check current session status |
| `logout` | Revoke session token |
| `list [service]` | List all services or secrets in a service |
| `get <service>` | Retrieve secret values for a service |
| `set <service> KEY=val...` | Create/update secrets for a service |
| `inject <service>` | Generate `.env` file from Vault secrets |

## Architecture

### Session Management

- Tokens stored in `$VAULT_TOKEN` environment variable (memory only)
- 60-minute expiry enforced by Vault
- Must use `source claude-vault login` to persist token in current shell

### Secret Organization

Secrets are organized by service name in Vault's KV v2 engine:

```
kv/data/
├── jellyfin/
│   ├── API_KEY
│   └── DB_PASSWORD
├── authentik/
│   ├── SECRET_KEY
│   └── POSTGRES_PASSWORD
└── ...
```

### Audit Logging

All operations are logged to `.claude-vault-audit.log`:

```
[2024-01-15 10:30:00] vault_get: service=jellyfin user=admin@example.com
[2024-01-15 10:35:00] vault_set: service=myapp keys=API_KEY,DB_PASSWORD user=admin@example.com
```

## Security Features

- **Input validation** - Prevents path traversal (`../`) and command injection
- **Token expiry** - Automatic 60-minute session timeout
- **Audit trail** - Complete log of all operations
- **No persistent credentials** - Tokens never written to disk
- **OIDC + MFA** - Strong authentication required

## AI Integration

For AI-assisted secret management, use the **MCP Server** component:
- See [../mcp-server/README.md](../mcp-server/README.md)
- Adds WebAuthn approval workflow for AI write operations
- Provides Claude Code with Vault tool access

## Troubleshooting

### "No active Vault session"

**Solution:** Login first with `source claude-vault login`

### "Permission denied"

**Causes:**
1. Session expired (60-min timeout)
2. Insufficient Vault permissions

**Solution:** Re-authenticate with `source claude-vault login`

### "Command not found"

**Cause:** Installation directory not in PATH

**Solution:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$PATH:/usr/local/bin"  # Or wherever installed
```

## Development

### Project Structure

```
packages/cli/
├── claude-vault              # Main CLI entry point
├── claude-vault-get.sh       # Get secrets implementation
├── claude-vault-list.sh      # List services/secrets
├── claude-vault-register.sh  # Set secrets implementation
└── inject-secrets.sh         # .env file generation
```

### Adding New Commands

1. Create `claude-vault-<command>.sh` script
2. Add command handler in `claude-vault` main script
3. Update this README with usage example

## See Also

- [Main README](../../README.md) - Project overview
- [MCP Server](../mcp-server/README.md) - AI integration
- [Setup Guide](../../docs/SETUP.md) - Complete installation guide
