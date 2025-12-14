# Screenshots Needed

Please capture the following screenshots and save them to this directory:

## Required Screenshots

### 1. `home-page.png`
- **URL**: http://localhost:8091 or https://vault-approve.laboiteaframboises.duckdns.org/
- **What to capture**: Full page showing server status, pending operations count, registered devices
- **State**: After registration is complete (so it shows "Setup Complete")
- **Recommended size**: ~400-600KB (compress if larger)

### 2. `registration-page.png`
- **URL**: http://localhost:8091/register or https://vault-approve.laboiteaframboises.duckdns.org/register
- **What to capture**: The registration interface before clicking the button
- **Shows**: Purple gradient header, "Register Authenticator" button, info boxes
- **Recommended size**: ~400-600KB

### 3. `approval-page.png`
- **URL**: Open any approval URL (create a test vault_set operation to get one)
- **What to capture**: The approval page showing:
  - Service name
  - Vault path
  - Secrets table with preview
  - "Approve with WebAuthn" and "Deny" buttons
- **State**: Before clicking approve
- **Recommended size**: ~400-600KB

### 4. `approval-success.png`
- **URL**: Same as approval page, but after successful authentication
- **What to capture**: Success message showing:
  - Green checkmark ✅
  - "Operation approved!" message
  - "Secrets have been approved and written to Claude-Vault"
  - "Return to home" link
- **Recommended size**: ~400-600KB

## How to Capture

### macOS
```bash
# Full window: Cmd+Shift+4, then press Space, click window
# Or use built-in Screenshot app
```

### Windows
```bash
# Windows+Shift+S for Snipping Tool
# Or use Snip & Sketch
```

### Linux
```bash
# Use Flameshot, GNOME Screenshot, or similar
```

## After Capturing

1. Save screenshots to this directory (`/workspace/claude-vault/docs/images/`)
2. Optimize them (optional):
   ```bash
   optipng -o7 *.png
   # or
   pngquant --quality 80-95 *.png
   ```
3. Commit them:
   ```bash
   cd /workspace/claude-vault
   git add docs/images/*.png
   git commit -m "docs: Add UI screenshots to documentation"
   git push
   ```

The documentation already has placeholder references to these images, so they'll appear automatically once you add them!
