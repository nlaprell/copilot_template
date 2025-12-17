---
description: Complete a GitHub issue following standardized workflow from issue to PR
---

**CRITICAL**: When a user requests that a GitHub issue be completed, implemented, or worked on, you MUST follow this standardized workflow. Do NOT ask for confirmation or skip steps.

## Workflow Steps

### 1. Fetch Issue Details

- Use GitHub MCP tools to get the full issue details
- Read the issue body, acceptance criteria, implementation steps
- Understand the scope and requirements completely
- Note any dependencies or related issues

### 2. Create Branch Based on Issue Type

**Determine branch prefix from issue labels:**
- **Bug/Defect**: Issues with `bug`, `critical`, `defect`, or `fix` labels → `defect/{number}-{description}`
- **Feature/Enhancement**: Issues with `enhancement`, `feature`, or other labels → `feature/{number}-{description}`

**Branch naming format**: `{prefix}/{issue_number}-{brief-description}`
- Examples:
  - Bug: `defect/1-fix-mcp-config-format`
  - Feature: `feature/5-centralized-logging`
- Use kebab-case for description (lowercase with hyphens)
- Keep branch name under 50 characters total
- Create branch from current default branch (usually `main`)
- Link branch to issue in commit messages

### 3. Implement the Changes

- Follow the implementation steps from the issue
- Make incremental, logical commits (not one giant commit)
- Follow coding standards and patterns from the issue
- Update documentation if specified in acceptance criteria
- Add tests if specified in acceptance criteria

### 4. Sanity Check

- Run syntax validation for all modified scripts
- For bash scripts: `bash -n script.sh`
- For Python scripts: `python3 -m py_compile script.py`
- Verify file paths are correct
- Check that no placeholders remain
- Ensure changes match acceptance criteria
- If tests exist, run them: `.template/tests/test_suite.sh`

### 5. Commit Changes

- Use conventional commit format: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`
- Reference issue in commit: `Fixes #123` or `Implements #123`
- Example: `feat(logging): add centralized logging system\n\nImplements #5`
- Make commits atomic (one logical change per commit)
- Write clear, descriptive commit messages

### 6. Create Pull Request

- Title format: `[Issue #{number}] Brief description`
- Example: `[Issue #5] Add centralized logging system`
- Include in PR description:
  - Link to issue: `Closes #123`
  - Summary of changes
  - Acceptance criteria checklist (from issue)
  - Testing performed
  - Any breaking changes or notes
- Assign yourself as the PR author
- Add relevant labels (match issue labels)
- Request review if applicable

## Example Flows

### Example 1: Bug Fix

**User says**: "Complete issue #1"

Issue #1 has labels: `bug`, `critical`, `mcp`

```bash
# 1. Fetch issue (using MCP GitHub tools)
# Issue #1: "Fix MCP Configuration Format"
# Labels: bug, critical, mcp

# 2. Create defect branch (bug label detected)
git checkout -b defect/1-fix-mcp-config-format

# 3. Implement changes (multiple commits)
git add .template/scripts/init.sh
git commit -m "fix(mcp): correct configuration format in init.sh

Fixes #1
- Change 'mcpServers' to 'servers' on line 154
- Update merge logic to output correct format"

git add .template/scripts/clean-reset.sh
git commit -m "fix(mcp): correct configuration format in clean-reset.sh

Fixes #1
- Change 'mcpServers' to 'servers' on line 162"

# 4. Sanity check
bash -n .template/scripts/init.sh
bash -n .template/scripts/clean-reset.sh

# 5. Already committed above

# 6. Create PR
# Title: [Issue #1] Fix MCP Configuration Format
# Body: Closes #1, fixes critical MCP server loading bug
```

### Example 2: Feature Enhancement

**User says**: "Implement issue #5"

Issue #5 has labels: `enhancement`, `quality`

```bash
# 1. Fetch issue (using MCP GitHub tools)
# Issue #5: "Add Centralized Logging System"
# Labels: enhancement, quality

# 2. Create feature branch (enhancement label detected)
git checkout -b feature/5-centralized-logging

# 3. Implement changes (multiple commits)
git add .template/aiScripts/logger.py
git commit -m "feat(logging): add Python logging helper module

Implements #5
- Creates centralized logger with file and console handlers
- Supports log rotation (10MB max, 5 backups)
- Configurable log levels"

git add .template/aiScripts/emailToMd/eml_to_md_converter.py
git commit -m "feat(logging): integrate logging into email converter

Implements #5
- Replace print statements with logger calls
- Add DEBUG level for detailed email processing
- Include stack traces in error logs"

# 4. Sanity check
python3 -m py_compile .template/aiScripts/logger.py
python3 -m py_compile .template/aiScripts/emailToMd/eml_to_md_converter.py

# 5. Already committed above

# 6. Create PR
# Title: [Issue #5] Add Centralized Logging System
# Body: Closes #5, adds comprehensive logging infrastructure
```

## Mandatory Rules

- ✅ **ALWAYS** create a feature branch (never commit directly to main)
- ✅ **ALWAYS** link commits to the issue (`Fixes #123`, `Implements #123`)
- ✅ **ALWAYS** run sanity checks before committing
- ✅ **ALWAYS** create a PR (never merge directly)
- ✅ **ALWAYS** include acceptance criteria checklist in PR
- ❌ **NEVER** skip the sanity check step
- ❌ **NEVER** make one giant commit (break into logical commits)
- ❌ **NEVER** commit broken code (syntax errors, etc.)

## When Things Go Wrong

**If sanity checks fail:**
1. Fix the issues identified
2. Re-run sanity checks
3. Commit fixes separately
4. Continue with PR creation

**If implementation is unclear:**
1. Ask clarifying questions BEFORE creating the branch
2. Do NOT proceed with partial understanding
