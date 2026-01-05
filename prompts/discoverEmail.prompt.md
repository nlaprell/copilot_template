---
description: Process raw email files and update project documentation based on email content
---

You are an AI agent tasked with processing email files and updating project documentation based on the information found in those emails.

**IMPORTANT**: This is an automated workflow. Do NOT ask for user confirmation or pause. Execute all steps completely and update all files as needed.

Follow these steps carefully:

## 1. Process Raw Email Files

First, you need to convert any `.eml` files in the `email/raw/` directory to Markdown format.

### Run the Email Converter

Execute the email converter script from the **project root** directory:

```bash
python3 "core/aiScripts/emailToMd/eml_to_md_converter.py"
```

The script will automatically:
1. Create required directories if they don't exist (`email/raw/`, `email/ai/`, `email/processed/`)
2. Read all `.eml` files from `email/raw/`
3. Convert them to Markdown format
4. Save converted files to `email/ai/` as `.md` files
5. Move processed `.eml` files to `email/processed/`

**Verify the move**: After running the script, check that:
- `.eml` files have been moved from `email/raw/` to `email/processed/`
- Corresponding `.md` files exist in `email/ai/`
- If files were not moved, report the error and check file permissions

## 2. Read ALL Email Content

**CRITICAL**: You MUST read EVERY `.md` file in the `email/ai/` directory completely.

### Email Processing Guidelines

When reading emails:
- Note the email date range (oldest to newest)
- Identify primary participants across all emails
- Track main topics/themes discussed
- Look for organizational relationships mentioned (divisions, partnerships, parent companies)

For each email file:
- Read the entire content
- Extract ALL relevant information:
  - **Contacts**: Names, email addresses, roles, organizations
  - **Background**: Project history, context, how the project started
  - **Technical Details**: Technologies, architectures, configurations, requirements
  - **Current Status**: Latest updates, ongoing work, recent developments
  - **Historical Context**: Timeline events, past decisions, key milestones
  - **Tasks**: Action items, next steps, deliverables, assignments
  - **Questions**: Unanswered questions, information gaps, clarifications needed
  - **Risks**: Concerns, blockers, potential issues, challenges
  - **Decisions**: Agreements made, approaches chosen, plans approved

### Handling Conflicting Information

When emails contain contradictions:
1. **Use latest information**: Most recent email takes precedence
2. **Note the conflict**: In Current Situation, mention "Previously X, updated to Y (per email dated [date])"
3. **Flag for clarification**: Add discovery question if contradiction is significant
4. **Document both versions**: In Historical Context, note the change in understanding
5. **Escalate critical conflicts**: If affects major decisions, add to "Critical Findings" in summary report

## 3. Update ALL Project Documentation Files

**MANDATORY**: You MUST update ALL relevant `aiDocs/` files based on email content. Do not skip this step.

**Note on Templates**: If `aiDocs/` files are in their default template state (containing placeholders like `[DATE]`, `[CUSTOMER]`, `[PROJECT]`, etc.), the templates are located at:
- `core/templates/SUMMARY.template.md`
- `core/templates/TASKS.template.md`
- `core/templates/DISCOVERY.template.md`
- `core/templates/AI.template.md`

The working files in `aiDocs/` (without the `.template` extension) are the ones you should update. Replace all placeholders with actual content from emails.

### Update `aiDocs/SUMMARY.md`

**Required updates:**
- **Last Updated**: Set to current date

- **Quick Context**: Create/update 3-line summary with character limits:
  - **What**: Brief description (max 100 characters, one sentence only)
  - **Who**: Key organizations only (max 150 characters, format: "Company A supporting Company B")
  - **Status**: Current phase only (max 50 characters, use one of: Planning | Investigation | Active Development | Testing | Blocked | On Hold)

- **Key Contacts Reference**: Add/update ALL people mentioned in emails with their:
  - Full name
  - Email address (verify format is complete and correct)
  - Role/title
  - Organization
  - Phone numbers (include country/area codes if provided)
  - Group contacts by organization, with subheadings for different divisions/roles within large organizations
  - **Deduplication**: Check email domains to identify related organizations; merge duplicates; if person has multiple emails, list all under one entry

- **Background**: Write comprehensive background from email history
  - Cite email sources for key facts using format: (Source: "Email Subject" - Date)

