---
description: Process notes files and update project documentation based on note content
---

You are an AI agent tasked with processing notes files and updating project documentation based on the information found in those notes.

**IMPORTANT**: This is an automated workflow. Do NOT ask for user confirmation or pause. Execute all steps completely and update all files as needed.

Follow these steps carefully:

## 1. Process Raw Notes Files

First, you need to convert any `.txt` or `.md` files in the `notes/raw/` directory to standardized Markdown format.

### Run the Notes Converter

Execute the notes converter script from the **project root** directory:

```bash
python3 "core/aiScripts/notesToMd/notes_to_md_converter.py"
```

The script will automatically:
1. Create required directories if they don't exist (`notes/raw/`, `notes/ai/`, `notes/processed/`)
2. Read all `.txt` and `.md` files from `notes/raw/`
3. Extract metadata (title, author, date)
4. Convert to standardized Markdown format
5. Save converted files to `notes/ai/` as `.md` files
6. Move processed files to `notes/processed/`

**Verify the move**: After running the script, check that:
- Original files have been moved from `notes/raw/` to `notes/processed/`
- Corresponding `.md` files exist in `notes/ai/`
- If files were not moved, report the error and check file permissions

## 2. Read ALL Notes Content

**CRITICAL**: You MUST read EVERY `.md` file in the `notes/ai/` directory completely.

### Notes Processing Guidelines

When reading notes:
- Note the date range (oldest to newest)
- Identify author if available
- Track main topics/themes discussed
- Look for meeting notes, decisions, action items

For each notes file:
- Read the entire content
- Extract ALL relevant information:
  - **Contacts**: Names, email addresses, roles, organizations
  - **Background**: Project history, context, meeting minutes
  - **Technical Details**: Technologies, architectures, configurations, requirements
  - **Current Status**: Latest updates, ongoing work, recent developments
  - **Historical Context**: Timeline events, past decisions, key milestones
  - **Tasks**: Action items, next steps, deliverables, assignments
  - **Questions**: Unanswered questions, information gaps, clarifications needed
  - **Risks**: Concerns, blockers, potential issues, challenges
  - **Decisions**: Agreements made, approaches chosen, plans approved

### Handling Conflicting Information

When notes contain contradictions:
1. **Use latest information**: Most recent note takes precedence
2. **Note the conflict**: In Current Situation, mention "Previously X, updated to Y (per note dated [date])"
3. **Flag for clarification**: Add discovery question if contradiction is significant
4. **Document both versions**: In Historical Context, note the change in understanding
5. **Escalate critical conflicts**: If affects major decisions, add to "Critical Findings" in summary

## 3. Update ALL Project Documentation Files

**MANDATORY**: You MUST update ALL relevant `aiDocs/` files based on notes content. Do not skip this step.

**Note on Templates**: If `aiDocs/` files are in their default template state (containing placeholders like `[DATE]`, `[CUSTOMER]`, `[PROJECT]`, etc.), the templates are located at:
- `core/templates/SUMMARY.template.md`
- `core/templates/TASKS.template.md`
- `core/templates/DISCOVERY.template.md`
- `core/templates/AI.template.md`

The working files in `aiDocs/` (without the `.template` extension) are the ones you should update. Replace all placeholders with actual content from notes.

### Update `aiDocs/SUMMARY.md`

**Required updates:**
- **Last Updated**: Set to current date

- **Quick Context**: Create/update 3-line summary with character limits:
  - **What**: Brief description (max 100 characters, one sentence only)
  - **Who**: Key organizations only (max 150 characters, format: "Company A supporting Company B")
  - **Status**: Current phase only (max 50 characters, use one of: Planning | Investigation | Active Development | Testing | Blocked | On Hold)

- **Key Contacts Reference**: Add/update ALL people mentioned in notes with their:
  - Full name
  - Email address (verify format is complete and correct)
  - Role/title
  - Organization
  - Phone numbers (include country/area codes if provided)
  - Group contacts by organization
  - **Deduplication**: Check for related organizations; merge duplicates

- **Background**: Write comprehensive background from note history
  - Cite note sources for key facts using format: (Source: "Note Title" - Date)

- **Historical Context**: Add timeline of key events from notes
  - Organize chronologically
  - Anything older than 30 days goes here
  - Use consistent date format throughout

- **Technical Details**: Document all technical information mentioned
  - Be specific (e.g., "MarkLogic 10.0-9.3" not just "MarkLogic")
  - Include version numbers, configurations, error codes

- **Current Situation**: Describe latest status from most recent notes
  - Focus on last 2 weeks of activity only
  - Recent progress = last 30 days

- **Decision Log**: Extract all decisions into table format:
  - Date of decision
  - What was decided
  - Who made the decision
  - Rationale/reason for decision (include note source)
  - Use consistent date format

