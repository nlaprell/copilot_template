# Lumina Roadmap

This roadmap outlines the planned development path for the Lumina bootstrap system.

---

## v1.0.0 - MVP Release 🎯

**Target Date:** December 31, 2025  
**Status:** In Progress  
**Milestone:** [v1.0.0 - MVP Release](https://github.com/nlaprell/lumina/milestone/1)

Production-ready MVP for MarkLogic consultants with critical stability fixes, logging, health checks, and essential UX improvements.

### Critical Fixes (Must Have)

- [x] ~~#4 - Add Basic Smoke Tests~~ (closed as duplicate of #9)
- [x] ~~#5 - Create Centralized Logging System~~ (closed as duplicate of #7)
- [ ] **#1** - 🔴 Fix MCP Configuration Format (servers vs mcpServers)
  - **Priority:** CRITICAL
  - **Impact:** Template currently broken for MCP server usage
  - **Effort:** Low (~30 minutes)

- [ ] **#8** - 🔴 Add error handling and recovery to email converter
  - **Priority:** CRITICAL
  - **Impact:** Prevents data loss from failed email conversions
  - **Effort:** Medium (1-2 hours)

- [ ] **#10** - 🔴 Add requirements.txt and remove runtime auto-install
  - **Priority:** CRITICAL
  - **Impact:** Fixes dependency management anti-pattern
  - **Effort:** Low (~1 hour)

### Essential Features (Should Have)

- [ ] **#7** - Add centralized logging module
  - **Priority:** HIGH
  - **Impact:** Enables debugging when failures occur
  - **Effort:** Low (~1 hour)

- [ ] **#6** - Add health check to go.sh menu
  - **Priority:** HIGH
  - **Impact:** Catches problems early, prevents runtime failures
  - **Effort:** Low (~1 hour)

- [ ] **#12** - Add decision tree / quick reference cheat sheet
  - **Priority:** HIGH
  - **Impact:** Dramatically improves onboarding UX
  - **Effort:** Low (<1 hour)

- [ ] **#13** - Add success validation checklist after workflows
  - **Priority:** HIGH
  - **Impact:** Builds consultant confidence in output
  - **Effort:** Low (<1 hour)

### Quality Improvements (Could Have)

- [ ] **#2** - Add MCP Configuration Validation to init.sh
  - **Priority:** MEDIUM
  - **Impact:** Validates MCP config before writing
  - **Effort:** Low (~30 minutes)

- [ ] **#3** - Improve Error Handling in Bash Scripts
  - **Priority:** MEDIUM
  - **Impact:** Better error messages and graceful failures
  - **Effort:** Medium (1-2 hours)

### Estimated Total Effort

**6-8 hours** to complete all MVP work

---

## v1.1.0 - Post-MVP Enhancements 🚀

**Target Date:** Q1 2026  
**Status:** Planned  
**Milestone:** [v1.1.0 - Post-MVP Enhancements](https://github.com/nlaprell/lumina/milestone/2)

Enhancements to improve onboarding experience, maintainability, and advanced features.

### Documentation & Examples

- [ ] **#14** - Add sample project documentation for reference
  - **Priority:** MEDIUM
  - **Impact:** Provides learning reference and quick demo
  - **Effort:** Medium (2-3 hours)

### Testing & Quality

- [ ] **#9** - Add smoke tests for critical code paths
  - **Priority:** MEDIUM
  - **Impact:** Improves maintainability and regression protection
  - **Effort:** Medium (1-2 hours)

### Advanced Features

- [ ] **#11** - Add state tracking for project initialization
  - **Priority:** LOW
  - **Impact:** Enhanced UX with better error messages
  - **Effort:** Medium (1-2 hours)

### Estimated Total Effort

**5-7 hours** for v1.1.0 enhancements

---

## Future Considerations (v1.2.0+)

**Status:** Backlog

Ideas for future releases (not yet scoped):

### Integration Enhancements
- Azure DevOps integration
- Jira ticket linking
- Slack notifications for status reports
- Email export automation (Outlook plugin)

### Advanced Features
- Multi-project workspace support
- Team collaboration features
- Advanced dependency visualization
- Automated weekly status reports
- Custom template creation wizard

### Quality of Life
- VS Code extension for common workflows
- CLI tool for command-line usage
- Configuration profiles for different project types
- Template customization without forking

---

## Release Process

### Pre-Release Checklist

1. All milestone issues closed
2. `/sanityCheck` passes with 0 critical issues
3. `/healthCheck` shows no major problems
4. Manual testing on sample emails
5. README.md updated with new features
6. CHANGELOG.md updated with release notes
7. Version bump in relevant files

### Release Steps

1. Merge all PRs to `main`
2. Create release branch: `release/vX.Y.Z`
3. Final testing and validation
4. Tag release: `git tag vX.Y.Z`
5. Push tags: `git push --tags`
6. Create GitHub release with notes
7. Announce to team

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

To work on roadmap items:
1. Pick an issue from the current milestone
2. Use `/completeIssue` to follow the standardized workflow
3. Submit PR following branch naming conventions
4. Ensure all validation checks pass

---

**Last Updated:** December 19, 2025
