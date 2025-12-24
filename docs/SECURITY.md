# Security Architecture

## Overview

MCP-Vault provides defense-in-depth security through multiple layers:
1. **Tokenization** - Secrets never sent to AI APIs
2. **WebAuthn Approval** - Human-in-the-loop for write operations
3. **Vault Integration** - Enterprise-grade secret storage
4. **Session Management** - Time-limited OIDC tokens

## How Tokenization Works

**Your secrets are NEVER sent to AI provider APIs:**

### 1. Scanning Phase (when AI needs to see secrets)
```
Original: DATABASE_PASSWORD="super_secret_123"
Sent to AI: DATABASE_PASSWORD="@token-a8f3d9e1b2c4"
```

- MCP server tokenizes values before sending to AI
- Tokens are temporary and session-specific (2 hour expiry)
- AI sees structure and keys, never actual secrets

### 2. Writing Phase (when AI wants to save secrets)
```
AI sends: vault_set(service="myapp", secrets={"KEY": "value"})
Your action: Review on http://localhost:8091 and approve with TouchID
Result: Only written to Vault after your biometric confirmation
```

## Security Model

| Operation | AI Sees | Human Approval | Notes |
|-----------|---------|----------------|-------|
| **List services** | Service names only | ❌ Not required | Safe metadata |
| **Read secrets** | Tokens like `@token-xxx` | ❌ Not required | Values stay in MCP server |
| **Write secrets** | Structure and keys | ✅ **WebAuthn required** | You review real values in browser |
| **Scan configs** | Tokens for detected secrets | ✅ **WebAuthn required** | Tokenization prevents leakage |
| **Inject to .env** | File path only | ❌ Not required | Real values injected locally |

## Trust Boundaries

```
┌──────────────────┐
│  AI Provider     │  ← Sees: Tokens, structure, metadata
│ (Claude/Gemini)  │     Never sees: Actual secret values
└────────┬─────────┘
         │ MCP Protocol
         │ (only tokens sent)
         │
┌────────▼─────────┐
│   MCP Server     │  ← Has: Full access to secrets
│ (Your Machine)   │     Enforces: WebAuthn approval for writes
└────────┬─────────┘
         │ Vault API
         │ (with your token)
         │
┌────────▼─────────┐
│  HashiCorp Vault │  ← Stores: All secrets encrypted
│ (Your Infra)     │     Access: Controlled by your OIDC/MFA
└──────────────────┘
```

## WebAuthn Approval Architecture

### Why WebAuthn?

**The Problem:** AI assistants have access to the `vault_set` tool and could write secrets to your production Vault. If an attacker tricks the AI through prompt injection, they could write malicious secrets without your knowledge.

**The Solution:** WebAuthn approval adds a human-in-the-loop checkpoint that AI cannot bypass:

```
┌─────────────────────────────────────────────────────────────────┐
│ Without Approval (UNSAFE)                                       │
├─────────────────────────────────────────────────────────────────┤
│  Attacker → AI Agent → vault_set() → Vault ✅ (secrets written) │
│  ⚠️ AI can be tricked via prompt injection!                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ With WebAuthn Approval (SECURE)                                 │
├─────────────────────────────────────────────────────────────────┤
│  Attacker → AI Agent → vault_set() → Pending Operation          │
│                      ↓                                           │
│  You review in browser → Touch TouchID → Operation Approved     │
│                      ↓                                           │
│  AI Agent → vault_set(approval_token) → Vault ✅                │
│  ✅ Human verification required - AI cannot bypass!             │
└─────────────────────────────────────────────────────────────────┘
```

### How Approval Works

The approval flow has three distinct phases:

```python
# Phase 1: Create Pending Operation (no approval_token)
vault_set(service="myapp", secrets={"KEY": "value"})
→ Creates operation in approval server memory
→ Returns approval URL: http://localhost:8091/approve/{op_id}
→ No secrets written to Vault yet ❌

# Phase 2: Human Approval (out-of-band, in browser)
User opens URL → Reviews secrets → Clicks "Approve"
→ WebAuthn challenge-response authentication
→ Private key in Secure Enclave signs challenge
→ Server verifies signature matches public key
→ Operation marked as approved in server memory ✅

# Phase 3: Execute (with approval_token = op_id)
vault_set(service="myapp", secrets={"KEY": "value"}, approval_token="abc123")
→ Checks if operation "abc123" exists and is approved
→ If yes: Write secrets to Vault ✅
→ If no: Reject with "Operation not approved" ❌
```

