#!/bin/bash
#
# Validate Skill Sync
#
# Validates that skills are properly synced between platforms, checking for:
# - Platform reference consistency
# - Platform-specific metadata
# - Drift between platforms
# - Missing platform-specific adaptations
#
# Usage:
#   ./scripts/validate-skill-sync.sh [skill-name]
#
# Examples:
#   ./scripts/validate-skill-sync.sh                    # Validate all skills
#   ./scripts/validate-skill-sync.sh accessibility      # Validate specific skill
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

CLAUDE_DIR="$REPO_ROOT/agents/.claude/skills"
CODEX_DIR="$REPO_ROOT/agents/.codex/skills"

SKILL_NAME="${1:-}"

# Statistics
TOTAL_ISSUES=0
TOTAL_SKILLS=0
SKILLS_WITH_ISSUES=0

# Function to check platform references
check_platform_references() {
    local file="$1"
    local platform="$2"
    local issues=0
    
    if [[ ! -f "$file" ]]; then
        return 0
    fi
    
    local content=$(cat "$file")
    
    if [[ "$platform" == "claude" ]]; then
        # Check for Codex references in Claude skill
        if echo "$content" | grep -qi "Codex's capabilities"; then
            echo -e "  ${RED}✗${NC} Contains 'Codex's capabilities' (should be 'Claude's capabilities')"
            ((issues++))
        fi
        if echo "$content" | grep -qi "Codex reads"; then
            echo -e "  ${RED}✗${NC} Contains 'Codex reads' (should be 'Claude will use')"
            ((issues++))
        fi
        if echo "$content" | grep -qi "~/.codex/skills"; then
            echo -e "  ${RED}✗${NC} Contains '~/.codex/skills' (should be '~/.claude/skills')"
            ((issues++))
        fi
    else
        # Check for Claude references in Codex skill
        if echo "$content" | grep -qi "Claude's capabilities"; then
            echo -e "  ${RED}✗${NC} Contains 'Claude's capabilities' (should be 'Codex's capabilities')"
            ((issues++))
        fi
        if echo "$content" | grep -qi "Claude will use"; then
            echo -e "  ${RED}✗${NC} Contains 'Claude will use' (should be 'Codex reads')"
            ((issues++))
        fi
        if echo "$content" | grep -qi "~/.claude/skills"; then
            echo -e "  ${RED}✗${NC} Contains '~/.claude/skills' (should be '~/.codex/skills')"
            ((issues++))
        fi
    fi
    
    return $issues
}

# Function to check frontmatter
check_frontmatter() {
    local file="$1"
    local platform="$2"
    local issues=0

    if [[ ! -f "$file" ]]; then
        return 0
    fi

    local content=$(cat "$file")

    # Extract frontmatter (between first two --- lines)
    if ! echo "$content" | grep -q "^---$"; then
        return 0
    fi

    # Extract only the frontmatter section for checks (macOS compatible)
    local frontmatter=$(echo "$content" | awk '/^---$/{if(++c==1)next; if(c==2)exit} c==1{print}')

    if [[ "$platform" == "codex" ]]; then
        # Codex should have metadata.short-description (optional but recommended)
        # Codex should NOT have license field
        if echo "$frontmatter" | grep -q "^license:"; then
            echo -e "  ${YELLOW}⚠${NC} Contains 'license' field (Codex doesn't use this)"
            ((issues++))
        fi
    else
        # Claude can have license field (optional)
        # Claude should NOT have metadata.short-description in frontmatter
        if echo "$frontmatter" | grep -q "^metadata:"; then
            echo -e "  ${YELLOW}⚠${NC} Contains 'metadata' section (Claude doesn't use this)"
            ((issues++))
        fi
    fi
    
    # Check for required fields
    if ! echo "$content" | grep -q "^name:"; then
        echo -e "  ${RED}✗${NC} Missing required 'name' field"
        ((issues++))
    fi
    
    if ! echo "$content" | grep -q "^description:"; then
        echo -e "  ${RED}✗${NC} Missing required 'description' field"
        ((issues++))
    fi
    
    return $issues
}

