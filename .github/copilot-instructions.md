# GitHub Copilot Instructions

This file contains universal instructions for AI agents working in this workspace. These rules apply to ALL projects using this template.

---

## Project Structure

### Email Management Workflow

All project communication and context from email should follow this workflow:

1. **Raw emails**: Place `.eml` files in `/email/raw/` for processing
2. **Convert**: Run the email converter to transform emails into AI-readable format
3. **AI-readable emails**: Converted emails stored in `/email/ai/` as Markdown files
4. **Processed emails**: Original `.eml` files archived in `/email/processed/` after conversion

### Email Converter Tool

Located at `.template/aiScripts/emailToMd/eml_to_md_converter.py`, this tool converts `.eml` email files to Markdown format.

**Usage**:
```bash
# Run from project root
python3 ".template/aiScripts/emailToMd/eml_to_md_converter.py"
```

The converter automatically:
- Creates required directories (`email/raw/`, `email/ai/`, `email/processed/`)
- Converts all `.eml` files from `email/raw/` to Markdown
- Saves converted files to `email/ai/`
- Moves processed `.eml` files to `email/processed/`

---

## GitHub Labels and Milestones

### Standard Labels

Labels must be applied to ALL issues and PRs to enable proper categorization, filtering, and workflow automation.

#### Type Labels (Required - Choose ONE)

Every issue/PR must have exactly one type label:

- **`bug`** - Something is broken or not working as intended
  - Use for: Runtime errors, incorrect behavior, crashes, data corruption
  - Branch: `defect/{number}-...`
  - Commit: `fix(scope):`

- **`critical`** - Urgent bug that blocks major functionality or causes data loss
  - Use for: Showstoppers, security vulnerabilities, data loss, broken core features
  - Branch: `defect/{number}-...`
  - Commit: `fix(scope):`
  - **Always prioritize critical issues first**

- **`enhancement`** - New feature or improvement to existing functionality
  - Use for: New capabilities, feature additions, improvements
  - Branch: `feature/{number}-...`
  - Commit: `feat(scope):`

- **`documentation`** - Changes to documentation only
  - Use for: README updates, code comments, API docs, user guides
  - Branch: `feature/{number}-...`
  - Commit: `docs(scope):`

- **`refactor`** - Code restructuring without changing behavior
  - Use for: Code cleanup, reorganization, performance improvements
  - Branch: `feature/{number}-...`
  - Commit: `refactor(scope):`

#### Category Labels (Optional - Choose MULTIPLE)

Add category labels to provide additional context:

- **`quality`** - Code quality improvements (testing, logging, error handling)
- **`testing`** - Test-related changes (unit tests, integration tests, test infrastructure)
- **`mcp`** - Model Context Protocol related (server configs, MCP functionality)
- **`scripts`** - Bash/shell script changes
- **`python`** - Python code changes
- **`workflow`** - GitHub Actions, CI/CD, automation
- **`dependencies`** - Dependency updates or changes
- **`security`** - Security-related issues or improvements

#### Priority Labels (Optional - Choose ONE)

Use priority labels when needed for planning:

- **`priority: high`** - Should be done soon (next sprint/week)
- **`priority: medium`** - Should be done eventually (next month)
- **`priority: low`** - Nice to have (backlog)

#### Status Labels (Automatic/Manual)

- **`wip`** - Work in progress (applied to PRs when not ready for review)
- **`ready for review`** - PR is complete and ready for review
- **`blocked`** - Cannot proceed due to external dependency
- **`needs discussion`** - Requires team discussion before implementation

### Label Combination Rules

**For Bugs:**
```
Required: bug
Optional: critical (if urgent), mcp, scripts, python, security
Priority: high, medium, or low
```

**For Features:**
```
Required: enhancement
Optional: quality, testing, mcp, scripts, python, workflow
Priority: high, medium, or low
```

**For Documentation:**
```
Required: documentation
Optional: (rarely needed)
Priority: (rarely needed)
```

### Labeling Examples

**Example 1: Critical Bug**
```
Labels: bug, critical, mcp
Reason: MCP servers not loading - blocks all MCP functionality
Branch: defect/1-fix-mcp-config-format
```

**Example 2: Quality Enhancement**
```
Labels: enhancement, quality, scripts
Reason: Adding error handling to bash scripts
Branch: feature/3-improve-error-handling
```

**Example 3: Testing Infrastructure**
```
Labels: enhancement, testing, quality
Reason: Adding smoke test suite
Branch: feature/4-add-smoke-tests
```

**Example 4: Security Bug**
```
Labels: bug, critical, security
Reason: Exposed GitHub token in config
Branch: defect/7-remove-exposed-token
```

### Milestones

Milestones group related issues for release planning and progress tracking.

#### Milestone Naming Convention