**The Approval Token is Just an Operation ID:**
- Format: Random 16-byte URL-safe string (e.g., `"a1b2c3d4e5f6g7h8"`)
- Generated by: `secrets.token_urlsafe(16)` in Python
- Storage: In-memory dict + JSON file (`~/.claude-vault/pending-operations.json`)
- Lifetime: 5 minutes (automatically expires)

## Threat Model

| Attack Vector | Defense Mechanism |
|---------------|-------------------|
| **Prompt injection** | WebAuthn approval shows real values to human |
| **API compromise** | Secrets tokenized, API only sees placeholders |
| **Token theft** | Tokens expire in 2 hours, session-specific |
| **Replay attacks** | Challenge nonces prevent signature reuse |
| **Stolen credentials file** | Only public keys stored, private keys in hardware |
| **AI tries to bypass MCP tool** | Tool code runs server-side, AI can only send params |
| **Attacker steals pending-operations.json** | File contains secrets, but can't approve without WebAuthn device |
| **Attacker steals approval token from logs** | Token useless after 5 minutes, and still needs WebAuthn |
| **Replay previous WebAuthn signature** | Challenge is single-use, signature won't verify |
| **Phishing: Fake approval page** | Origin binding prevents credentials from working on fake site |
| **Man-in-the-middle intercepts token** | Token alone insufficient, needs approved operation state |

## For Ultra-Sensitive Secrets

If you have secrets that should never be accessible to AI tooling at all:

### 1. Use CLI Directly
Bypass MCP server entirely:
```bash
source vault-session login
vault-session set prod-db MASTER_KEY="..."
```

### 2. Hybrid Approach
Let AI structure, you provide values:
```
AI: "I'll set up the Vault structure for your database service"
You: Manually provide sensitive values via CLI
```

### 3. Separate Vault Paths
Keep ultra-sensitive secrets in a different path that the MCP server can't access:
```bash
# MCP server only has access to: secret/proxmox-services/*
# Ultra-sensitive secrets in: secret/production/critical/*
```

## Data Storage Locations

### In `~/.claude-vault/webauthn-credentials.json`
- ✅ Credential ID (public, uniquely identifies the credential)
- ✅ Public key (public, used to verify signatures)
- ✅ Sign counter (public, prevents replay attacks)
- ✅ Device name (public, for UI display)
- ❌ **NO** private keys
- ❌ **NO** biometric data
- ✅ Safe to commit to git

### In `~/.claude-vault/pending-operations.json`
- Pending operations waiting for approval
- Operation ID, service name, secrets (in plaintext!)
- Approval status (approved: true/false)
- ⚠️ **Do NOT commit** - contains secrets before approval
- Auto-cleanup: Expires after 5 minutes

### In your device's Secure Enclave/TPM
- 🔐 Private key (never leaves device, never exported)
- 🔐 Biometric templates (TouchID/Windows Hello)
- 🔐 Hardware-bound, cannot be copied

### In approval server memory
- Pending operations (Dict[str, PendingOperation])
- WebAuthn challenges (single-use, expires after authentication)

## Security Best Practices

1. **Environment Variables**: Never commit `VAULT_TOKEN` or approval server URLs to git
2. **Token Rotation**: Re-authenticate with `vault-session login` before token expiry
3. **WebAuthn Registration**: Register authenticators in the same environment (local vs production)
4. **Approval Expiry**: Approve operations within 5 minutes or create a new one
5. **Network Security**: Use HTTPS for production approval server (nginx reverse proxy)
6. **Audit Trail**: Review operation history at http://localhost:8091

## Further Reading

- [WebAuthn Setup Guide](../packages/mcp-server/WEBAUTHN_SETUP.md) - Detailed setup and troubleshooting
- [MCP Integration](MCP.md) - Model Context Protocol configuration
- [CLI Setup](SETUP.md) - Direct Vault access without AI