# Function to check for drift
check_drift() {
    local skill_name="$1"
    local claude_file="$CLAUDE_DIR/$skill_name/SKILL.md"
    local codex_file="$CODEX_DIR/$skill_name/SKILL.md"
    
    if [[ ! -f "$claude_file" ]] || [[ ! -f "$codex_file" ]]; then
        return 0
    fi
    
    # Remove platform-specific sections for comparison
    local claude_content=$(cat "$claude_file" | sed "/<!-- PLATFORM-SPECIFIC-START: codex -->/,/<!-- PLATFORM-SPECIFIC-END: codex -->/d" | sed "s/Claude/PLATFORM/g" | sed "s/claude/PLATFORM/g")
    local codex_content=$(cat "$codex_file" | sed "/<!-- PLATFORM-SPECIFIC-START: claude -->/,/<!-- PLATFORM-SPECIFIC-END: claude -->/d" | sed "s/Codex/PLATFORM/g" | sed "s/codex/PLATFORM/g")
    
    # Remove frontmatter differences
    claude_content=$(echo "$claude_content" | sed "/^license:/d" | sed "/^metadata:/,/^---$/d")
    codex_content=$(echo "$codex_content" | sed "/^license:/d" | sed "/^metadata:/,/^---$/d")
    
    # Compare (simple line count check - could be enhanced)
    local claude_lines=$(echo "$claude_content" | wc -l)
    local codex_lines=$(echo "$codex_content" | wc -l)
    local diff=$((claude_lines - codex_lines))
    
    if [[ ${diff#-} -gt 50 ]]; then
        echo -e "  ${YELLOW}⚠${NC} Significant content drift detected (${diff#-} line difference)"
        echo -e "     Claude: $claude_lines lines, Codex: $codex_lines lines"
        echo -e "     Consider syncing to ensure core content is identical"
    fi
    
    # Always return 0 - drift is informational only, not an error
    return 0
}

# Function to validate a single skill
validate_skill() {
    local skill_name="$1"
    local skill_issues=0
    
    echo -e "${BLUE}Validating: $skill_name${NC}"
    
    # Check Claude version
    local claude_file="$CLAUDE_DIR/$skill_name/SKILL.md"
    if [[ -f "$claude_file" ]]; then
        echo "  Claude version:"
        check_platform_references "$claude_file" "claude" || skill_issues=$?
        check_frontmatter "$claude_file" "claude" || skill_issues=$?
    else
        echo -e "  ${YELLOW}⚠${NC} Claude version missing"
        ((skill_issues++))
    fi
    
    # Check Codex version
    local codex_file="$CODEX_DIR/$skill_name/SKILL.md"
    if [[ -f "$codex_file" ]]; then
        echo "  Codex version:"
        check_platform_references "$codex_file" "codex" || skill_issues=$?
        check_frontmatter "$codex_file" "codex" || skill_issues=$?
    else
        echo -e "  ${YELLOW}⚠${NC} Codex version missing"
        ((skill_issues++))
    fi
    
    # Check for drift
    if [[ -f "$claude_file" ]] && [[ -f "$codex_file" ]]; then
        echo "  Drift check:"
        check_drift "$skill_name" || skill_issues=$?
    fi
    
    if [[ $skill_issues -eq 0 ]]; then
        echo -e "  ${GREEN}✓${NC} No issues found"
    else
        ((SKILLS_WITH_ISSUES++))
        ((TOTAL_ISSUES += skill_issues))
    fi
    
    echo
    return $skill_issues
}

# Main validation logic
if [[ -n "$SKILL_NAME" ]]; then
    # Validate specific skill
    if [[ ! -d "$CLAUDE_DIR/$SKILL_NAME" ]] && [[ ! -d "$CODEX_DIR/$SKILL_NAME" ]]; then
        echo -e "${RED}Error: Skill '$SKILL_NAME' not found in either platform${NC}"
        exit 1
    fi
    ((TOTAL_SKILLS++))
    validate_skill "$SKILL_NAME"
else
    # Validate all skills
    echo -e "${BLUE}Validating all skills...${NC}"
    echo
    
    # Get all skill names from both platforms, excluding .system (Codex-specific system directory)
    all_skills=$(find "$CLAUDE_DIR" "$CODEX_DIR" -maxdepth 1 -type d -not -path "$CLAUDE_DIR" -not -path "$CODEX_DIR" -not -name ".system" | xargs -n1 basename | sort -u)
    
    while IFS= read -r skill_name; do
        if [[ -n "$skill_name" ]] && [[ "$skill_name" != ".system" ]]; then
            ((TOTAL_SKILLS++))
            validate_skill "$skill_name"
        fi
    done <<< "$all_skills"
fi

# Summary
echo -e "${BLUE}=== Validation Summary ===${NC}"
echo "Total skills checked: $TOTAL_SKILLS"
echo "Skills with issues: $SKILLS_WITH_ISSUES"
echo "Total issues found: $TOTAL_ISSUES"
echo

if [[ $TOTAL_ISSUES -eq 0 ]]; then
    echo -e "${GREEN}✓ All skills validated successfully!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠ Some issues were found. Review the output above.${NC}"
    echo
    echo "To fix issues:"
    echo "1. Review the specific issues for each skill"
    echo "2. Use sync tool: ./scripts/sync-skill.sh <skill-name> <source> <target>"
    echo "3. Manually fix platform-specific issues"
    exit 1
fi

