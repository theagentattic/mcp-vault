# Screenshot TODO List

Based on the recent documentation updates, here are the screenshots needed for complete documentation.

## 🔴 High Priority (Core Workflow)

### 1. **Approval Server Home Page** ✅ EXISTS
**File:** `docs/images/home-page.png`
**Location:** README.md (line ~87)
**Status:** Update recommended
**Details:**
- Should show: Server status, pending operations count, registered devices
- Update to show: Operation history section (new feature)
- Should be provider-agnostic (no "Claude" branding visible)

### 2. **Approval Page - Review Operation** ✅ EXISTS
**File:** `docs/images/approval-page.png`
**Location:** README.md (line ~91)
**Status:** Update recommended
**Details:**
- Should show: Service name, operation type, secrets preview
- Update to show: Operation expires in X minutes (countdown)
- Should use localhost URL in browser bar (not domain)

### 3. **TouchID/Biometric Prompt** ✅ EXISTS
**File:** `docs/images/approval-page-touchid.png`
**Location:** README.md (line ~98)
**Status:** Good as-is
**Details:**
- Shows: Native TouchID/Windows Hello prompt
- Note: This is OS-specific, current one is fine

### 4. **Success Page After Approval** ✅ EXISTS
**File:** `docs/images/approval-page-success.png`
**Location:** README.md (line ~103)
**Status:** Update recommended
**Details:**
- Should show: Success message, operation ID, redirect countdown
- Update to show: "Redirecting to home in 3 seconds..."
- Should show localhost URL (not domain)

## 🟡 Medium Priority (New Features)

### 5. **WebAuthn Registration Page** 🆕 NEEDED
**File:** `docs/images/registration-page.png`
**Location:** WEBAUTHN_SETUP.md
**Details:**
- URL: http://localhost:8091/register
- Should show: Device name input field, "Register Authenticator" button
- Should show: Supported authenticators list (TouchID, Windows Hello, YubiKey)
- Browser should show localhost:8091 in address bar

### 6. **Registration Success** 🆕 NEEDED
**File:** `docs/images/registration-success.png`
**Location:** WEBAUTHN_SETUP.md
**Details:**
- Should show: "✅ Authenticator registered successfully!"
- Should show: Link back to home page
- Should show registered device info

### 7. **Operation History View** 🆕 NEEDED
**File:** `docs/images/operation-history.png`
**Location:** README.md, WEBAUTHN_SETUP.md
**Details:**
- URL: http://localhost:8091/
- Should show: Table of completed operations
- Columns: Service, Action, Secrets count, Status, Completed time, Age
- Should show clickable rows
- Show "Last 100 completed operations" subtitle

### 8. **Operation Details Modal** 🆕 NEEDED
**File:** `docs/images/operation-details-modal.png`
**Location:** WEBAUTHN_SETUP.md
**Details:**
- Triggered by: Clicking a row in operation history
- Should show: Full operation details, timeline, approval info
- Should show: Device used for approval
- Should show: All secrets (not truncated)

## 🟢 Low Priority (Configuration & Testing)

### 9. **MCP Client Configuration** 🆕 NEEDED
**File:** `docs/images/mcp-config.png`
**Location:** docs/MCP.md
**Details:**
- Show: Claude Desktop settings or .mcp.json file
- Should show: mcp-vault configuration
- Should show: Environment variables section
- Highlight: VAULT_ADDR, VAULT_TOKEN, VAULT_SECURITY_MODE

### 10. **Terminal - Approval Server Auto-Start** 🆕 NEEDED
**File:** `docs/images/terminal-autostart.png`
**Location:** README.md, docs/TESTING.md
**Details:**
- Show: Terminal output when MCP server starts
- Should show: "✅ Approval server started on http://localhost:8091"
- Should be first time MCP server runs (auto-start message)

### 11. **Terminal - Environment Variable Check** 🆕 NEEDED
**File:** `docs/images/terminal-env-check.png`
**Location:** docs/TESTING.md
**Details:**
- Show: Output of `env | grep VAULT_APPROVE`
- Two examples:
  - a) No variables set (local development)
  - b) Variables set (production mode)

### 12. **Terminal - Test Script Output** 🆕 NEEDED
**File:** `docs/images/terminal-test-script.png`
**Location:** docs/TESTING.md
**Details:**
- Show: Running the test script from TESTING.md
- Should show: All green checkmarks
- Should show: Approval URL with localhost

### 13. **Browser - Pending Operations Table** 🆕 NEEDED
**File:** `docs/images/pending-operations.png`
**Location:** README.md
**Details:**
- URL: http://localhost:8091/
- Should show: Pending operations section
- Columns: Service, Action, Secrets, Status, Created, Age, Actions
- Should show "Pending" badge for unapproved operations
- Should show "View →" link

### 14. **Browser - Registered Devices Table** 🆕 NEEDED
**File:** `docs/images/registered-devices.png`
**Location:** WEBAUTHN_SETUP.md
**Details:**
- URL: http://localhost:8091/
- Should show: Registered devices table
- Columns: Device Name, Credential ID, Status, Registered
- Should show device name like "MacBook Pro", "My YubiKey", etc.
- Should show "Active" badge