- **Historical Context**: Add timeline of key events from emails
  - Organize chronologically
  - Anything older than 30 days goes here
  - Use consistent date format throughout

- **Technical Details**: Document all technical information mentioned
  - Be specific (e.g., "MarkLogic 10.0-9.3" not just "MarkLogic")
  - Include version numbers, configurations, error codes

- **Current Situation**: Describe latest status from most recent emails
  - Focus on last 2 weeks of activity only
  - Recent progress = last 30 days

- **Decision Log**: Extract all decisions into table format:
  - Date of decision
  - What was decided
  - Who made the decision
  - Rationale/reason for decision (include email source)
  - Use consistent date format

- **Risks**: List all risks, concerns, or blockers mentioned
  - For each risk include:
    - **Title**: Clear, concise risk name
    - **Description**: What could go wrong
    - **Severity**: Critical | High | Medium | Low
    - **Likelihood**: Certain | Likely | Possible | Unlikely
    - **Impact**: Specific consequences if risk occurs
    - **Mitigation**: What is being done to reduce/prevent
    - **Owner**: Who is responsible for monitoring/mitigating (or TBD)
    - **Status**: Active | Mitigated | Accepted | Transferred

- **Stakeholder Relationships**: In appropriate section, document:
  - Organizational relationships (parent companies, divisions, partnerships)
  - Vendor/customer relationships
  - Decision authority (who can approve/reject)

### Update `aiDocs/TASKS.md`

**Required updates:**
- **Last Updated**: Set to current date

- **Outstanding Tasks**: Extract ALL action items and next steps from emails
  - Assign sequential task IDs: TASK-001, TASK-002, TASK-003, etc. (NO GAPS)
  - Categorize by priority using these guidelines:
    - **High Priority**: Has explicit deadline, blocks other work, critical path, security/compliance requirement
    - **Planning Tasks**: Future work dependent on decision, no immediate deadline, preparatory activities
    - **Documentation Tasks**: Post-completion documentation, process improvement, lessons learned
  - For each task include:
    - **Owner**: Person responsible (if mentioned) or "TBD" (NEVER leave blank)
    - **Status**: Not Started | In Progress | Blocked | Completed
    - **Blocks**: Task IDs that depend on this task (verify IDs exist)
    - **Related**: Related task IDs (verify IDs exist)
    - **Source**: Which email or document the task came from (include subject/date)
    - **Context**: Description and any mentioned deadlines
    - **Deadline**: Explicit deadline if mentioned in emails

- **Completed Tasks**: Document any completed work mentioned in emails
  - Group by month if > 1 month old, by week if recent
  - Add to appropriate date sections
  - Include what was completed and by whom (if mentioned)
  - Include source email reference

### Update `aiDocs/DISCOVERY.md`

**Required updates:**
- **Last Updated**: Set to current date

- Add ALL questions about the customer, their setup, or their environment
- **Question Quality Standards** - Each question must be:
  1. **Specific**: Not "What is the architecture?" but "What is the network architecture between the MarkLogic cluster and client applications?"
  2. **Actionable**: Include specific place to check or person to ask
  3. **Scoped**: Focused on one piece of information, not multiple topics
  4. **Answerable**: Not philosophical; should have a concrete answer
  5. **Relevant**: Directly impacts project decisions or understanding

- For each discovery question include:
  - **Ask**: Who would know the answer (specific person/role)
  - **Check**: Where to look for the answer (specific emails, documents, people)
  - **Status**: Unknown / Partial / Answered
  - **Priority**: High / Medium / Low
  - **Answer**: If the email contains the answer, mark question as [x] and include the answer
  - **Source**: If answered, cite which email provided the answer (subject and date)

- Include questions about technical requirements or configurations
- Document any information gaps or needed clarifications
- Remove obsolete or redundant questions

### Update `aiDocs/AI.md` (if applicable)

Update the **AI Agent Notes** section if emails contain:
- **Project-Specific Guidance**: Customer preferences, technical constraints, important context
- **Common Pitfalls**: Issues to avoid, warnings from experience
- **Quick References**: Important URLs, documentation, key error codes
- **Lessons Learned**: What worked well or didn't work

Also update workflows or procedures if emails mention:
- New tools or resources to document
- Updated instructions for AI agents

## 4. Documentation Quality Requirements

