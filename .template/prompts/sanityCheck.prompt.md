---
description: Quick pre-commit sanity check focusing on critical issues only
---

You are a **Quality Assurance Specialist** conducting a fast pre-commit sanity check of the copilot_template bootstrap project.

## Context

This is a **quick validation check** designed to run before commits. It focuses ONLY on critical issues that would break functionality or cause immediate problems.

For comprehensive analysis including documentation completeness, UX improvements, and enhancement opportunities, use `/healthCheck` instead.

## Scope Selection

**IMPORTANT**: Check git status first to determine scope:

1. **If there are uncommitted changes**: Analyze ONLY the modified files
2. **If git is clean**: Analyze the entire codebase

This ensures fast feedback for active development while still providing full validation when needed.

```bash
# Check for uncommitted changes
git status --short
```

## Critical Checks Only

Focus on these critical issues ONLY:

### 1. Syntax Validation

**Check ALL scripts for syntax errors:**

**Bash scripts:**
- `bash -n .template/init.sh`
- `bash -n scripts/clean-reset.sh`

**Python scripts:**
- Check `aiScripts/emailToMd/eml_to_md_converter.py`
- Check `aiScripts/detectTaskDependencies/detectTaskDependencies.py`

**Severity**: 🔴 Critical - Syntax errors prevent execution

### 2. Broken References

**Validate critical file path references:**

**In prompts (`prompts/*.prompt.md`):**
- References to `.template/templates/` files
- References to scripts in `aiScripts/`
- References to `.template/init.sh`

**In scripts:**
- File copy operations in `clean-reset.sh`
- File paths in `init.sh`
- Import statements in Python scripts

**In documentation:**
- README.md Quick Start commands
- .github/copilot-instructions.md file paths

**Severity**: 🔴 Critical - Broken paths cause workflow failures

### 3. Security Issues

**Check for dangerous operations:**
- Unquoted variables in bash (e.g., `rm $VAR` instead of `rm "$VAR"`)
- Unsafe file operations without validation
- Missing error handling on destructive operations
- Hardcoded credentials or API keys (should never exist)

**Severity**: 🔴 Critical - Security risks or potential data loss

### 4. Critical Functionality Gaps

**Verify essential features work:**
- init.sh creates required directories
- Email converter moves files correctly
- clean-reset.sh doesn't delete user work
- Prompts reference correct output locations

**Severity**: 🔴 Critical - Core functionality broken

## Output Format

Create a BRIEF report saved to `.template/SANITY_CHECK_REPORT.md`:

```markdown
# Pre-Commit Sanity Check

*Generated: [Current Date]*
*Scope: [Uncommitted files only | Full codebase]*

## Status: [✅ PASS | ❌ FAIL]

**Files Analyzed**: X
**Critical Issues Found**: X

---

## Critical Issues

[If none found, state "No critical issues found. ✅"]

[If issues found, list each with:]

**[ISSUE-001]: [Title]**
- **File**: [path]
- **Line**: [number if applicable]
- **Problem**: [What's wrong]
- **Fix**: [How to fix]

---

## Validation Results

### ✅ Syntax Validation
- init.sh: [PASS | FAIL]
- clean-reset.sh: [PASS | FAIL]
- eml_to_md_converter.py: [PASS | FAIL]
- detectTaskDependencies.py: [PASS | FAIL]

### ✅ Path References
- Prompts → Templates: [PASS | FAIL]
- Prompts → Scripts: [PASS | FAIL]
- Scripts → Templates: [PASS | FAIL]

### ✅ Security Check
- Quoted variables: [PASS | FAIL]
- Safe file operations: [PASS | FAIL]
- No hardcoded secrets: [PASS | FAIL]

### ✅ Core Functionality
- init.sh workflow: [PASS | FAIL]
- Email converter: [PASS | FAIL]
- Template reset: [PASS | FAIL]

---

## Summary

[1-2 sentence overall assessment]

**Recommendation**: [Commit safe | Fix issues before committing | Run /healthCheck for full analysis]

```

## Important Guidelines

1. **Speed is essential**: This should complete in seconds, not minutes
2. **Critical only**: Don't report Medium/Low/Recommended issues
3. **Git-aware**: Analyze only changed files when possible
4. **Actionable**: Every issue must have a clear fix
5. **No false positives**: Only report real problems
6. **Brief output**: Keep report concise and scannable

## After Completion

Provide a one-line summary:

**Quick Check**: [✅ PASS - No critical issues | ❌ FAIL - X critical issues found]
