#!/bin/bash

# validate-output.sh - Validates project output structure and content
# Checks for required files, proper formatting, and common issues

set -euo pipefail

# Colors
if [ -t 1 ] && command -v tput &> /dev/null; then
    NUM_COLORS=$(tput colors 2>/dev/null || echo 0)
    if [ "$NUM_COLORS" -ge 8 ]; then
        GREEN=$(tput setaf 2)
        YELLOW=$(tput setaf 3)
        RED=$(tput setaf 1)
        BLUE=$(tput setaf 4)
        NC=$(tput sgr0)
    else
        GREEN=''
        YELLOW=''
        RED=''
        BLUE=''
        NC=''
    fi
else
    GREEN=''
    YELLOW=''
    RED=''
    BLUE=''
    NC=''
fi

echo -e "${BLUE}🔍 Validating project output...${NC}"
echo ""

errors=0
warnings=0

# Check file existence
check_file() {
    local file=$1
    local level=${2:-error}  # error or warning

    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
        return 0
    else
        if [ "$level" = "error" ]; then
            echo -e "${RED}✗${NC} $file MISSING"
            ((errors++))
        else
            echo -e "${YELLOW}⚠${NC} $file missing (optional)"
            ((warnings++))
        fi
        return 1
    fi
}

# Check directory existence
check_dir() {
    local dir=$1

    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} Directory exists: $dir"
        return 0
    else
        echo -e "${RED}✗${NC} Directory missing: $dir"
        ((errors++))
        return 1
    fi
}

echo -e "${BLUE}Required Files:${NC}"
check_file "PROJECT.md"
check_file "aiDocs/SUMMARY.md"
check_file "aiDocs/TASKS.md"
check_file "aiDocs/DISCOVERY.md"
check_file "aiDocs/AI.md"
check_file "docs/CONTACTS.md"
check_file "docs/TASKS.md"
check_file "docs/DECISIONS.md"
check_file "docs/QUESTIONS.md"

echo ""
echo -e "${BLUE}Directory Structure:${NC}"
check_dir "core/templates"
check_dir "email/raw"
check_dir "email/ai"
check_dir "email/processed"
check_dir "aiDocs"
check_dir "prompts"
check_dir "docs"

echo ""
echo -e "${BLUE}Content Quality:${NC}"

# Check for placeholders
if grep -rq '\[CUSTOMER\]\|\[PROJECT\]\|\[DATE\]' aiDocs/ PROJECT.md 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC} Placeholder text found ([CUSTOMER], [PROJECT], [DATE])"
    ((warnings++))
else
    echo -e "${GREEN}✓${NC} No placeholder text found"
fi

# Check PROJECT.md has AI tagline
if [ -f "PROJECT.md" ] && grep -q "This document was originally created by an AI agent" PROJECT.md; then
    echo -e "${GREEN}✓${NC} PROJECT.md contains AI model tagline"
else
    echo -e "${YELLOW}⚠${NC} PROJECT.md missing AI model tagline"
    ((warnings++))
fi

# Check task ID format in TASKS.md
if [ -f "aiDocs/TASKS.md" ]; then
    if grep -q 'TASK-[0-9]\{3\}' aiDocs/TASKS.md; then
        echo -e "${GREEN}✓${NC} TASKS.md contains properly formatted task IDs"
    else
        echo -e "${YELLOW}⚠${NC} TASKS.md may not have proper task IDs (TASK-001 format)"
        ((warnings++))
    fi
fi

# Check Quick Context in SUMMARY.md
if [ -f "aiDocs/SUMMARY.md" ]; then
    if grep -q "## Quick Context" aiDocs/SUMMARY.md; then
        echo -e "${GREEN}✓${NC} SUMMARY.md has Quick Context section"
    else
        echo -e "${YELLOW}⚠${NC} SUMMARY.md missing Quick Context section"
        ((warnings++))
    fi
fi

# Check Last Updated dates
if [ -f "aiDocs/SUMMARY.md" ] && grep -q "Last Updated:" aiDocs/SUMMARY.md; then
    echo -e "${GREEN}✓${NC} aiDocs files have 'Last Updated' dates"
else
    echo -e "${YELLOW}⚠${NC} Missing 'Last Updated' dates in aiDocs/"
    ((warnings++))
fi

echo ""
echo -e "${BLUE}Email Processing:${NC}"

# Check email directories
email_ai_count=$(find email/ai -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
email_processed_count=$(find email/processed -name "*.eml" 2>/dev/null | wc -l | tr -d ' ')
email_raw_count=$(find email/raw -name "*.eml" 2>/dev/null | wc -l | tr -d ' ')

if [ "$email_ai_count" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} email/ai/ contains $email_ai_count converted email(s)"
fi

if [ "$email_processed_count" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} email/processed/ contains $email_processed_count archived email(s)"
fi

if [ "$email_raw_count" -gt 0 ]; then
    echo -e "${YELLOW}⚠${NC} email/raw/ still contains $email_raw_count unprocessed email(s)"
    ((warnings++))
elif [ "$email_ai_count" -eq 0 ] && [ "$email_processed_count" -eq 0 ]; then
    echo -e "${BLUE}ℹ${NC} No emails processed (optional)"
else
    echo -e "${GREEN}✓${NC} email/raw/ is empty (all emails processed)"
fi

# Summary
echo ""
echo "═══════════════════════════════════════"
if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo -e "${GREEN}✅ All validation checks passed!${NC}"
    echo "Project output is complete and properly structured."
    echo ""
    echo "Next steps:"
    echo "  1. Review PROJECT.md for project overview"
    echo "  2. Check docs/ folder for quick reference"
    echo "  3. Review aiDocs/TASKS.md for outstanding work"
    exit 0
elif [ $errors -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Validation completed with $warnings warning(s)${NC}"
    echo "Project output is functional but some optional items are missing."
    echo ""
    echo "You can proceed, but consider addressing warnings for better documentation quality."
    exit 0
else
    echo -e "${RED}❌ Validation failed: $errors error(s), $warnings warning(s)${NC}"
    echo ""
    echo "Please resolve errors before proceeding:"
    echo "  - Run /quickStartProject to generate missing files"
    echo "  - Check that email files are in correct format"
    echo "  - Verify Python 3.x is installed"
    echo "  - Run ./go.sh and select 'Health Check' for system validation"
    exit 1
fi
