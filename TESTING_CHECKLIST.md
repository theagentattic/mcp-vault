# Testing Checklist

## Before Publishing v1.4.1

### 1. MCP Server Testing

#### Installation
- [ ] Fresh install: `pip install mcp-vault`
- [ ] Verify version: `pip show mcp-vault` (should show 1.4.1)
- [ ] Test uvx: `uvx --from mcp-vault vault-approve-server --help`

#### Approval Server
- [ ] Start server: `vault-approve-server`
- [ ] Access UI: http://localhost:8091
- [ ] Register WebAuthn device (TouchID/YubiKey)
- [ ] Verify "Manage Authenticators" shows your device

#### MCP Client Integration (Claude Code)
- [ ] Configure `.mcp.json` with new package name (`mcp-vault`)
- [ ] Restart Claude Code to load MCP server
- [ ] Test: "Check my Vault session status" → should call `vault_status`
- [ ] Test: "List my services in Vault" → should call `vault_list`

#### Tokenization Flow
- [ ] Create test `.env` file with secrets
- [ ] Ask AI: "Scan this .env and show me the secrets"
- [ ] Verify AI sees `@token-xxx` not real values
- [ ] Check approval UI shows real values
- [ ] Approve with WebAuthn
- [ ] Verify secrets registered in Vault

### 2. CLI Testing

#### Installation
- [ ] Install CLI (if using standalone): `sudo ./install.sh`
- [ ] Verify: `vault-session --help`
- [ ] Check version: `vault-session --version`

#### Authentication
- [ ] Login: `source vault-session login`
- [ ] OIDC browser opens and authenticates
- [ ] Verify: `vault-session status` shows active session
- [ ] Check env vars: `echo $VAULT_TOKEN` (should be set)

#### Secret Operations
- [ ] List services: `vault-session list`
- [ ] Get secrets: `vault-session get <service>`
- [ ] Register secret: `vault-session set test-app KEY=value`
- [ ] Verify confirmation prompt appears
- [ ] Inject to .env: `vault-session inject <service>`
- [ ] Logout: `vault-session logout`

### 3. Cross-Platform Testing (if possible)

- [ ] **Linux**: All features work
- [ ] **macOS**: WebAuthn with TouchID works
- [ ] **Windows**: WebAuthn with Windows Hello works

### 4. Multi-AI Client Testing (bonus)

- [ ] Test with Claude Code ✓
- [ ] Test with Claude Desktop (same `.mcp.json`)
- [ ] Test with other MCP client (Gemini CLI, BoltAI, etc.)

### 5. Documentation Accuracy

- [ ] All commands in README.md run successfully
- [ ] Installation instructions work on fresh system
- [ ] Examples produce expected output
- [ ] Links are not broken (check with `markdown-link-check`)

### 6. Security Validation

- [ ] Secrets never appear in Claude Code chat history
- [ ] Tokens (`@token-xxx`) visible in AI responses, not real values
- [ ] Approval required for all write operations
- [ ] Audit log created at `~/.mcp-vault/audit.log`
- [ ] Operations logged with timestamps

---

## Post-Publication Testing

### PyPI Package
- [ ] Package published: https://pypi.org/project/mcp-vault/
- [ ] Version 1.4.1 available
- [ ] Fresh install works: `pip install mcp-vault`
- [ ] Dependencies install correctly

### GitHub Release
- [ ] Release created: https://github.com/weber8thomas/mcp-vault/releases/tag/v1.4.1
- [ ] Release notes accurate
- [ ] Assets attached (if applicable)

### MCP Directories
- [ ] Submitted to Smithery.ai
- [ ] Submitted PR to awesome-mcp-servers
- [ ] Submitted to mcp.so

---

## Known Issues to Document

- [ ] List any known limitations
- [ ] Document workarounds
- [ ] Create GitHub issues for bugs

---

## Performance Testing (optional)

- [ ] Large .env file (100+ secrets): scans in <5s
- [ ] Approval server handles 10+ concurrent approvals
- [ ] Token cache doesn't leak memory over time
- [ ] MCP server responds within 1s for reads
