---
description: Quick start workflow - Initialize project, process emails and notes, and generate summary in one flow
---

You are an AI agent performing a complete project initialization workflow.

Follow these steps in sequence:

## Step 1: Initialize AI Agent Context

First, run the `/projectInit` prompt to:
- Read AI agent instructions from `aiDocs/AI.md`
- Understand the project structure and data processing workflows
- Review project documentation in `aiDocs/`
- Get familiar with available tools and scripts

## Step 2: Check for Email and Notes Files

Check if there are any data files to process:

### Check for Emails
- Check if any `.eml` files exist in the `email/raw/` directory

### Check for Notes
- Check if any `.txt` or `.md` files exist in the `notes/raw/` directory

**If NO files exist in either directory**, inform the user:

```
No email or notes files found in email/raw/ or notes/raw/

To add project context:
1. Export email threads to .eml format from your email client → place in email/raw/
2. Export notes from OneNote/Apple Notes as .txt or .md → place in notes/raw/
3. Re-run /quickStartProject or run /discoverEmail and /discoverNotes

For now, I'll skip data processing and continue with available context.
```

## Step 3: Process Email Files (if present)

If `.eml` files were found in `email/raw/`, run the `/discoverEmail` workflow:

Execute the email converter script from the **project root** directory:

```bash
python3 "core/aiScripts/emailToMd/eml_to_md_converter.py"
```

The script will:
1. Convert all `.eml` files from `email/raw/` to Markdown
2. Save converted files to `email/ai/`
3. Move processed `.eml` files to `email/processed/`

**Verify the move**: After running the script, check that:
- `.eml` files have been moved from `email/raw/` to `email/processed/`
- Corresponding `.md` files exist in `email/ai/`
- If files were not moved, report the error and check file permissions

Then:
- Read all converted Markdown files in `email/ai/`
- Extract relevant information (contacts, tasks, technical details, etc.)
- Update all files in `aiDocs/` based on email content:
  - `aiDocs/SUMMARY.md` - Quick Context, contacts, background, technical details, Decision Log
  - `aiDocs/TASKS.md` - tasks with IDs (`TASK-001`), statuses, cross-references, priorities
  - `aiDocs/DISCOVERY.md` - discovery questions with metadata (Ask/Check/Status/Priority)
  - `aiDocs/AI.md` - workflows, procedures, AI Agent Notes with project-specific guidance
- Update "Last Updated" dates to current date in all modified `aiDocs/` files

**Update State File**: After email processing completes:
```python
python3 -c "
import sys
sys.path.insert(0, 'core/aiScripts')
from state_manager import increment_email_count
increment_email_count()
"
```

## Step 3b: Process Notes Files (if present)

If `.txt` or `.md` files were found in `notes/raw/`, run the `/discoverNotes` workflow:

Execute the notes converter script from the **project root** directory:

```bash
python3 "core/aiScripts/notesToMd/notes_to_md_converter.py"
```

The script will:
1. Convert all `.txt` and `.md` files from `notes/raw/` to standardized Markdown
2. Save converted files to `notes/ai/`
3. Move processed files to `notes/processed/`

**Verify the move**: After running the script, check that:
- Original files have been moved from `notes/raw/` to `notes/processed/`
- Corresponding `.md` files exist in `notes/ai/`
- If files were not moved, report the error and check file permissions

Then:
- Read all converted Markdown files in `notes/ai/`
- Extract relevant information (contacts, tasks, decisions, technical details, etc.)
- Update all files in `aiDocs/` based on notes content (merge with email data if both exist):
  - `aiDocs/SUMMARY.md` - Add/update contacts, decisions, risks from notes
  - `aiDocs/TASKS.md` - Add tasks from action items in notes
  - `aiDocs/DISCOVERY.md` - Add questions from notes
  - `aiDocs/AI.md` - Add project-specific guidance from notes
- Update "Last Updated" dates to current date in all modified `aiDocs/` files

**Update State File**: After notes processing completes:
```python
python3 -c "
import sys
sys.path.insert(0, 'core/aiScripts')
from state_manager import increment_notes_count
increment_notes_count()
"
```

## Step 4: Generate Project Summary and Documentation

Run the `/updateSummary` workflow:

