# Changelog

All notable changes to Lumina will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-06

### Added
- **Notes Processing** - Complete notes-to-Markdown workflow supporting 5 formats (#53)
  - Plain text (.txt) and Markdown (.md)
  - OneNote exports (.docx) (#68)
  - Apple Notes exports (.html) (#70)
  - Bear notes (.textbundle) (#69)
- **Dependency Management** - Interactive dependency checker and installer
  - Auto-detects missing optional dependencies
  - Shows format support status on startup
  - Interactive installation workflow
  - Graceful degradation without optional deps
- **PDF Export** - Professional LaTeX-based PDF generation
  - Complete LaTeX dependency management
  - Custom styling and formatting
  - Export project documentation to PDF
- **Backup & Restore** - Project state management (#51)
  - Backup current project state
  - Restore from previous backups
  - List available backups
  - Integrated into go.sh menu
- **State Tracking** - Project initialization tracking (#33)
  - Tracks email/notes processing counts
  - Records last summary update
  - Persistent state across sessions
- **Comprehensive Tests** - Expanded test coverage
  - Notes converter tests (7 tests)
  - Integration tests for full workflow
  - Smoke tests for all critical paths (#48)
  - Total: 58+ tests (all passing)
- **Writing Style Guidelines** - Professional documentation standards
  - Consultant voice and tone guidelines
  - Clear structure and formatting rules
  - Anti-patterns and preferred patterns

### Enhanced
- **go.sh Menu** - Improved interactive menu
  - "Lumina Prompts" quick access
  - "Manage Dependencies" option
  - "Process Notes" workflow
  - Removed redundant "Validate Project" option
- **Documentation** - Enhanced clarity throughout
  - Concrete usage examples for all prompts (#52)
  - Streamlined Quick Start instructions
  - Better sample project section
  - Notes workflow documentation (#54)
- **clean-reset.sh** - Enhanced to handle notes directories
  - Clears notes/raw, notes/ai, notes/processed
  - Validates directory structure
  - Comprehensive cleanup

### Fixed
- **Sanity Check** - Better branch validation logic
  - Correctly handles feature/defect branches
  - Validates all changes since branching from main
- **Documentation Links** - Corrected relative paths in prompts (#49)
- **Code Cleanup** - Removed unnecessary blank lines
  - go.sh process functions
  - health-check prompt

### Refactored
- **Template Naming** - Standardized template file names
  - Clear distinction between aiDocs and docs templates
  - Consistent .template.md extension
- **Prompt Naming** - initSampleProject (was endToEndTest)
  - More descriptive and clear purpose
- **Menu Options** - User-focused language
  - "Process Emails" instead of "Health Check"
  - Clearer action-oriented labels

### Documentation
- Quick Reference Card updated
- All workflow prompts include concrete scenarios
- Dependency management fully documented
- Notes processing workflow explained

---

## [1.0.0] - 2026-01-06

### Added
- **Email Processing** - Email to Markdown converter (eml_to_md_converter.py)
  - Parse .eml files from raw email exports
  - Convert to structured Markdown
  - Preserve metadata and formatting
  - Handle attachments
- **Task Dependency Detection** - Automated relationship discovery
  - 3-tier confidence scoring (high/medium/low)
  - Circular dependency detection
  - Dependency graph visualization
  - Automated report generation
- **AI Workflow Prompts** - 10 comprehensive prompts
  - ProjectInit - Initialize agent context
  - discoverEmail - Process email data
  - discoverNotes - Process notes data (v1.1)
  - updateSummary - Generate project documentation
  - quickStartProject - Complete initialization workflow
  - validateTasks - Task structure validation
  - cleanupTasks - Task maintenance and optimization
  - generateReport - Executive status reports
  - syncFromProject - Reverse sync from PROJECT.md
  - completeIssue - GitHub issue to PR workflow
- **Interactive Menu** - go.sh menu system
  - Initialize Project
  - Process Emails
  - Manage Dependencies
  - Export to PDF
  - Reset Project
  - User-friendly navigation
- **Documentation Templates** - Structured project docs
  - aiDocs/ - AI agent context (SUMMARY, TASKS, DISCOVERY, AI)
  - docs/ - Human-readable extracts (CONTACTS, TASKS, DECISIONS, QUESTIONS)
  - PROJECT.md - Executive summary
- **Test Suite** - Comprehensive validation
  - Shell script syntax tests (21 tests)
  - Email converter tests (7 tests)
  - Task detector tests (7 tests)
  - Fast execution (< 1 second)
- **Git Integration** - Pre-commit hooks
  - Automatic syntax validation
  - Commit message format checking
  - Branch name validation

### Features
- **Email-to-Documentation Pipeline** - Complete workflow
  - Export emails → process → generate docs
  - Automatic contact extraction
  - Task identification and tracking
  - Risk and decision logging
- **Task Management** - Sophisticated tracking
  - Sequential task IDs (TASK-001, TASK-002, ...)
  - Cross-references (Blocks, Related)
  - Priority categorization
  - Dependency detection
- **Discovery Questions** - Information gap tracking
  - Structured question format
  - Priority levels
  - Answer tracking with sources
- **Risk Management** - 8-field risk format
  - Severity, Likelihood, Impact
  - Mitigation strategies
  - Owner assignment
  - Status tracking
- **Decision Log** - Historical record
  - Date, Decision, Made By, Rationale
  - Source citation
  - Searchable history

### Developer Experience
- Clear documentation (README.md, CONTRIBUTING.md)
- Git branching strategy (feature/, defect/)
- Conventional commits
- GitHub issue/PR templates
- Pre-commit validation

### Security
- .gitignore for sensitive data
  - Email files excluded
  - Virtual environments excluded
  - Credentials and keys excluded
- No hardcoded secrets
- Safe file operations

---

## Release Notes

### v1.1.0 Highlights

This release significantly expands Lumina's capabilities with **complete notes processing**, **dependency management**, and **professional PDF export**. The notes converter now supports 5 different formats, making it easy to import from any note-taking app. The new dependency checker ensures users have the tools they need while gracefully degrading for optional features.

**Key additions:**
- 📝 Process notes from 5 different formats
- 🔧 Interactive dependency management
- 📄 Professional PDF export with LaTeX
- 💾 Backup and restore project states
- 📊 58+ comprehensive tests
- 🎨 Professional writing guidelines

### v1.0.0 Highlights

The initial release of Lumina provides a complete email-to-documentation pipeline for MarkLogic consultants. Export email threads, run one command, and get comprehensive project documentation including contacts, tasks, risks, and decisions.

**Core features:**
- 📧 Email processing with automatic extraction
- 📋 Task management with dependency detection
- 🤖 10 AI workflow prompts
- ✅ Comprehensive test suite
- 🎯 Interactive menu system
- 📚 Professional documentation templates

---

[1.1.0]: https://github.com/nlaprell/lumina/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/nlaprell/lumina/releases/tag/v1.0.0