Use semantic versioning or descriptive names:
- **`v1.0.0`** - Initial release
- **`v1.1.0`** - Feature release
- **`v1.0.1`** - Patch release
- **`Phase 1: Core Functionality`** - Functional grouping
- **`Q1 2025`** - Time-based grouping

#### When to Create Milestones

Create milestones for:
- **Releases**: Major versions (v1.0.0, v2.0.0)
- **Phases**: Logical groupings of work (Phase 1: Foundation, Phase 2: Quality)
- **Sprints**: Time-boxed iterations (Sprint 1, Sprint 2)
- **Initiatives**: Major projects (Email Workflow, MCP Integration)

#### Milestone Assignment Rules

**Always assign issues to milestones when:**
- Issue is part of a planned release
- Issue belongs to a specific project phase
- Issue is in current sprint/iteration

**Don't assign to milestone when:**
- Issue is exploratory or research
- Issue is a small fix with no release target
- Issue is in backlog with no timeline

#### Milestone Examples

**Release-based:**
```
Milestone: v1.0.0 - Bootstrap MVP
Issues: #1, #2, #3, #4 (core functionality bugs and must-have features)
Due Date: 2025-01-15
```

**Phase-based:**
```
Milestone: Phase 2: Quality Improvements
Issues: #3, #4, #5, #6, #7 (error handling, testing, logging, etc.)
Due Date: 2025-02-01
```

**Sprint-based:**
```
Milestone: Sprint 3
Issues: Top priority items from backlog
Due Date: End of sprint (2025-12-31)
```

### Workflow Integration

When creating issues or PRs, apply labels based on this logic:

1. **Determine type** (bug/critical/enhancement/documentation/refactor) → Add type label
2. **Identify categories** (what areas does this touch?) → Add category labels
3. **Assess priority** (when should this be done?) → Add priority label if needed
4. **Check milestone** (is this part of planned work?) → Assign milestone if applicable
5. **Branch name follows type** (bug/critical → defect/, others → feature/)

### Label Management Commands

When agent creates issues:
```python
# Bug example
labels = ["bug", "critical", "mcp"]
milestone = "v1.0.0"

# Enhancement example  
labels = ["enhancement", "quality", "scripts"]
milestone = "Phase 2: Quality Improvements"
```

When agent creates PRs:
```python
# Match issue labels plus status
labels = ["bug", "critical", "mcp", "ready for review"]
milestone = "v1.0.0"  # Same as issue
```

---

## Issue-to-PR Workflow

**CRITICAL**: When a user requests that a GitHub issue be completed, implemented, or worked on, you MUST follow this standardized workflow. Do NOT ask for confirmation or skip steps.

### Workflow Steps

1. **Fetch Issue Details**
   - Use GitHub MCP tools to get the full issue details
   - Read the issue body, acceptance criteria, implementation steps
   - Understand the scope and requirements completely
   - Note any dependencies or related issues

2. **Create Branch Based on Issue Type**
   
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

3. **Implement the Changes**
   - Follow the implementation steps from the issue
   - Make incremental, logical commits (not one giant commit)
   - Follow coding standards and patterns from the issue
   - Update documentation if specified in acceptance criteria
   - Add tests if specified in acceptance criteria

4. **Sanity Check**
   - Run syntax validation for all modified scripts
   - For bash scripts: `bash -n script.sh`
   - For Python scripts: `python3 -m py_compile script.py`
   - Verify file paths are correct
   - Check that no placeholders remain
   - Ensure changes match acceptance criteria
   - If tests exist, run them: `.template/tests/test_suite.sh`

5. **Commit Changes**
   - Use conventional commit format: `type(scope): description`
   - Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`
   - Reference issue in commit: `Fixes #123` or `Implements #123`
   - Example: `feat(logging): add centralized logging system\n\nImplements #5`
   - Make commits atomic (one logical change per commit)
   - Write clear, descriptive commit messages

6. **Create Pull Request**
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

### Example Flows

**Example 1: Bug Fix - User says "Complete issue #1"**

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

**Example 2: Feature - User says "Implement issue #5"**

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

### Mandatory Rules

- ✅ **ALWAYS** create a feature branch (never commit directly to main)
- ✅ **ALWAYS** link commits to the issue (`Fixes #123`, `Implements #123`)
- ✅ **ALWAYS** run sanity checks before committing
- ✅ **ALWAYS** create a PR (never merge directly)
- ✅ **ALWAYS** include acceptance criteria checklist in PR
- ❌ **NEVER** skip the sanity check step
- ❌ **NEVER** make one giant commit (break into logical commits)
- ❌ **NEVER** commit broken code (syntax errors, etc.)

### When Things Go Wrong

If sanity checks fail:
1. Fix the issues identified
2. Re-run sanity checks
3. Commit fixes separately
4. Continue with PR creation