- Review all `aiDocs/` files for consistency and accuracy
- Verify Quick Context, Decision Log, Task IDs, and Discovery metadata
- Cross-reference with email content in `email/ai/`
- Create or update `PROJECT.md` at the project root with:
  - **AI model tagline** (if creating for first time): *This document was originally created by an AI agent using the Claude Sonnet 4.5 model.*
  - Project overview and current status
  - Key contacts
  - Completed work and outstanding tasks (with TASK IDs)
  - Blockers and risks
  - Outstanding questions and next steps
  - Decision log highlights
- Generate human-readable extracts in `docs/` directory:
  - `docs/CONTACTS.md` - Key stakeholder contact information
  - `docs/TASKS.md` - High-priority tasks and blockers
  - `docs/DECISIONS.md` - Decision log table
  - `docs/QUESTIONS.md` - Unanswered questions

**Update State File**: After summary generation completes:
```python
python3 -c "
import sys
sys.path.insert(0, 'core/aiScripts')
from state_manager import update_summary_timestamp
update_summary_timestamp()
"
```

**Optional: Run Task Dependency Detection**

If tasks were created or updated during email or notes processing:
- Run: `python3 core/aiScripts/detectTaskDependencies/detectTaskDependencies.py aiDocs/TASKS.md`
- Review generated `TASK_DEPENDENCY_REPORT.md` for suggested relationships
- Update task Blocks/Related fields based on high-confidence detections
- Resolve any circular dependencies identified

## Step 5: Validate and Provide Summary Report

Before providing your final report, verify:
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
- [ ] "Last Updated" dates are current in all `aiDocs/` files

After completing all steps, provide a comprehensive report:

### Initialization Complete

**Project Setup Summary:**
- ✓ AI agent initialized with project context
- ✓ Email processing: [X emails processed / No emails found]
- ✓ Notes processing: [X notes processed / No notes found]
- ✓ Documentation updated: [list files updated]
- ✓ Project summary generated: PROJECT.md
- ✓ Human-readable docs created: docs/ folder

**Key Findings:**
- **Contacts**: [number added] new contacts added, [number removed] removed
  - New: [list names and organizations]
  - Removed: [list names if any]
- **Tasks**: [number created] new tasks created, [number completed] tasks marked complete
  - New outstanding tasks: [list TASK-IDs with brief description]
  - Newly completed tasks: [list completed task descriptions]
- **Risks**: [number added] new risks identified, [number removed] risks resolved
  - New risks: [list risk descriptions with severity]
  - Resolved risks: [list if any]
- **Blockers**: [number added] new blockers identified, [number removed] blockers cleared
  - New blockers: [list blocker descriptions]
  - Cleared blockers: [list if any]

**Documentation Health Check:**
- Contact completeness: [X%] have complete email, role, and organization
- Task ownership: [X%] of tasks have assigned owners (not TBD)
- Cross-reference integrity: [X%] of task cross-references are valid
- Discovery question metadata: [X%] have all required fields
- Quick Context compliance: [Yes/No] meets character limits

**Next Steps:**
1. **📄 Review PROJECT.md at project root for complete project overview**
2. **📁 Check docs/ folder for quick reference (contacts, tasks, decisions, questions)**
3. Check `aiDocs/TASKS.md` for complete task details
4. Review `aiDocs/DISCOVERY.md` for unanswered questions

**To add more context later:**
- Export emails to `email/raw/` and run `/discoverEmail` to process them
- Export notes to `notes/raw/` and run `/discoverNotes` to process them
- Run `/updateSummary` to regenerate the summary

**Optional: Run Task Dependency Detection**

If tasks were created during email or notes processing:
- Run: `python3 core/aiScripts/detectTaskDependencies/detectTaskDependencies.py aiDocs/TASKS.md`
- Review generated `aiDocs/TASK_DEPENDENCY_REPORT.md` for suggested relationships
- Update task Blocks/Related fields based on high-confidence detections
- Resolve any circular dependencies identified

---

## Step 6: Output Success Validation Checklist

After completing all steps, validate the output and provide this checklist:

