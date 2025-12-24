# Testing Guide

Quick guide for testing the MCP-Vault approval server and verifying configuration.

## Quick Approval Server Test

### 1. Check Environment Variables

First, verify your environment configuration:

```bash
echo "VAULT_APPROVE_DOMAIN: ${VAULT_APPROVE_DOMAIN:-(not set)}"
echo "VAULT_APPROVE_ORIGIN: ${VAULT_APPROVE_ORIGIN:-(not set)}"
```

**For local development:**
- Both should show `(not set)` - this uses localhost defaults
- If they're set to a domain, unset them: `unset VAULT_APPROVE_DOMAIN VAULT_APPROVE_ORIGIN`

**For production (nginx/HTTPS):**
- Should show your domain, e.g., `vault-approve.yourdomain.com`

### 2. Test Approval Server Starts

```bash
# Start the approval server
vault-approve-server
```

**Expected output:**
```
✅ Approval server started on http://localhost:8091
```

Open http://localhost:8091 in your browser. You should see the approval server home page.

### 3. Test Approval URL Generation

Create a test operation to verify URL generation:

```bash
cd /workspace/mcp-vault/packages/mcp-server

uv run python3 -c "
from src.claude_vault_mcp.approval_server import get_approval_server

server = get_approval_server()
op_id, approval_url = server.create_pending_operation(
    service='test-service',
    action='CREATE',
    secrets={'TEST_KEY': 'test-value'},
    warnings=[]
)

print(f'✅ Test Operation Created')
print(f'Operation ID: {op_id}')
print(f'Approval URL: {approval_url}')
print()

# Verify URL format
if 'localhost' in approval_url and 'http://' in approval_url:
    print('✅ SUCCESS: Using localhost for local development')
elif 'https://' in approval_url:
    print('✅ SUCCESS: Using HTTPS for production')
else:
    print('❌ WARNING: Unexpected URL format')
"
```

**Expected for local development:**
```
✅ Test Operation Created
Operation ID: abc123xyz...
Approval URL: http://localhost:8091/approve/abc123xyz...

✅ SUCCESS: Using localhost for local development
```

### 4. Test Approval Page

Open the approval URL from step 3 in your browser. You should see:
- Service name: `test-service`
- Action: `CREATE`
- Secrets table with `TEST_KEY`
- "Approve with WebAuthn" button

## Testing with MCP Client

### 1. Test with vault_set (No Vault Required)

Even without Vault authentication, you can test the approval flow:

```python
# In your MCP client (e.g., Claude Desktop)
vault_set(service="test-app", secrets={"API_KEY": "test123"})
```

**Expected response:**
```
⚠️  SECURITY CHECKPOINT - WEBAUTHN APPROVAL REQUIRED

To approve:
  1. Open in browser: http://localhost:8091/approve/{op_id}
  ...
```

**Verify:**
- ✅ Approval URL uses `http://localhost:8091` (not a domain)
- ✅ Opening the URL shows the approval page
- ✅ Page displays the test-app service and API_KEY

### 2. Register WebAuthn Device

Before you can approve operations:

1. Open http://localhost:8091/register
2. Enter a device name (e.g., "My Laptop")
3. Click "Register Authenticator"
4. Complete TouchID/Windows Hello authentication

**Expected:**
```
✅ Authenticator registered successfully!
You can now approve operations!
```

### 3. Full Approval Flow Test

```python
# Step 1: Create operation (returns approval URL)
vault_set(service="test-app", secrets={"KEY": "value"})

# Step 2: Open approval URL in browser, approve with WebAuthn

# Step 3: Execute with approval token
vault_set(
    service="test-app",
    secrets={"KEY": "value"},
    approval_token="abc123xyz"  # from URL
)
```

**Expected flow:**
1. First call: Returns approval URL
2. Browser: Shows secrets, you approve
3. Second call: Writes to Vault (or fails if no Vault auth)

## Troubleshooting Tests

### "Approval URLs use wrong domain"

**Problem:** URLs show `https://vault-approve.domain.com` instead of `localhost`

