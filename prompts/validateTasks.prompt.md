---
description: Validate task structure, dependencies, and metadata integrity
---

You are an AI agent performing a quick validation check on the task tracking system.

This is a **lightweight validation** focused on task structure and integrity. For comprehensive documentation review, use `/updateSummary` instead.

## Purpose

Validate `aiDocs/TASKS.md` for:
- Structural integrity
- Metadata completeness
- Cross-reference validity
- Dependency relationships
- Common issues

## Validation Steps

### 1. Check Task ID Sequencing

Verify all outstanding tasks have proper sequential IDs:
- Format: `TASK-001`, `TASK-002`, `TASK-003`, etc.
- No duplicates
- Gaps are allowed (completed tasks moved to archive)
- All IDs are properly formatted (3 digits, zero-padded)

### 2. Verify Required Metadata

For each task, check that it has:
- **Owner**: Must be present (can be "TBD", never blank)
- **Status**: One of: Not Started | In Progress | Blocked | Completed
- **Source**: Citation for where task originated
- **Context**: Description of what needs to be done

### 3. Validate Cross-References

Check all task cross-references:
- **Blocks**: All referenced task IDs must exist
- **Related**: All referenced task IDs must exist
- No self-references (task blocking/relating to itself)
- Report any broken references

### 4. Detect Circular Dependencies

Look for circular dependency chains:
- Task A blocks Task B, Task B blocks Task A
- Longer chains: A → B → C → A
- Report all circular dependencies found

### 5. Check Task Priority Alignment

Verify tasks are in appropriate priority categories:

**High Priority tasks should have:**
- Explicit deadline, OR
- Blocks other work, OR
- On critical path, OR
- Security/compliance requirement

**Planning Tasks should be:**
- Future work dependent on decision, OR
- No immediate deadline, OR
- Preparatory activities

**Documentation Tasks should be:**
- Post-completion documentation, OR
- Process improvement, OR
- Lessons learned

Report any tasks that seem miscategorized.

### 6. Run Dependency Detection Tool

Execute the automated dependency detector:

```bash
python3 core/aiScripts/detectTaskDependencies/detectTaskDependencies.py aiDocs/TASKS.md
```

Review the generated `aiDocs/TASK_DEPENDENCY_REPORT.md` for:
- Suggested task relationships
- Confidence scores (high/medium/low)
- Potential missing dependencies
- Circular dependency warnings

### 7. Check for Orphaned Tasks

Identify tasks that:
- Have no dependencies (don't block anything, aren't blocked)
- Have no related tasks
- Might need better integration with other work

## Validation Report

Provide a concise validation report:

```markdown
# Task Validation Report

**Date**: [Current Date]
**File**: `aiDocs/TASKS.md`

## Summary

- Total outstanding tasks: X
- Task ID integrity: ✅ PASS / ❌ FAIL
- Metadata completeness: X% complete
- Cross-reference validity: X% valid
- Circular dependencies: X found
- Orphaned tasks: X found

---

## Issues Found

### Critical Issues (Must Fix)

**[ISSUE-001]: [Description]**
- **Task**: TASK-XXX
- **Problem**: [What's wrong]
- **Fix**: [How to resolve]

### Warnings (Should Review)

**[WARNING-001]: [Description]**
- **Task**: TASK-XXX
- **Concern**: [What to check]
- **Suggestion**: [Recommendation]

---

## Dependency Analysis

**Dependency Detection Results:**
- High confidence suggestions: X
- Medium confidence suggestions: X
- Low confidence suggestions: X
- Circular dependencies detected: X

**Recommended Actions:**
1. [First priority action]
2. [Second priority action]

---

## Task Health Metrics

- **Ownership**: X% of tasks have assigned owners (not TBD)
- **Blocked tasks**: X tasks currently blocked
- **Critical path**: X tasks on critical path
- **Average dependencies per task**: X.X

---

## Recommendations

1. [Specific recommendation based on findings]
2. [Another recommendation]

**Next Steps:**
- Fix critical issues immediately
- Review warnings and update as needed
- Apply high-confidence dependency suggestions
- Resolve circular dependencies
```

## Important Notes

- This is a **validation only** - does not modify files
- For comprehensive review, use `/updateSummary`
- Run this after manually editing TASKS.md
- Run this before major planning sessions
- Does not check email content or PROJECT.md

---

## Common Scenarios

### Scenario 1: After Manual TASKS.md Edits
**Situation**: Just manually added 5 tasks and updated 3 task statuses in aiDocs/TASKS.md
**Steps**:
1. Run `/validateTasks`
2. Agent validates structure and relationships
3. Agent reports findings

**Expected Result**:
- Task ID integrity: ✅ PASS (sequential IDs maintained)
- Metadata completeness: 90% (2 tasks missing deadlines)
- Cross-references: 95% valid (1 broken reference)
- Circular dependencies: 0 found
- Orphaned tasks: 2 identified

**Report Shows**:
- Issue: TASK-025 references TASK-099 which doesn't exist
- Warning: TASK-018 and TASK-022 have no dependencies
- Recommendation: Fix broken reference, review orphaned tasks

---

### Scenario 2: Pre-Planning Session Validation
**Situation**: Sprint planning meeting tomorrow, want to ensure task list is clean
**Steps**:
1. Run `/validateTasks`
2. Review dependency detection results
3. Apply high-confidence suggestions

**Expected Result**:
- Total outstanding tasks: 45
- Task ownership: 80% assigned (9 tasks need owners)
- Dependency detection: 12 high-confidence suggestions
- Circular dependencies: 0
- Critical path: 8 tasks identified

**Report Shows**:
- 9 tasks with Owner: TBD (need assignment)
- 12 suggested task relationships to add
- No blocking issues for planning session

**Next Steps**: Assign owners to TBD tasks, apply dependency suggestions

---

### Scenario 3: After Large Task Import
**Situation**: Imported 30 tasks from email thread, want to validate relationships
**Steps**:
1. Run `/validateTasks`
2. Run dependency detection
3. Review circular dependency warnings

**Expected Result**:
- Task ID integrity: ❌ FAIL (duplicate ID TASK-042)
- Circular dependencies: 1 found (TASK-015 → TASK-022 → TASK-015)
- High confidence suggestions: 18
- Metadata completeness: 85%

**Report Shows**:
- CRITICAL: Duplicate task ID TASK-042 (must fix immediately)
- CRITICAL: Circular dependency between TASK-015 and TASK-022
- 18 suggested relationships based on context analysis

**Next Steps**: Fix duplicate ID, resolve circular dependency, apply suggestions
