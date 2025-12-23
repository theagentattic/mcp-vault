# Quick Test Guide

Fast reference for running tests and CI/CD.

## Run Tests Locally

```bash
# 1. Navigate to MCP server directory
cd packages/mcp-server

# 2. Install with dev dependencies
pip install -e ".[dev]"

# 3. Run all tests
pytest

# 4. Run with coverage
pytest --cov=claude_vault_mcp --cov-report=term

# 5. Run specific test file
pytest tests/test_tokenization.py -v

# 6. Run one specific test
pytest tests/test_security.py::TestSecurityValidator::test_validate_service_name_valid -v
```

## What Gets Tested

| Module | Tests | What It Checks |
|--------|-------|----------------|
| **test_tokenization.py** | 10 | Secrets never leak, tokens work correctly |
| **test_security.py** | 12 | Injection attacks blocked, inputs validated |
| **test_vault_client.py** | 10 | Vault API works, errors handled |
| **test_file_parsers.py** | 12 | .env and docker-compose parsing |
| **TOTAL** | **44** | Core security + functionality |

## CI/CD (Automatic on GitHub)

When you push code:

1. **Test Workflow** runs automatically:
   - Tests on Python 3.11 and 3.12
   - Coverage reporting
   - Takes ~2 minutes

2. **Security Workflow** runs:
   - Bandit security scan
   - Dependency vulnerability check
   - Takes ~1 minute

3. **Badges update** in README:
   - [![Tests](badge.svg)](link) - Green if passing
   - [![Security](badge.svg)](link) - Green if no issues

## Check CI/CD Status

```bash
# View workflows on GitHub
open https://github.com/weber8thomas/mcp-vault/actions

# Or use gh CLI
gh workflow list
gh run list
gh run view <run-id>
```

## Fix Failing Tests

```bash
# Run tests to see failures
pytest -v

# Run with more detail
pytest -vv

# Stop on first failure
pytest -x

# Run only failed tests from last run
pytest --lf
```

## Add New Test

```python
# In appropriate test file (e.g., tests/test_security.py)

def test_my_new_feature():
    """Test description - be specific."""
    # Arrange
    validator = SecurityValidator()

    # Act
    result = validator.my_method("input")

    # Assert
    assert result == expected_value
```

## Common Issues

### "ModuleNotFoundError: No module named 'claude_vault_mcp'"

**Fix:** Install package first:
```bash
cd packages/mcp-server
pip install -e ".[dev]"
```

### "externally-managed-environment"

**Fix:** Use virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows
pip install -e ".[dev]"
```

### Tests pass locally but fail in CI

**Fix:** Check Python version:
```bash
python --version  # Should be 3.11 or 3.12
```

## Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=claude_vault_mcp --cov-report=html

# View report
open htmlcov/index.html  # Mac
# or: xdg-open htmlcov/index.html  # Linux
# or: start htmlcov/index.html  # Windows
```

## Security Scan (Local)

```bash
# Install security tools
pip install bandit safety

# Run Bandit
bandit -r src/

# Check dependencies
safety check
```

## That's It!

For more details:
- See `packages/mcp-server/tests/README.md`
- See `IMPLEMENTATION_SUMMARY.md`
- See `PROJECT_GAPS_ANALYSIS.md`