```
# ✅ Project Initialization Complete

## Validation Checklist

### Required Files
- [✓] PROJECT.md exists at project root
- [✓] aiDocs/SUMMARY.md exists and populated
- [✓] aiDocs/TASKS.md exists and populated
- [✓] aiDocs/DISCOVERY.md exists and populated
- [✓] aiDocs/AI.md exists and populated
- [✓] docs/CONTACTS.md exists
- [✓] docs/TASKS.md exists
- [✓] docs/DECISIONS.md exists
- [✓] docs/QUESTIONS.md exists

### Email Processing (if emails present)
- [✓] email/ai/ contains .md files (X files converted)
- [✓] email/processed/ contains .eml files (X files archived)
- [✓] email/raw/ is empty

### Content Quality
- [✓] PROJECT.md contains AI model tagline
- [✓] PROJECT.md has sections: Overview, Status, Contacts, Tasks, Risks
- [✓] SUMMARY.md Quick Context populated (What/Who/Status)
- [✓] SUMMARY.md has at least 1 contact listed
- [✓] TASKS.md has tasks with sequential IDs (TASK-001, TASK-002, etc.)
- [✓] All task cross-references (Blocks, Related) are valid
- [✓] "Last Updated" dates are current

### Structure Validation
- [✓] No placeholder text remains ([CUSTOMER], [PROJECT], [DATE])
- [✓] All required metadata fields populated
- [✓] Markdown formatting is valid
- [✓] File paths and links are correct

## Success! 🎉

Your project documentation is ready.

**Next Steps:**
1. Review PROJECT.md for project overview
2. Check docs/ folder for quick reference
3. Review aiDocs/TASKS.md for outstanding work
4. Add more emails to email/raw/ or notes to notes/raw/ as project progresses
5. Run /updateSummary when you need to refresh documentation

**If any items are unchecked:**
- Review error messages above
- Check that email/notes files were in correct format
- Verify prerequisites (Python 3.x installed)
- Run /projectInit to reload context
- Try /quickStartProject again
```

---

## Important Notes

- Always run the email converter from the project root directory
- Skip email processing gracefully if no `.eml` files are present
- Ensure all documentation is consistent across files
- Highlight any critical issues or urgent items discovered
- If email processing fails, continue with remaining steps and report the error
- **Direct user to PROJECT.md at project root for complete project status**
- **Direct user to docs/ folder for quick reference materials**
- Template files are preserved in `core/templates/` directory
- To reset project to clean state, use `./go.sh` and select "Reset Project"

---

## Common Scenarios

### Scenario 1: Brand New Project Setup
**Situation**: Just cloned Lumina, have 10 emails from new MarkLogic consulting engagement
**Input**: 10 .eml files exported from email client
**Steps**:
1. Place all .eml files in email/raw/
2. Run `/quickStartProject`
3. Workflow runs all steps automatically

**Expected Result**:
- ProjectInit: Context loaded successfully
- Email processing: 10 emails converted and processed
- aiDocs/ populated: 15 contacts, 20 tasks (TASK-001 to TASK-020), 5 risks
- PROJECT.md created with AI tagline
- docs/ created with all 4 quick reference files
- Ready to work on project immediately

**Next Steps**: Review PROJECT.md for project overview, check outstanding tasks

---

### Scenario 2: Project Already Initialized
**Situation**: Coming back to project after week off, 3 new emails to process
**Input**: 3 .eml files from last week
**Steps**:
1. Add 3 new .eml files to email/raw/
2. Run `/quickStartProject`
3. Workflow processes new emails, updates existing docs

**Expected Result**:
- ProjectInit: Shows existing project state (50 tasks, 12 contacts)
- Email processing: 3 new emails processed
- aiDocs/ updated: 2 new contacts, 4 new tasks (TASK-051 to TASK-054), 2 tasks completed
- PROJECT.md regenerated with updates
- docs/ refreshed with current state
- Existing data preserved, only additions made

**Summary Shows**: 3 emails processed, 2 contacts added, 4 tasks created, 2 completed

---

### Scenario 3: No Emails Yet (Documentation Only)
**Situation**: Want to set up project structure before emails arrive
**Input**: No .eml files
**Steps**:
1. Run `/quickStartProject`
2. Workflow detects empty email/raw/
3. Continues with context loading and template setup

**Expected Result**:
- ProjectInit: Context loaded from templates
- Email processing: Skipped with message "No emails found"
- aiDocs/ in template state (placeholders present)
- PROJECT.md not created yet (no content)
- docs/ in template state
- Ready to add emails when they arrive

**Message**: "No email files found. Add emails to email/raw/ then run /discoverEmail"