If implementation is unclear:
1. Ask clarifying questions BEFORE creating the branch
2. Do NOT proceed with partial understanding

---

## Standard AI Agent Workflow

When starting work on any project in this workspace:

1. **Initialize context**: Read all files in `aiDocs/` to understand project state
   - `aiDocs/AI.md` - Project-specific guidance and lessons learned
   - `aiDocs/SUMMARY.md` - Project background, contacts, risks, planning options
   - `aiDocs/TASKS.md` - Outstanding and completed tasks
   - `aiDocs/DISCOVERY.md` - Unanswered questions and information gaps

2. **Process new emails** (if present):
   - Check `/email/raw/` for new `.eml` files
   - Run email converter if emails found
   - Read converted Markdown files from `/email/ai/`
   - Extract relevant information (contacts, tasks, decisions, risks, questions)

3. **Update documentation**: Keep `aiDocs/` files current with new information
   - Update `SUMMARY.md` with new contacts, background, decisions, risks
   - Update `TASKS.md` with new tasks and completion status
   - Update `DISCOVERY.md` with new questions and answers
   - Update `AI.md` with project-specific learnings

4. **Maintain human summary**: Update root `PROJECT.md` and `docs/` for stakeholders when significant changes occur
   - **Bidirectional sync**: If users edit root `PROJECT.md`, sync changes back to `aiDocs/` files first
   - User edits to root summary are authoritative and should be preserved
   - Then regenerate root `PROJECT.md` and `docs/` extracts from updated `aiDocs/` to maintain consistency
   - Generate simplified views in `docs/` (CONTACTS.md, TASKS.md, DECISIONS.md, QUESTIONS.md)

---

## Documentation Standards

### File Responsibilities

AI agents MUST maintain these files:

- **`aiDocs/SUMMARY.md`**: Single source of truth for project state
  - Quick Context (What/Who/Status with character limits)
  - Key Contacts (complete with email, phone, role, organization)
  - Background and historical context
  - Technical details
  - Current situation (last 30 days)
  - Decision Log (Date | Decision | Made By | Rationale | Source)
  - Planning Options
  - Risks (8-field format: Title, Description, Severity, Likelihood, Impact, Mitigation, Owner, Status)
  - References

- **`aiDocs/TASKS.md`**: Task tracking with dependencies
  - Sequential task IDs (TASK-001, TASK-002, no gaps)
  - Required metadata: Owner, Status, Deadline (if applicable), Blocks, Related, Source, Context
  - Categories: High Priority, Planning Tasks, Documentation Tasks
  - Completed tasks archived by date

- **`aiDocs/DISCOVERY.md`**: Information gaps and questions
  - Checkbox format: `- [ ]` unanswered, `- [x]` answered
  - Required metadata: Ask, Check, Status, Priority
  - Answer and Source when answered
  - Categories: High Priority, Technical, Environmental

