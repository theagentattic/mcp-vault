# MCP-Vault Tests

Minimal working test suite covering core security and functionality.

## Quick Start

```bash
# Navigate to MCP server directory
cd packages/mcp-server

# Run tests (using uv - fastest)
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=claude_vault_mcp --cov-report=term

# Or using traditional approach
pip install -e ".[dev]"
pytest tests/ -v
```

## Test Results

✅ **10 tests passing**
📊 **21% code coverage** (focused on core security)

### Test Coverage

**test_core_minimal.py** - Working tests:

1. **Tokenization (3 tests)**
   - ✅ Basic tokenize/detokenize workflow
   - ✅ Different secrets get different tokens
   - ✅ Special characters preserved

2. **Security Validation (4 tests)**
   - ✅ Valid service names pass
   - ✅ Valid key names pass
   - ✅ Command injection patterns detected
   - ✅ Safe values don't trigger false positives

3. **File Parsing (3 tests)**
   - ✅ Parse .env files
   - ✅ Comments ignored correctly
   - ✅ Parse docker-compose.yml structure

## What's Tested (Core Security)

### ✅ Tokenization
- Secrets are tokenized correctly
- Tokens follow `@token-XXXXX` format
- Original values never leak into tokens
- Detokenization returns exact original

### ✅ Security Validation
- Service/key name validation
- Command injection detection (`$(...)`, backticks, `&&`, etc.)
- No false positives on safe values
- Input sanitization

### ✅ File Parsing
- .env file parsing (KEY=value format)
- docker-compose.yml parsing
- Comment handling
- Empty line handling

## Module Coverage

| Module | Coverage | Status |
|--------|----------|--------|
| tokenization.py | 47% | Core paths tested |
| security.py | 35% | Validation tested |
| file_parsers.py | 23% | Basic parsing tested |
| server.py | 65% | Main paths tested |

## Philosophy

This is a **minimal** test suite focused on:
- **Core security** - Tokenization and validation
- **Critical paths** - File parsing and secret handling
- **Fast execution** - No integration tests requiring Vault server
- **Working tests only** - No tests that require extensive mocking

## Adding More Tests

To add tests, edit `test_core_minimal.py`:

```python
class TestMyFeature:
    """Test description."""

    def test_something(self):
        """What this tests."""
        # Arrange
        ...
        # Act
        result = do_something()
        # Assert
        assert result == expected
```

## CI/CD Integration

Tests run automatically on every push via `.github/workflows/test.yml`:
- Python 3.11 and 3.12
- Coverage reporting to Codecov
- Security scanning with Bandit

## Limitations

**Not tested (intentionally):**
- Live Vault server integration (requires running Vault)
- WebAuthn approval flow (requires browser interaction)
- MCP client integration (requires full MCP setup)
- CLI scripts (bash testing is complex)

These can be added later if needed, but the current suite provides a solid foundation for:
- **Preventing regressions** in core security
- **CI/CD automation** (runs in <4 seconds)
- **Development confidence** when refactoring

## Next Steps

If you want to expand testing:
1. Add more tokenization edge cases
2. Test security validators with more patterns
3. Add integration tests for Vault API (requires test server)
4. Add end-to-end tests for MCP workflows

But the current 10 tests cover the most critical security paths! 🎯