## 🔵 Optional (Edge Cases & Error States)

### 15. **Error - No Registered Authenticator** 🆕 NEEDED
**File:** `docs/images/error-no-authenticator.png`
**Location:** WEBAUTHN_SETUP.md
**Details:**
- Show: Error message when trying to approve without registered device
- Should show: "No registered authenticator. Please register first."
- Should show: Link to /register

### 16. **Error - Operation Expired** 🆕 NEEDED
**File:** `docs/images/error-expired.png`
**Location:** WEBAUTHN_SETUP.md
**Details:**
- Show: Error when opening approval URL after 5 minutes
- Should show: "Operation expired (max 5 minutes)"
- Should show: Instruction to create new operation

### 17. **Production Mode - HTTPS URL** 🆕 NEEDED
**File:** `docs/images/production-https-url.png`
**Location:** WEBAUTHN_SETUP.md (Production Deployment section)
**Details:**
- Show: Browser with HTTPS URL
- URL: https://vault-approve.yourdomain.com/approve/...
- Should show: SSL padlock in browser
- Should show same approval page but with HTTPS

### 18. **AI Assistant Output - Approval URL** 🆕 NEEDED
**File:** `docs/images/ai-approval-prompt.png`
**Location:** README.md
**Details:**
- Show: AI assistant (Claude/Gemini) output
- Should show: Tokenized preview
- Should show: "⚠️ SECURITY CHECKPOINT - WEBAUTHN APPROVAL REQUIRED"
- Should show: Full approval instructions with localhost URL
- Should NOT show specific AI branding (provider-agnostic)

## 📋 Screenshot Capture Guidelines

### Browser Screenshots
- **Resolution:** 1920x1080 or higher
- **Browser:** Chrome or Firefox (consistent UI)
- **Zoom:** 100% (default)
- **Window:** Full window, not just viewport
- **Cropping:** Include browser chrome (address bar, tabs) to show URL

### Terminal Screenshots
- **Terminal:** Use consistent terminal (iTerm2, Windows Terminal, etc.)
- **Theme:** Dark theme recommended for consistency
- **Font:** Monospace, readable size (14pt+)
- **Cropping:** Include prompt and command, trim unnecessary context

### Naming Convention
```
<category>-<description>.png

Examples:
approval-page.png
registration-success.png
terminal-autostart.png
error-no-authenticator.png
```

### Image Optimization
- **Format:** PNG (lossless)
- **Optimize:** Use `optipng` or similar to reduce file size
- **Max size:** Aim for < 500KB per screenshot

## 📍 Where Screenshots Are Used

```
docs/images/
├── home-page.png                    → README.md, WEBAUTHN_SETUP.md
├── approval-page.png                → README.md, WEBAUTHN_SETUP.md
├── approval-page-touchid.png        → README.md, WEBAUTHN_SETUP.md
├── approval-page-success.png        → README.md, WEBAUTHN_SETUP.md
├── registration-page.png            → WEBAUTHN_SETUP.md
├── registration-success.png         → WEBAUTHN_SETUP.md
├── operation-history.png            → README.md, WEBAUTHN_SETUP.md
├── operation-details-modal.png      → WEBAUTHN_SETUP.md
├── mcp-config.png                   → docs/MCP.md
├── terminal-autostart.png           → README.md, docs/TESTING.md
├── terminal-env-check.png           → docs/TESTING.md
├── terminal-test-script.png         → docs/TESTING.md
├── pending-operations.png           → README.md
├── registered-devices.png           → WEBAUTHN_SETUP.md
├── error-no-authenticator.png       → WEBAUTHN_SETUP.md
├── error-expired.png                → WEBAUTHN_SETUP.md
├── production-https-url.png         → WEBAUTHN_SETUP.md
└── ai-approval-prompt.png           → README.md
```

## ✅ Checklist for Each Screenshot

Before capturing, ensure:
- [ ] Environment variables are set correctly (local vs production)
- [ ] Browser is at correct URL (localhost or domain)
- [ ] No personal/sensitive data visible
- [ ] UI is in expected state
- [ ] Browser address bar is visible (shows URL)
- [ ] Screenshot is cropped appropriately
- [ ] Image is optimized for size
- [ ] File is named correctly
- [ ] Screenshot shows provider-agnostic content (no Claude branding)

## 🎯 Priority Order for Capture

1. **Week 1** - Update existing screenshots (1-4)
2. **Week 2** - Capture new core features (5-8)
3. **Week 3** - Configuration and testing (9-12)
4. **Week 4** - Edge cases and production (15-18)

## 📝 Notes

- All screenshots should reflect the **current localhost-by-default** configuration
- Screenshots showing URLs should use `http://localhost:8091` unless specifically demonstrating production mode
- Provider-agnostic: No AI provider branding (Claude, Gemini) in screenshots where possible
- Operation history is a new feature - needs comprehensive screenshots
- WebAuthn registration flow needs complete documentation
