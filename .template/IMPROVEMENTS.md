# Bootstrap Project Improvements

**⚠️ DEPRECATED - Use GitHub Issues Instead**

*Last Updated: December 22, 2025*

This file is maintained for reference only. **All template work is now tracked in [GitHub issues](https://github.com/nlaprell/lumina/issues) instead of markdown files.**

## Migration to GitHub

- **Previous Format**: `.template/IMPROVEMENTS.md`, `.template/FIXES.md` (deprecated)
- **Current Format**: [GitHub issues](https://github.com/nlaprell/lumina/issues) (single source of truth)
- **Workflow**: Use `/healthCheck` → `/reportToGitHub` to create issues

## Why GitHub?

1. **Single source of truth** - One place for all template work
2. **Better tracking** - Assign, label, and track progress
3. **No duplication** - Eliminates maintenance burden of markdown files
4. **Project boards** - Organize work by milestone and status
5. **Collaboration** - Comments, reviews, and discussions

## How to Use

When you find improvements needed:

1. Open a GitHub issue: https://github.com/nlaprell/lumina/issues/new
2. Add appropriate labels (`enhancement`, `quality`, `documentation`, etc.)
3. Assign to a milestone (`v1.0.0 - MVP`, `v1.1.0 - Post-MVP`)
4. Track progress through GitHub

**Do NOT** add improvements to this file. This file is archived for reference only.

---

## Archived Improvements (From December 15, 2025)

Below are improvements identified from previous health checks. These are now tracked as GitHub issues.

---

## High Impact Improvements

These improvements would significantly enhance the bootstrap system.

### TASK-027: Build Minimal VS Code Extension for Custom Slash Commands

**Priority**: High  
**Category**: Feature - VS Code Integration  
**Component**: New directory: .vscode-extension/  
**Effort**: Medium (4-6 hours)  
**Impact**: High  

**Problem**:
Current `.prompt.md` files are configured in `settings.json` as `github.copilot.chat.codeGeneration.instructions`, but they don't create actual slash commands. Users cannot type `/` in Copilot Chat and see custom prompts in autocomplete. The only way to discover prompts is by reading documentation or remembering filenames.

**Current Behavior**:
- Prompts must be typed manually or copied from documentation
- No autocomplete when typing `/` in chat
- No native integration with VS Code Chat API
- Prompts appear as context but not as commands

**Expected Behavior**:
- Type `@copilotTemplate /` in chat to see all available prompts
- Autocomplete shows prompt names with descriptions
- Commands execute by loading `.prompt.md` file content
- Extension auto-discovers prompts from `prompts/` directory
- Works locally without marketplace deployment

**Proposed Solution**:

Create a lightweight TypeScript VS Code extension with Chat Participant API:

**Directory Structure**:
```
.vscode-extension/
├── package.json              # Extension manifest
├── tsconfig.json            # TypeScript config
├── .vscodeignore            # Files to exclude from VSIX
├── src/
│   ├── extension.ts         # Main extension entry point
│   └── promptLoader.ts      # Auto-discover and load prompts
└── README.md                # Extension documentation
```

**package.json** (key parts):
```json
{
  "name": "lumina-prompts",
  "displayName": "Lumina - Project Prompts",
  "version": "1.0.0",
  "engines": { "vscode": "^1.85.0" },
  "categories": ["AI", "Chat"],
  "activationEvents": ["onStartupFinished"],
  "main": "./out/extension.js",
  "contributes": {
    "chatParticipants": [
      {
        "id": "copilotTemplate",
        "name": "copilotTemplate",
        "description": "Project documentation workflow prompts",
        "isSticky": true
      }
    ]
  }
}
```

**src/extension.ts**:
```typescript
import * as vscode from 'vscode';
import * as fs from 'fs/promises';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
    const handler: vscode.ChatRequestHandler = async (
        request: vscode.ChatRequest,
        chatContext: vscode.ChatContext,
        stream: vscode.ChatResponseStream,
        token: vscode.CancellationToken
    ) => {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            stream.markdown('No workspace folder open.');
            return { metadata: { command: '' } };
        }

        // Load prompt file based on command
        const promptFile = path.join(
            workspaceFolder.uri.fsPath,
            'prompts',
            `${request.command}.prompt.md`
        );

        try {
            const content = await fs.readFile(promptFile, 'utf8');
            // Strip YAML frontmatter (---...---)
            const markdown = content.replace(/^---[\s\S]*?---\n/, '');
            stream.markdown(markdown);
        } catch (error) {
            stream.markdown(`Error: Could not load prompt "${request.command}"`);
        }

        return { metadata: { command: request.command || '' } };
    };

    const participant = vscode.chat.createChatParticipant('copilotTemplate', handler);
    participant.iconPath = new vscode.ThemeIcon('file-directory');

    // Auto-discover prompts from prompts/ directory
    discoverPrompts(participant);

    context.subscriptions.push(participant);
}

async function discoverPrompts(participant: vscode.ChatParticipant) {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) return;

    const promptsDir = path.join(workspaceFolder.uri.fsPath, 'prompts');
    
    try {
        const files = await fs.readdir(promptsDir);
        const commands: vscode.ChatCommand[] = [];

        for (const file of files) {
            if (file.endsWith('.prompt.md')) {
                const name = file.replace('.prompt.md', '');
                const filePath = path.join(promptsDir, file);
                const description = await extractDescription(filePath);
                
                commands.push({ name, description });
            }
        }

        participant.commands = commands;
    } catch (error) {
        console.error('Failed to discover prompts:', error);
    }
}

async function extractDescription(filePath: string): Promise<string> {
    try {
        const content = await fs.readFile(filePath, 'utf8');
        const match = content.match(/^---\s*\ndescription:\s*(.+?)\s*\n/m);
        return match ? match[1] : 'Project workflow prompt';
    } catch {
        return 'Project workflow prompt';
    }
}
```

**Installation & Usage**:

1. Build extension:
   ```bash
   cd .vscode-extension
   npm install
   npm run compile
   ```

2. Install locally (no marketplace needed):
   ```bash
   # Package as VSIX
   npx vsce package
   
   # Install in VS Code
   code --install-extension lumina-prompts-1.0.0.vsix
   ```

   OR symlink for development:
   ```bash
   ln -s "$(pwd)/.vscode-extension" \
     "$HOME/.vscode/extensions/lumina-prompts-1.0.0"
   ```

3. Usage in VS Code:
   - Type `@copilotTemplate /` in Copilot Chat
   - Autocomplete shows: `projectInit`, `discoverEmail`, `updateSummary`, etc.
   - Select command and press Enter
   - Prompt content loads into chat automatically

**Location**:
- New directory: `.vscode-extension/` at project root
- Update `.gitignore` to exclude `node_modules/` and `out/`
- Update `README.md` with extension installation instructions

**Dependencies**:
- Blocks: None (prompts continue working via settings.json during development)
- Requires: Node.js, npm, VS Code 1.85+
- Related: TASK-002 (can remove settings.json entries once extension is active)

**Acceptance Criteria**:
- [ ] Extension created in `.vscode-extension/` directory
- [ ] TypeScript compiles without errors
- [ ] Extension packages as VSIX successfully
- [ ] Local installation works (symlink or VSIX install)
- [ ] Chat participant `@copilotTemplate` appears in VS Code
- [ ] Typing `@copilotTemplate /` shows all prompts in autocomplete
- [ ] Selecting `/projectInit` loads prompt content correctly
- [ ] All 11 prompts (8 user + 3 bootstrap) auto-discovered
- [ ] YAML frontmatter stripped from loaded prompts
- [ ] Works without marketplace deployment
- [ ] Documentation added to README.md

**References**:
- Architecture Review Recommendation #1
- VS Code Chat Participant API: https://code.visualstudio.com/api/extension-guides/chat
- vsce packaging tool: https://github.com/microsoft/vscode-vsce

---

### TASK-024: Add Terminal Color Support Detection

**Priority**: Low  
**Category**: Code Quality  
**Component**: init.sh  
**Effort**: Low (1 hour)  
**Impact**: Low  

**Problem**:
init.sh uses hard-coded ANSI color codes without checking if terminal supports colors. May show escape codes on terminals without color support.

**Current Behavior**:
Color codes defined as magic strings; always displayed regardless of terminal capability.

**Expected Behavior**:
Check terminal capabilities before using colors; fall back to no colors if unsupported.

**Proposed Solution**:
Add color capability detection at start of script:
```bash
# Check if terminal supports colors
if [ -t 1 ] && command -v tput &> /dev/null && [ $(tput colors) -ge 8 ]; then
    GREEN=$(tput setaf 2)
    BLUE=$(tput setaf 4)
    YELLOW=$(tput setaf 3)
    RED=$(tput setaf 1)
    NC=$(tput sgr0)
else
    GREEN=''
    BLUE=''
    YELLOW=''
    RED=''
    NC=''
fi
```

**Location**:
- File: `init.sh`
- Lines: 8-12

**Dependencies**:
- Blocks: None
- Requires: None
- Related: None

**Acceptance Criteria**:
- [ ] Terminal color support detected
- [ ] tput used for portable color codes
- [ ] Graceful fallback to no colors
- [ ] Test on terminal without color support
- [ ] Test on terminal with color support

**References**:
- Sanity Check Issue: ISSUE-024

---

### TASK-025: Add .editorconfig for Consistent Formatting

**Priority**: Low  
**Category**: Best Practice  
**Component**: Root directory  
**Effort**: Low (1 hour)  
**Impact**: Medium  

**Problem**:
Project lacks .editorconfig file to enforce consistent indentation and line endings across contributors. Potential formatting inconsistencies in contributed files.

**Current Behavior**:
No automated formatting enforcement.

**Expected Behavior**:
.editorconfig provides consistent formatting rules for all file types.

**Proposed Solution**:
Create .editorconfig in project root:
```ini
# EditorConfig for Lumina
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
indent_style = space
indent_size = 2
trim_trailing_whitespace = false

[*.{py,sh}]
indent_style = space
indent_size = 4

[*.{json,yml,yaml}]
indent_style = space
indent_size = 2

[*.sh]
end_of_line = lf

[Makefile]
indent_style = tab
```

**Location**:
- New file: `.editorconfig` at project root

**Dependencies**:
- Blocks: None
- Requires: None
- Related: None

**Acceptance Criteria**:
- [ ] .editorconfig created
- [ ] Rules for all file types used in project
- [ ] Markdown, Python, Bash, JSON configured
- [ ] Line ending consistency enforced (LF)
- [ ] Trailing whitespace handling appropriate per file type
- [ ] Test with different editors (VS Code, vim, etc.)

**References**:
- Sanity Check Issue: ISSUE-025
- EditorConfig.org specification

---

## Medium Impact Improvements

These improvements would provide noticeable benefits.

### TASK-026: Add Pre-Commit Hook for Placeholder Detection

**Priority**: Medium  
**Category**: Quality Assurance  
**Component**: New file: .git/hooks/pre-commit  
**Effort**: Low (2 hours)  
**Impact**: Medium  

**Problem**:
No automated detection if aiDocs files still contain template placeholders like [DATE], [CUSTOMER], [PROJECT] before allowing commit. Users may accidentally commit placeholder text.

**Current Behavior**:
No pre-commit validation of placeholder removal.

**Expected Behavior**:
Git pre-commit hook detects placeholders and blocks commit with helpful message.

**Proposed Solution**:
Create pre-commit hook script:
```bash
#!/bin/bash
# Pre-commit hook to detect template placeholders

PLACEHOLDER_PATTERN='\[(DATE|CUSTOMER|PROJECT|NAME|EMAIL|TASK|PERSON)\]'

# Check aiDocs files
if git diff --cached --name-only | grep -q '^aiDocs/'; then
    if git diff --cached | grep -E "$PLACEHOLDER_PATTERN" > /dev/null; then
        echo "ERROR: Template placeholders detected in aiDocs/"
        echo "Please replace all [PLACEHOLDER] text before committing"
        git diff --cached | grep -E "$PLACEHOLDER_PATTERN"
        exit 1
    fi
fi

exit 0
```

Also create script to install hook: `scripts/install-hooks.sh`

**Location**:
- New file: `.git/hooks/pre-commit`
- New file: `scripts/install-hooks.sh`

**Dependencies**:
- Blocks: None
- Requires: None
- Related: TASK-020 (Quick Context validation could be added to this hook)

**Acceptance Criteria**:
- [ ] Pre-commit hook script created
- [ ] Detects common placeholder patterns
- [ ] Blocks commit if placeholders found
- [ ] Shows which placeholders were found
- [ ] Clear error message with resolution steps
- [ ] install-hooks.sh script for easy setup
- [ ] README updated with hook installation instructions

**References**:
- Sanity Check Issue: ISSUE-026

---

### TASK-027: Create Quick Reference Card

**Priority**: Medium  
**Category**: Documentation  
**Component**: New file: QUICKREF.md  
**Effort**: Low (1-2 hours)  
**Impact**: Medium  

**Problem**:
No one-page quick reference showing common commands, slash commands, and workflow steps. Users must read full README to find basic information.

**Current Behavior**:
Information scattered across README, prompts, and documentation.

**Expected Behavior**:
Single-page quick reference with essential commands and decision tree.

**Proposed Solution**:
Create QUICKREF.md with sections:
```markdown
# Lumina Quick Reference

## Essential Commands

### Setup (One Time)
- `./.template/scripts/init.sh` - Configure project and MCP servers
- `./.template/scripts/clean-reset.sh` - Reset to clean state

### Email Processing
- Place emails in: `email/raw/`
- Run: `/discoverEmail` in Copilot

### Workflows (Slash Commands)
- `/quickStartProject` - Complete init workflow
- `/projectInit` - Initialize AI context
- `/discoverEmail` - Process emails
- `/updateSummary` - Generate summary
- `/sanityCheck` - Run bootstrap validation
- `/healthCheck` - Comprehensive QA analysis
- `/reportToGitHub` - Create GitHub issues from findings

## Decision Tree

**First time using template?**
→ Run `./.template/scripts/init.sh`
→ Add emails to `email/raw/`
→ Run `/quickStartProject`

**Adding more emails later?**
→ Add to `email/raw/`
→ Run `/discoverEmail`
→ Run `/updateSummary`

**Need project status summary?**
→ Run `/updateSummary`
→ Check `SUMMARY.md`

**Want to analyze template health?**
→ Run `/sanityCheck`
→ Review `.template/SANITY_CHECK_REPORT.md`

## File Locations

- **Project docs**: `aiDocs/`
- **Email context**: `email/ai/`
- **Task list**: `aiDocs/TASKS.md`
- **Project summary**: `SUMMARY.md` (root)
- **Template tasks**: `.template/FIXES.md`, `.template/IMPROVEMENTS.md`
```

**Location**:
- New file: `QUICKREF.md` at project root

**Dependencies**:
- Blocks: None
- Requires: None
- Related: TASK-006 (README improvements)

**Acceptance Criteria**:
- [ ] QUICKREF.md created
- [ ] All slash commands listed
- [ ] Decision tree for common scenarios
- [ ] File locations quick reference
- [ ] Fits on one printed page (or close)
- [ ] Link from README to QUICKREF
- [ ] Clear, scannable format

**References**:
- Sanity Check Issue: ISSUE-027

---

### TASK-028: Add Bootstrap Analysis Directory

**Priority**: Medium  
**Category**: Project Structure  
**Component**: .template/  
**Effort**: Low (< 1 hour)  
**Impact**: Low  

**Problem**:
Template prompts reference `.template/analysis/` directory but it doesn't exist. Generated reports need a consistent location.

**Current Behavior**:
Reports saved to .template/ root, creating clutter.

**Expected Behavior**:
Dedicated analysis/ subdirectory for all generated reports.

**Proposed Solution**:
1. Create `.template/analysis/` directory
2. Add .gitkeep to preserve in git
3. Update sanityCheck prompt to save to `.template/analysis/SANITY_CHECK_REPORT.md`
4. Move existing SANITY_CHECK_REPORT.md if present
5. Add README explaining directory purpose

**Location**:
- New directory: `.template/analysis/`
- Update: `.template/prompts/sanityCheck.prompt.md`

**Dependencies**:
- Blocks: None
- Requires: None
- Related: None

**Acceptance Criteria**:
- [ ] .template/analysis/ directory created
- [ ] .gitkeep added
- [ ] README.md in analysis/ explains purpose
- [ ] sanityCheck prompt updated to use new location
- [ ] Existing reports moved if present

**References**:
- Sanity Check Report: Project Structure findings

---

### TASK-029: Add MCP Config to .gitignore

**Priority**: Medium  
**Category**: Best Practice  
**Component**: .gitignore  
**Effort**: Low (< 1 hour)  
**Impact**: Low  

**Problem**:
`.vscode/mcp.json` not in .gitignore but could contain sensitive paths or configuration specific to individual developer machines.

**Current Behavior**:
mcp.json may be committed with user-specific or sensitive paths.

**Expected Behavior**:
mcp.json ignored by default; each developer runs init.sh to create their own.

**Proposed Solution**:
Add to .gitignore:
```
# MCP configuration (user-specific)
.vscode/mcp.json
```

Add note to README about running init.sh on clone.

**Location**:
- File: `.gitignore`

**Dependencies**:
- Blocks: None
- Requires: None
- Related: None

**Acceptance Criteria**:
- [ ] .vscode/mcp.json added to .gitignore
- [ ] README notes mcp.json is user-specific
- [ ] init.sh instructions emphasize re-running after clone
- [ ] Example mcp.json.template provided (optional)

**References**:
- Sanity Check Report: Project Structure findings

---

## Low Impact Improvements

These are polish and optimization improvements.

### TASK-030: Add Troubleshooting Section to README

**Priority**: Low  
**Category**: Documentation  
**Component**: README.md  
**Effort**: Medium (2-3 hours)  
**Impact**: High  

**Problem**:
No troubleshooting guide for common issues. Users get stuck on common problems without guidance.

**Current Behavior**:
Users must search through issues or ask for help.

**Expected Behavior**:
README has troubleshooting section addressing common problems.

**Proposed Solution**:
Add section to README before conclusion:
```markdown
## Troubleshooting

### Python 3 Not Found
**Error**: `python3: command not found`
**Solution**: Install Python 3.8+ from https://python.org

### Email Converter Fails
**Error**: Email conversion errors
**Solutions**:
- Check email file encoding (UTF-8 recommended)
- Ensure .eml files are valid email format
- Run with `python3 -v` for detailed errors
- Check file permissions in email/ directories

### Prompts Not Available in Copilot
**Error**: Slash commands don't work
**Solutions**:
- Verify files exist in prompts/
- Check .vscode/settings.json references prompts
- Reload VS Code window
- Ensure GitHub Copilot extension enabled

### Task IDs Have Gaps
**Info**: This is normal!
**Explanation**: When tasks complete, they move to archive. Gaps in outstanding task IDs are expected.

### MCP Server Selection Hangs
**Error**: init.sh freezes at server selection
**Solutions**:
- Press arrow keys (not Enter) to navigate
- Press Space to toggle selection
- Navigate to "Confirm Selection" and press Enter
- Use Ctrl+C to cancel and restart
```

**Location**:
- File: `README.md`
- Add section before final conclusion

**Dependencies**:
- Blocks: None
- Requires: None
- Related: TASK-006 (README improvements)

**Acceptance Criteria**:
- [ ] Troubleshooting section added
- [ ] Common issues documented
- [ ] Clear solutions provided
- [ ] Links to relevant documentation
- [ ] Covers Python, email, MCP, and prompt issues

**References**:
- Sanity Check Report: User Experience Analysis

---

## Future Enhancements

These are aspirational features that would significantly enhance the template system but are not yet scoped as actionable tasks. When ready to implement, convert to proper tasks with TASK-IDs.

### Change Detection and Diff Reports
**Category:** Audit & Tracking  
**Effort:** Medium  
**Impact:** Medium

Generate automated change reports:
- Track changes between workflow runs
- Generate human-readable diff reports
- Highlight critical changes (new blockers, completed tasks, answered questions)
- Email notification for significant changes
- Change log with attribution

**Implementation approach:**
- Add change tracking to workflow prompts
- Create `.template/aiScripts/generateChangeReport.py`
- Store snapshots for comparison
- Generate Markdown change reports

---

### Risk Scoring System
**Effort:** Low  
**Impact:** Medium

Calculate and track risk metrics:
- Calculate risk scores (Severity × Likelihood)
- Auto-prioritize risk mitigation
- Track risk trends over time
- Flag risks exceeding threshold

---

### Validation Scripts Suite
**Effort:** Low  
**Impact:** High

Complete validation tooling:
- `./.template/scripts/validate-all.sh` - Run all quality checks
- `./.template/scripts/check-references.sh` - Verify all cross-references
- `./.template/scripts/lint-tasks.sh` - Task ID and metadata validation
- Exit codes for CI/CD integration

---

### CSV Export Capability
**Effort:** Low  
**Impact:** Medium

Export documentation to standard formats:
- Export tasks to CSV for project management tools
- Export contacts to CSV for CRM import
- Export risks to CSV for risk registers
- Command: `./scripts/export-to-csv.sh [tasks|contacts|risks]`

---

### Meeting Notes Template
**Effort:** Low  
**Impact:** Low

Structured meeting capture:
- Add `aiDocs/templates/MEETING_NOTES.template.md`
- Include: Date, Attendees, Decisions, Action Items, Next Meeting
- Auto-extract tasks from meeting notes
- Link meeting notes to decision log

---

### Integration with Project Management Tools
**Effort:** High  
**Impact:** Medium

Two-way sync with PM tools:
- Two-way sync with Jira, Asana, Trello
- Export tasks to PM tools
- Import status updates back to TASKS.md
- Maintain task ID mapping

---

### Multi-Project Support
**Effort:** High  
**Impact:** Medium

Manage multiple projects in one workspace:
- Support multiple projects in one workspace
- Separate aiDocs/ per project
- Consolidated cross-project view
- Shared contact database

---

### Timeline Visualization
**Effort:** Medium  
**Impact:** Low

Visual project timeline:
- Generate Gantt charts from tasks
- Timeline view of Historical Context
- Milestone tracking
- Export to PNG/SVG

---

### AI Agent Learning System
**Effort:** High  
**Impact:** Medium

Adaptive AI assistance:
- Track which AI suggestions are accepted/rejected
- Learn from user corrections
- Improve extraction accuracy over time
- Personalized workflows per user

---

### Interactive Dashboard
**Effort:** High  
**Impact:** Medium

Web-based project dashboard:
- Project health metrics
- Task completion trends
- Risk heat maps
- Contact network graphs
- Discovery question status
- Real-time updates as files change
- Export dashboard to PDF

---

## Completed Improvements

### December 9, 2025

[Improvements will be moved here as they are completed]

---

## Notes

- This file tracks all improvements to the bootstrap template itself
- For critical bugs and fixes, see `.template/FIXES.md`
- **Active Tasks** have TASK-IDs and are ready to implement
- **Future Enhancements** are aspirational ideas without TASK-IDs yet
- High impact improvements should be prioritized even if effort is higher
- Many active tasks can be done in parallel (no blocking dependencies)

## How to Add New Ideas

**For actionable improvements from health checks:**
1. Add to appropriate priority section (High/Medium/Low Impact)
2. Use full task format with TASK-ID, acceptance criteria, etc.
3. Assign sequential TASK-ID

**For aspirational future ideas:**
1. Add to "Future Enhancements" section
2. Include brief description, effort, impact
3. No TASK-ID needed yet
4. Convert to proper task when ready to implement