- **Risks**: List all risks, concerns, or blockers mentioned
  - For each risk include all 8 required fields:
    - **Title**: Clear, concise risk name
    - **Description**: What could go wrong
    - **Severity**: Critical | High | Medium | Low
    - **Likelihood**: Certain | Likely | Possible | Unlikely
    - **Impact**: Specific consequences if risk occurs
    - **Mitigation**: What is being done to reduce/prevent
    - **Owner**: Who is responsible for monitoring/mitigating (or TBD)
    - **Status**: Active | Mitigated | Accepted | Transferred

### Update `aiDocs/TASKS.md`

**Required updates:**
- **Last Updated**: Set to current date

- **Outstanding Tasks**: Extract ALL action items and next steps from notes
  - Assign sequential task IDs: TASK-001, TASK-002, TASK-003, etc. (NO GAPS in new tasks)
  - Categorize by priority
  - For each task include:
    - **Owner**: Person responsible (if mentioned) or "TBD" (NEVER leave blank)
    - **Status**: Not Started | In Progress | Blocked | Completed
    - **Blocks**: Task IDs that depend on this task (verify IDs exist)
    - **Related**: Related task IDs (verify IDs exist)
    - **Source**: Which note the task came from (include title/date)
    - **Context**: Description and any mentioned deadlines
    - **Deadline**: Explicit deadline if mentioned

- **Completed Tasks**: Document any completed work mentioned in notes
  - Group by month if > 1 month old, by week if recent
  - Include source note reference

### Update `aiDocs/DISCOVERY.md`

**Required updates:**
- **Last Updated**: Set to current date

- Add ALL questions about the customer, their setup, or their environment
- For each discovery question include:
  - **Ask**: Who would know the answer (specific person/role)
  - **Check**: Where to look for the answer (specific notes, documents, people)
  - **Status**: Unknown / Partial / Answered
  - **Priority**: High / Medium / Low
  - **Answer**: If the note contains the answer, mark question as [x] and include the answer
  - **Source**: If answered, cite which note provided the answer (title and date)

### Update `aiDocs/AI.md` (if applicable)

Update the **AI Agent Notes** section if notes contain:
- **Project-Specific Guidance**: Customer preferences, technical constraints, important context
- **Common Pitfalls**: Issues to avoid, warnings from experience
- **Quick References**: Important URLs, documentation, key error codes
- **Lessons Learned**: What worked well or didn't work

## 4. Documentation Quality Requirements

When updating files:
- **Be thorough**: Include ALL relevant information from notes
- **Be specific**: Use exact names, dates, technologies, and details
- **Update dates**: Change "Last Updated" fields to current date
- **Replace placeholders**: Replace ALL `[DATE]`, `[CUSTOMER]`, `[PROJECT]`, etc. with actual content
- **Preserve structure**: Keep existing formatting and section organization
- **Be factual**: Only include information directly from notes
- **Cross-reference**: When documenting facts, note which note they came from

## 5. Validation Step

Before providing your summary, verify:
- [ ] All email addresses are correctly formatted and complete
- [ ] Phone numbers include country/area codes if provided
- [ ] All task IDs are sequential (gaps allowed for completed tasks)
- [ ] Every task has an Owner or "TBD" explicitly stated (never blank)
- [ ] All discovery questions have all required metadata fields populated
- [ ] Cross-references (Blocks, Related) use valid task IDs that exist
- [ ] Dates are in consistent format throughout
- [ ] Organization names are consistent throughout
- [ ] No template placeholders remain (`[DATE]`, `[CUSTOMER]`, etc.)
- [ ] Quick Context meets character limits (What: 100, Who: 150, Status: 50)

**Update State File**: After notes processing completes:
```python
python3 -c "
import sys
sys.path.insert(0, 'core/aiScripts')
from state_manager import increment_notes_count
increment_notes_count()
"
```

## 6. Mandatory Summary Report

After completing ALL updates to `aiDocs/` files, provide a comprehensive summary:

**Notes Processing Summary:**
- Total notes processed: [number]
- Notes read and analyzed: [list filenames]

**Documentation Updates Made:**
- `aiDocs/SUMMARY.md`: [Specific changes made]
- `aiDocs/TASKS.md`: [Specific changes made]
- `aiDocs/DISCOVERY.md`: [Specific changes made]
- `aiDocs/AI.md`: [Changes made, if any]

**Key Information Extracted:**
- **Contacts**: [number added] new contacts added, [number removed] removed
  - New: [list names and organizations]
- **Tasks**: [number created] new tasks created, [number completed] tasks marked complete
  - New outstanding tasks: [list TASK-IDs with brief description]
- **Risks**: [number added] new risks identified
- **Blockers**: [number added] new blockers identified
- **Discovery Questions**: [number added] new questions added, [number answered] questions answered

**Critical Findings:**
- Urgent items or blockers: [list any critical issues]
- Key decisions documented: [list important decisions]
- Unanswered questions: [list gaps in information]