- **`aiDocs/AI.md`**: Project-specific context for AI agents
  - Project-Specific Guidance (THIS project's unique context)
  - Common Pitfalls (THIS project's known issues)
  - Quick References (THIS project's links and resources)
  - Lessons Learned (THIS project's experiences)

- **`PROJECT.md`** (root): Human-readable project summary
  - Executive summary with visual indicators
  - Condensed information for busy stakeholders
  - Links to detailed documentation in `aiDocs/`

- **`docs/`** (directory): Human-readable quick reference extracts
  - `CONTACTS.md` - Key stakeholder contact information
  - `TASKS.md` - High-priority tasks and current blockers
  - `DECISIONS.md` - Decision log in table format
  - `QUESTIONS.md` - Outstanding discovery questions

### Quick Context Format

In `aiDocs/SUMMARY.md`, the Quick Context section has strict character limits:

```markdown
## Quick Context

**What**: [Brief description - max 100 characters, one sentence only]
**Who**: [Key organizations - max 150 characters, format "Company A supporting Company B"]
**Status**: [Planning | Investigation | Active Development | Testing | Blocked | On Hold - max 50 chars]
```

### Task ID Format

Tasks must have sequential IDs when created:
- Format: `TASK-001`, `TASK-002`, `TASK-003`, etc.
- Task IDs are permanent - once assigned, never reused or renumbered
- Gaps in outstanding task IDs are expected when tasks are completed and moved to archive
- Every task MUST have an Owner (use "TBD" if unknown, never blank)
- All cross-references (Blocks, Related) must use valid task IDs that exist
- Include Source field citing email/document where task originated
- Completed task IDs can remain in Related/Blocks fields for audit trail

### Task Dependency Detection

Use the automated dependency detection script to find task relationships:
- Run: `python3 .template/aiScripts/detectTaskDependencies/detectTaskDependencies.py aiDocs/TASKS.md`
- Reviews generated report in `aiDocs/TASK_DEPENDENCY_REPORT.md`
- Updates task Blocks/Related fields based on high-confidence detections
- Resolves circular dependencies before proceeding
- Uses dependency graph visualization for planning

### Discovery Question Format

```markdown
- [ ] **[Specific, actionable question]**  
  - Ask: [Who would know the answer - specific person/role]
  - Check: [Where to look - specific emails, documents, systems]
  - Status: Unknown / Partial / Answered
  - Priority: High / Medium / Low
  - Answer: [If answered, include the answer here]
  - Source: [If answered, cite email/document/person]
```

**Question Quality Standards** - Each question must be:
1. **Specific**: Not vague, focused on concrete information
2. **Actionable**: Includes where to check or who to ask
3. **Scoped**: One topic per question, not multiple
4. **Answerable**: Has concrete answer, not philosophical
5. **Relevant**: Directly impacts project decisions

### Risk Format

All risks must include 8 required fields:

```markdown
- **Title**: [Clear, concise risk name]
  - **Description**: What could go wrong
  - **Severity**: Critical | High | Medium | Low
  - **Likelihood**: Certain | Likely | Possible | Unlikely
  - **Impact**: Specific consequences if risk occurs
  - **Mitigation**: What is being done to reduce/prevent
  - **Owner**: Who is responsible (or TBD, never blank)
  - **Status**: Active | Mitigated | Accepted | Transferred
```

---

## Conflict Resolution Rules

When processing emails that contain conflicting information:

1. **Latest information wins**: Most recent email takes precedence
2. **Note the conflict**: In Current Situation, mention "Previously X, updated to Y (per email dated [date])"
3. **Flag for clarification**: Add discovery question if contradiction is significant
4. **Document both versions**: In Historical Context, note the change in understanding
5. **Escalate critical conflicts**: If affects major decisions, add to "Critical Findings" in summary

---

## Validation Checklist

Before completing work, verify:

- [ ] All email addresses are correctly formatted and complete
- [ ] Phone numbers include country/area codes if provided
- [ ] All task IDs are sequential (gaps allowed for completed tasks)
- [ ] Every task has an Owner or "TBD" (never blank)
- [ ] All discovery questions have required metadata (Ask, Check, Status, Priority)
- [ ] Cross-references (Blocks, Related) use valid task IDs that exist
- [ ] Dates are in consistent format throughout
- [ ] Organization names are consistent throughout
- [ ] No template placeholders remain (`[DATE]`, `[CUSTOMER]`, etc.)
- [ ] Quick Context meets character limits (What: 100, Who: 150, Status: 50)
- [ ] All risks include 8 required fields
- [ ] "Last Updated" dates are current
- [ ] Run dependency detection and review for circular dependencies
- [ ] Verify task dependency graph reflects project structure

---

## Template System

### Template Files

Templates are preserved in `.template/templates/` for reference and reset:
- `SUMMARY.template.md`
- `TASKS.template.md`
- `DISCOVERY.template.md`
- `AI.template.md`

### Working Files

Always update working files in `aiDocs/` (without `.template` extension), NOT the template files.

### Reset Process

To reset project to clean state:
```bash
./go.sh
```

This copies templates to working files, clearing all project-specific content.

---

## Email Processing Best Practices

- **Always read ALL emails**: Every `.md` file in `email/ai/` must be read completely
- **Extract comprehensively**: Get contacts, tasks, technical details, risks, questions, decisions, timeline
- **Cite sources**: Use format "(Source: "Email Subject" - Date)" when adding facts
- **Deduplication**: Check email domains to identify related organizations; merge duplicate contacts
- **Verify moves**: After conversion, confirm `.eml` files moved to `email/processed/`

### MarkLogic Ecosystem Organizations

When processing contacts and organizations in MarkLogic-related projects:
- **Progress Software** is the parent company of MarkLogic
- **Progress Federal** is the MarkLogic support and consulting division for government clients
- These should be treated as the same organizational entity in documentation, with Progress Federal being the service delivery arm
- Merge duplicate contacts across Progress/Progress Federal/MarkLogic divisions as appropriate

---

## Documentation Update Triggers

Update `aiDocs/` files when:
- New emails are processed
- Tasks are completed
- Decisions are made
- Risks are identified or resolved
- Discovery questions are answered
- Project status changes

Update root `PROJECT.md` and `docs/` when:
- Major milestones reached
- Critical decisions made
- Significant status changes
- Preparing for stakeholder review

---

## Notes for AI Agents

- Email files must be converted to Markdown before AI analysis
- Prefer reading Markdown files in `/email/ai/` over raw `.eml` files
- Keep email organization consistent: raw → processed, converted → ai
- When uncertain, err on side of documenting more rather than less
- Project-specific context belongs in `aiDocs/AI.md`, not this file