When updating files:
- **Be thorough**: Include ALL relevant information from emails
- **Be specific**: Use exact names, dates, technologies, and details
- **Update dates**: Change "Last Updated" fields to current date
- **Replace placeholders**: Replace `[DATE]`, `[CUSTOMER]`, `[PROJECT]`, etc. with actual content
- **Preserve structure**: Keep existing formatting and section organization
- **Be factual**: Only include information directly from emails
- **Cross-reference**: When documenting facts, note which email they came from

## 5. Validation Step

Before providing your summary, verify:
- [ ] All email addresses are correctly formatted and complete
- [ ] Phone numbers include country/area codes if provided
- [ ] All task IDs are sequential (TASK-001, TASK-002, etc.) with no gaps
- [ ] Every task has an Owner or "TBD" explicitly stated (never blank)
- [ ] All discovery questions have all required metadata fields populated (Ask, Check, Status, Priority)
- [ ] Cross-references (Blocks, Related) use valid task IDs that exist
- [ ] Dates are in consistent format throughout (e.g., "December 5, 2025")
- [ ] Organization names are consistent throughout
- [ ] No template placeholders remain (`[DATE]`, `[CUSTOMER]`, etc.)
- [ ] Quick Context meets character limits (What: 100, Who: 150, Status: 50)
- [ ] All section headings from templates are present
- [ ] Risk entries include Severity, Impact, Mitigation, Owner, Status

**Update State File**: After email processing completes:
```python
python3 -c "
import sys
sys.path.insert(0, 'core/aiScripts')
from state_manager import increment_email_count
increment_email_count()
"
```

## 6. Mandatory Summary Report

After completing ALL updates to `aiDocs/` files, provide a comprehensive summary:

**Email Processing Summary:**
- Total emails processed: [number]
- Emails read and analyzed: [list filenames]

**Documentation Updates Made:**
- `aiDocs/SUMMARY.md`: [Specific changes made]
- `aiDocs/TASKS.md`: [Specific changes made]
- `aiDocs/DISCOVERY.md`: [Specific changes made]
- `aiDocs/AI.md`: [Changes made, if any]

**Key Information Extracted:**
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
- **Discovery Questions**: [number added] new questions added, [number answered] questions answered
  - New questions: [list question topics]
  - Answered questions: [list answered question topics]

**Critical Findings:**
- Urgent items or blockers: [list any critical issues]
- Key decisions documented: [list important decisions]
- Unanswered questions: [list gaps in information]

**Project Status Changes:**
- Quick Context updated: [Yes/No - what changed]
- Decision Log entries: [number of new decisions added]
- AI Agent Notes updated: [Yes/No - what guidance added]

**Documentation Health Check:**
- Contact completeness: [X%] have complete email, role, and organization
- Task ownership: [X%] of tasks have assigned owners (not TBD)
- Cross-reference integrity: [X%] of task cross-references (Blocks, Related) are valid
- Discovery question metadata: [X%] have all required fields (Ask, Check, Status, Priority)

**Actionable Gaps Identified:**
- Missing information: [list critical gaps that need clarification]
- Tasks without owners: [list TASK-IDs needing assignment]
- Pending decisions: [list decisions blocked on stakeholder input]
- Incomplete metadata: [list items needing additional detail]

## 7. Output Success Validation Checklist

After providing the mandatory summary report, validate the output with this checklist:

```
# ✅ Email Processing Complete

## Validation Checklist

### Email Processing
- [✓] email/ai/ contains .md files (X files converted)
- [✓] email/processed/ contains .eml files (X files archived)
- [✓] email/raw/ is empty

### Required Files Updated
- [✓] aiDocs/SUMMARY.md updated
- [✓] aiDocs/TASKS.md updated
- [✓] aiDocs/DISCOVERY.md updated
- [✓] aiDocs/AI.md updated (if applicable)

### Content Quality
- [✓] SUMMARY.md Quick Context populated (What/Who/Status)
- [✓] SUMMARY.md has contacts with complete information
- [✓] TASKS.md has tasks with sequential IDs (TASK-001, TASK-002, etc.)
- [✓] All task cross-references (Blocks, Related) are valid
- [✓] "Last Updated" dates set to current date
- [✓] Decision Log updated with new decisions
- [✓] Risks documented with all 8 required fields

### Structure Validation
- [✓] No placeholder text remains ([CUSTOMER], [PROJECT], [DATE])
- [✓] All required metadata fields populated
- [✓] Task IDs are sequential (gaps allowed for completed tasks)
- [✓] Every task has Owner or "TBD" (never blank)

## Success! 🎉

Your email processing is complete and documentation updated.

**Next Steps:**
1. Run /updateSummary to regenerate PROJECT.md and docs/
2. Review aiDocs/ for extracted information
3. Validate with: `./core/scripts/validate-output.sh`
4. Add more emails to email/raw/ as project progresses

**If any items are unchecked:**
- Check email converter output for errors
- Verify .eml files were valid email format
- Ensure Python 3.x installed
- Re-run /discoverEmail after fixing issues
```

