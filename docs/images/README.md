# Documentation Images

This directory contains screenshots and images for the Claude-Vault documentation.

## Guidelines

- **Format**: Use PNG for UI screenshots (better quality than JPEG)
- **Compression**: Compress images to keep file size under 500KB
- **Naming**: Use descriptive names with hyphens (e.g., `approval-page-success.png`)
- **Optimization**: Run `optipng` or similar tools before committing

## Tools for Optimization

```bash
# Install optipng (optional)
apt-get install optipng  # Ubuntu/Debian
brew install optipng     # macOS

# Optimize a PNG
optipng -o7 screenshot.png
```

## Current Images

- `home-page.png` - Main approval server home page
- `registration-page.png` - WebAuthn registration interface
- `approval-page.png` - Vault operation approval interface
- `approval-success.png` - Success message after approval

## Size Limits

Pre-commit hooks will warn if images exceed 1MB. Keep screenshots reasonable:
- Full page: ~200-500KB
- Cropped UI: ~50-200KB
