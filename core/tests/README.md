# Smoke Tests

This directory contains smoke tests for the Lumina project. These tests validate critical code paths and ensure core functionality works correctly.

## Test Structure

```
core/tests/
├── fixtures/              # Test data
│   ├── sample.eml         # Valid test email
│   ├── invalid.eml        # Malformed email for error testing
│   └── sample_tasks.md    # Valid TASKS.md for parsing tests
├── test_email_converter.py    # Email conversion tests
├── test_task_detector.py      # Task dependency detector tests
├── test_scripts.sh            # Shell script validation tests
├── run_tests.sh               # Main test runner
└── README.md                  # This file
```

## Running Tests

### Run All Tests

```bash
./core/tests/run_tests.sh
```

### Run All Tests + Integration Tests

```bash
./core/tests/run_tests.sh --extended
```

### Run Individual Test Suites

**Shell Script Tests:**
```bash
./core/tests/test_scripts.sh
```

**Email Converter Tests:**
```bash
python3 core/tests/test_email_converter.py
```

**Notes Converter Tests:**
```bash
python3 core/tests/test_notes_converter.py
```

**Task Detector Tests:**
```bash
python3 core/tests/test_task_detector.py
```

**Notes Integration Tests:**
```bash
python3 core/tests/test_notes_integration.py
```

## Test Coverage

### Shell Script Tests (21 tests)
- Validates bash syntax for all core scripts
- Checks file existence and permissions
- Verifies template files are present

### Email Converter Tests (7 tests)
- Email structure validation
- Module import verification
- File processing capabilities
- Error handling for malformed input

### Notes Converter Tests (18 tests)
- Notes converter script validation
- Multi-format support verification (.txt, .md, .docx, .textbundle, .html)
- OneNote, Bear, Apple Notes sample data validation
- Parser functionality for each format
- Optional dependency checks (python-docx, html2text)
- File operations and directory handling

### Notes Converter Integration Tests (6 tests)
- End-to-end conversion workflow
- Multi-file processing validation
- Real sample data conversion (.txt, .md, .html)
- Directory creation and file management
- Empty directory handling

**Total: 57 tests** (52 fast smoke tests + 6 integration tests)

### Task Detector Tests (7 tests)
- Task file structure validation
- Dependency relationship parsing
- Error handling for empty/malformed files

## CI/CD Integration

These tests run automatically on:
- Pull requests (via GitHub Actions)
- Before merges to main branch

## Adding New Tests

When adding new tests:

1. **Create test file** in `core/tests/`
2. **Add fixtures** if needed in `core/tests/fixtures/`
3. **Update run_tests.sh** to include new test suite
4. **Run tests locally** before committing

### Test Guidelines

- **Fast**: Tests should complete in < 1 second each
- **Isolated**: No dependencies between tests
- **Repeatable**: Same result every run
- **Clear**: Descriptive test names and messages
- **Focused**: Test one thing at a time

## Maintenance

Tests should be updated when:
- Core functionality changes
- New scripts are added
- File formats change
- Error handling is modified

## Troubleshooting

**Tests fail locally but pass in CI:**
- Check Python version (3.8+ required)
- Verify file permissions (test scripts must be executable)
- Ensure working directory is project root

**Import errors:**
- Check sys.path modifications in test files
- Verify module locations match test expectations

**Permission errors:**
- Run: `chmod +x core/tests/*.sh core/tests/*.py`