## 7. Output Success Validation Checklist

After providing the mandatory summary report, validate the output with this checklist:

```
# ✅ Notes Processing Complete

## Validation Checklist

### Notes Processing
- [✓] notes/ai/ contains .md files (X files converted)
- [✓] notes/processed/ contains original files (X files archived)
- [✓] notes/raw/ is empty

### Required Files Updated
- [✓] aiDocs/SUMMARY.md updated
- [✓] aiDocs/TASKS.md updated
- [✓] aiDocs/DISCOVERY.md updated
- [✓] aiDocs/AI.md updated (if applicable)

### Content Quality
- [✓] SUMMARY.md Quick Context populated (What/Who/Status)
- [✓] SUMMARY.md has contacts with complete information
- [✓] TASKS.md has tasks with sequential IDs
- [✓] All task cross-references (Blocks, Related) are valid
- [✓] "Last Updated" dates set to current date
- [✓] Decision Log updated with new decisions
- [✓] Risks documented with all 8 required fields

### Structure Validation
- [✓] No placeholder text remains ([CUSTOMER], [PROJECT], [DATE])
- [✓] All required metadata fields populated
- [✓] Task IDs are sequential
- [✓] Every task has Owner or "TBD" (never blank)

## Success! 🎉

Your notes processing is complete and documentation updated.

**Next Steps:**
1. Run /updateSummary to regenerate PROJECT.md and docs/
2. Review aiDocs/ for extracted information
3. Add more notes to notes/raw/ as project progresses

**If any items are unchecked:**
- Check notes converter output for errors
- Verify files were valid text/markdown format
- Ensure Python 3.x installed
- Re-run /discoverNotes after fixing issues
```

## Critical Reminders

- **DO NOT skip updates**: You MUST update `aiDocs/` files based on notes content
- **DO NOT ask for confirmation**: This is an automated process
- **DO NOT leave placeholders**: Replace ALL `[DATE]`, `[CUSTOMER]`, `[PROJECT]`, etc. with actual content
- **DO read ALL notes**: Every `.md` file in `notes/ai/` must be read completely
- **DO be thorough**: Extract ALL relevant information from notes
- **DO update dates**: Set "Last Updated" fields to today's date
- **DO provide complete summary**: Include all metrics for contacts, tasks, risks, blockers
- Always run the notes converter from the project root directory
- If note content conflicts with existing documentation, update with the latest information and note the conflict in your summary

---

## Common Scenarios

### Scenario 1: First Notes Import (Meeting Minutes)
**Situation**: Just exported meeting minutes from OneNote, have 3 notes files
**Input**: 3 .txt files with meeting notes
**Steps**:
1. Place all .txt files in notes/raw/
2. Run `/discoverNotes`
3. Agent converts notes to Markdown
4. Agent extracts all information

**Expected Result**:
- 3 notes processed: notes/raw/ → notes/ai/ (converted) → notes/processed/ (archived)
- aiDocs/SUMMARY.md: 5 contacts added (meeting attendees), 2 decisions captured
- aiDocs/TASKS.md: 8 tasks created (action items from meetings)
- aiDocs/DISCOVERY.md: 4 questions added about customer environment
- All placeholders replaced with actual project data

**Summary Report Shows**:
- Total notes processed: 3
- Contacts: 5 new (meeting participants)
- Tasks: 8 created (all action items)
- Decisions: 2 captured from meeting
- Discovery questions: 4 added

---

### Scenario 2: Weekly Notes Update
**Situation**: Project ongoing, received 2 new daily standup notes
**Input**: 2 .md files with standup notes
**Steps**:
1. Add 2 new .md files to notes/raw/
2. Run `/discoverNotes`
3. Agent processes new notes only

**Expected Result**:
- 2 notes processed and moved
- aiDocs/SUMMARY.md: Current Situation updated with progress
- aiDocs/TASKS.md: 2 existing tasks marked complete, 1 new task added
- aiDocs/DISCOVERY.md: 1 question answered
- Existing data preserved, only new info added

**Summary Report Shows**:
- Total notes processed: 2
- Tasks: 1 new created, 2 marked complete
- Discovery questions: 1 answered

---

### Scenario 3: Large Notes Collection Import
**Situation**: Found project folder with 10 notes files spanning 2 months
**Input**: 10 .txt/.md files from historical project notes
**Steps**:
1. Export all notes to notes/raw/
2. Run `/discoverNotes`
3. Agent processes all chronologically

**Expected Result**:
- 10 notes processed
- aiDocs/SUMMARY.md: Historical Context section filled with timeline
- Technical Details section updated with architecture info
- Conflicting information resolved (latest note wins)
- Note dates noted in sources

**Summary Report Shows**:
- Total notes processed: 10
- Contacts: 3 new, 2 updated
- Decisions: 4 added to Decision Log
- Historical context: Timeline from 2 months ago populated
- Tasks: 15 created from action items