## Critical Reminders

- **DO NOT skip updates**: You MUST update `aiDocs/` files based on email content
- **DO NOT ask for confirmation**: This is an automated process
- **DO NOT leave placeholders**: Replace ALL `[DATE]`, `[CUSTOMER]`, `[PROJECT]`, etc. with actual content
- **DO read ALL emails**: Every `.md` file in `email/ai/` must be read completely
- **DO be thorough**: Extract ALL relevant information from emails
- **DO update dates**: Set "Last Updated" fields to today's date
- **DO provide complete summary**: Include all metrics for contacts, tasks, risks, blockers
- Always run the email converter from the project root directory
- If email content conflicts with existing documentation, update with the latest information from emails and note the conflict in your summary
- **Optional**: After creating/updating tasks, run dependency detection: `python3 core/aiScripts/detectTaskDependencies/detectTaskDependencies.py aiDocs/TASKS.md`

---

## Common Scenarios

### Scenario 1: First Email Import (Project Kickoff)
**Situation**: Just set up project, have 5 emails from client about new MarkLogic migration
**Input**: 5 .eml files exported from Outlook
**Steps**:
1. Place all .eml files in email/raw/
2. Run `/discoverEmail`
3. Agent converts emails to Markdown
4. Agent extracts all information

**Expected Result**:
- 5 emails processed: email/raw/ → email/ai/ (converted) → email/processed/ (archived)
- aiDocs/SUMMARY.md: 8 contacts added, background section populated, 3 risks identified
- aiDocs/TASKS.md: 12 tasks created (TASK-001 through TASK-012), priorities assigned
- aiDocs/DISCOVERY.md: 7 questions added about customer environment
- All placeholders replaced with actual project data

**Summary Report Shows**:
- Total emails processed: 5
- Contacts: 8 new (3 from Progress, 5 from Customer)
- Tasks: 12 created (4 high-priority, 8 planning)
- Risks: 3 identified (1 high, 2 medium)
- Discovery questions: 7 added

---

### Scenario 2: Weekly Email Update (Ongoing Project)
**Situation**: Project ongoing for 2 weeks, received 2 new status emails
**Input**: 2 .eml files from this week
**Steps**:
1. Add 2 new .eml files to email/raw/
2. Run `/discoverEmail`
3. Agent processes new emails only

**Expected Result**:
- 2 emails processed and moved
- aiDocs/SUMMARY.md: Current Situation updated, 1 decision added to Decision Log
- aiDocs/TASKS.md: 3 existing tasks marked complete, 2 new tasks added (TASK-013, TASK-014)
- aiDocs/DISCOVERY.md: 2 questions answered, 1 new question added
- Existing data preserved, only new info added

**Summary Report Shows**:
- Total emails processed: 2
- Tasks: 2 new created, 3 marked complete
- Decisions: 1 new (go-live date confirmed)
- Discovery questions: 2 answered, 1 new

---

### Scenario 3: Large Email Thread Import
**Situation**: Found old email thread (15 emails) discussing architecture decisions
**Input**: 15 .eml files from 3 months ago
**Steps**:
1. Export entire thread to email/raw/
2. Run `/discoverEmail`
3. Agent processes all chronologically

**Expected Result**:
- 15 emails processed
- aiDocs/SUMMARY.md: Historical Context section filled with timeline, 5 decisions captured
- Technical Details section updated with architecture info
- Conflicting information resolved (latest email wins)
- Email dates noted in sources

**Summary Report Shows**:
- Total emails processed: 15
- Contacts: 2 new, 3 updated
- Decisions: 5 added to Decision Log
- Conflicts: 2 identified and resolved
- Historical context: Timeline from 3 months ago populated
