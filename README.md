# Claude-Vault

Session-based CLI for HashiCorp Vault with AI assistant integration.

## Features

• Session-based authentication via OIDC + MFA (60-minute token expiry)
• No persistent credentials (tokens stored only in memory)
• Manual confirmation checkpoints (protection against prompt injection)
• Comprehensive audit logging (complete operation trail)
• Input validation (prevents path traversal and command injection)
• AI assistant friendly (designed for Claude Code integration)

## Quick Start

### Installation

**Quick install (recommended):**
```bash
# Install latest release
curl -fsSL https://github.com/weber8thomas/claude-vault/releases/latest/download/install.sh | sudo bash

# Or install to ~/.local/bin (no sudo)
curl -fsSL https://github.com/weber8thomas/claude-vault/releases/latest/download/install.sh | PREFIX="$HOME/.local/bin" bash
```

**Install specific version:**
```bash
VERSION="v1.0.0"
curl -fsSL "https://github.com/weber8thomas/claude-vault/releases/download/${VERSION}/install.sh" | sudo bash
```

**Manual installation:**
```bash
# Clone from source
git clone https://github.com/weber8thomas/claude-vault.git
cd claude-vault
sudo ./install.sh
```

### Authentication
```bash
source claude-vault login
```

### Usage
```bash
claude-vault list                  # List all services
claude-vault get esphome           # Get secret values
claude-vault set myapp KEY=val     # Register secrets
claude-vault inject authentik      # Inject to .env file
```

## Documentation

- [Setup Guide](docs/SETUP.md) - Complete installation and configuration
- [Quick Start](docs/QUICK_START.md) - AI assistant reference
- [MCP Integration](docs/MCP.md) - Model Context Protocol server setup

## Commands

- `login` - Authenticate via OIDC
- `status` - Check session status
- `logout` - Revoke token
- `list` - List services/secrets
- `get` - Get secret values
- `set` - Create/update secrets
- `inject` - Inject secrets to .env file

## MCP Server

This repository also includes an MCP (Model Context Protocol) server for Vault integration with Claude Code. See [mcp_vault/](mcp_vault/) for details.

## Releases

Releases are automatically created when new version tags are pushed. Each release includes:

- `install.sh` - Standalone installer (downloads latest from GitHub)
- `claude-vault-vX.X.X-linux-amd64.tar.gz` - Full tarball archive
- `claude-vault-vX.X.X-linux-amd64.zip` - Full ZIP archive
- `checksums.txt` - SHA256 checksums for verification

**One-command installation from release:**
```bash
curl -fsSL https://github.com/weber8thomas/claude-vault/releases/latest/download/install.sh | sudo bash
```

**To create a new release:**
```bash
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0
```

GitHub Actions will automatically build and publish the release.