**Solution:**
```bash
# Check environment
env | grep VAULT_APPROVE

# If variables are set, unset them
unset VAULT_APPROVE_DOMAIN
unset VAULT_APPROVE_ORIGIN

# Restart MCP server
```

### "Approval server not responding"

**Check if it's running:**
```bash
curl http://localhost:8091/
```

**Check port is available:**
```bash
lsof -i :8091
```

**Start manually if needed:**
```bash
vault-approve-server
```

### "WebAuthn registration fails"

**Common causes:**
- Browser not supporting WebAuthn (use Chrome, Firefox, Safari, Edge)
- No biometric hardware available (use YubiKey instead)
- Wrong origin (check VAULT_APPROVE_ORIGIN matches browser URL)

**Test WebAuthn support:**
Open browser console on http://localhost:8091/register:
```javascript
if (window.PublicKeyCredential) {
    console.log("✅ WebAuthn supported");
} else {
    console.log("❌ WebAuthn not supported");
}
```

### "Operation expired"

Operations expire after 5 minutes. Create a new one:
```python
vault_set(service="test-app", secrets={"KEY": "value"})
# Approve within 5 minutes
```

## Environment Switching

### Switch to Production Mode

```bash
# Set production variables
export VAULT_APPROVE_DOMAIN="vault-approve.yourdomain.com"
export VAULT_APPROVE_ORIGIN="https://vault-approve.yourdomain.com"

# Restart MCP server
# Test: URLs should now use HTTPS domain
```

### Switch Back to Local Mode

```bash
# Unset production variables
unset VAULT_APPROVE_DOMAIN
unset VAULT_APPROVE_ORIGIN

# Restart MCP server
# Test: URLs should now use localhost
```

## Automated Test Script

Save this as `test-approval-server.sh`:

```bash
#!/bin/bash
set -e

echo "🧪 Testing MCP-Vault Approval Server"
echo "===================================="
echo ""

# Check environment
echo "1. Checking environment variables..."
if [ -z "$VAULT_APPROVE_DOMAIN" ] && [ -z "$VAULT_APPROVE_ORIGIN" ]; then
    echo "   ✅ Local mode (no env vars set)"
else
    echo "   📍 Production mode detected:"
    echo "      DOMAIN: ${VAULT_APPROVE_DOMAIN}"
    echo "      ORIGIN: ${VAULT_APPROVE_ORIGIN}"
fi
echo ""

# Check server is running
echo "2. Checking server status..."
if curl -s -f http://localhost:8091/ > /dev/null; then
    echo "   ✅ Approval server is running"
else
    echo "   ❌ Approval server not responding"
    echo "   Run: vault-approve-server"
    exit 1
fi
echo ""

# Create test operation
echo "3. Creating test operation..."
cd /workspace/mcp-vault/packages/mcp-server
TEST_OUTPUT=$(uv run python3 -c "
from src.claude_vault_mcp.approval_server import get_approval_server
server = get_approval_server()
op_id, url = server.create_pending_operation(
    service='test', action='CREATE', secrets={'KEY': 'val'}, warnings=[]
)
print(url)
" 2>/dev/null)

echo "   URL: $TEST_OUTPUT"

if [[ "$TEST_OUTPUT" == http://localhost:8091* ]]; then
    echo "   ✅ Using localhost (local mode)"
elif [[ "$TEST_OUTPUT" == https://* ]]; then
    echo "   ✅ Using HTTPS (production mode)"
else
    echo "   ❌ Unexpected URL format"
    exit 1
fi
echo ""

echo "✅ All tests passed!"
echo ""
echo "Next steps:"
echo "  1. Open: http://localhost:8091/register"
echo "  2. Register your WebAuthn device"
echo "  3. Try: vault_set(service='test', secrets={'KEY': 'val'})"
```

Make it executable and run:
```bash
chmod +x test-approval-server.sh
./test-approval-server.sh
```

## See Also

- [WebAuthn Setup](../packages/mcp-server/WEBAUTHN_SETUP.md) - Detailed WebAuthn configuration
- [Security Architecture](SECURITY.md) - How the approval system works
- [MCP Integration](MCP.md) - MCP client configuration
