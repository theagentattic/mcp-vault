# Screenshots - Documentation Status

✅ All screenshots have been added and integrated into documentation!

## Completed Screenshots

### ✅ 1. `home-page.png` (2.0M)
- **Used in**: `mcp_vault/WEBAUTHN_SETUP.md`
- **Shows**: Server status, pending operations, registered devices
- **Status**: ✅ Added and documented

### ✅ 2. `approval-page.png` (2.6M)
- **Used in**: `mcp_vault/WEBAUTHN_SETUP.md`
- **Shows**: Approval page with service details and secrets preview
- **Status**: ✅ Added and documented

### ✅ 3. `approval-page-touchid.png` (3.1M)
- **Used in**: `mcp_vault/WEBAUTHN_SETUP.md`
- **Shows**: TouchID authentication prompt during approval
- **Status**: ✅ Added and documented

### ✅ 4. `approval-page-success.png` (2.7M)
- **Used in**: `mcp_vault/WEBAUTHN_SETUP.md`
- **Shows**: Success message after approval
- **Status**: ✅ Added and documented

### ✅ 5. `prompt.png` (114K)
- **Used in**: `docs/MCP.md`
- **Shows**: Claude Code using vault_set tool with MCP
- **Status**: ✅ Added and documented

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
