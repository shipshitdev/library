#!/bin/bash
#
# Validate Skills
#
# Validates skills have required files and frontmatter.
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

SKILLS_DIR="$REPO_ROOT/skills"

SKILL_NAME="${1:-}"

# Statistics
TOTAL_ISSUES=0
TOTAL_SKILLS=0
SKILLS_WITH_ISSUES=0

# Function to check frontmatter
check_frontmatter() {
    local file="$1"
    local issues=0

    if [[ ! -f "$file" ]]; then
        return 0
    fi

    local content=$(cat "$file")

    # Check for frontmatter
    if ! echo "$content" | grep -q "^---$"; then
        echo -e "  ${RED}✗${NC} Missing frontmatter (---)"
        return 1
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

# Function to validate a single skill
validate_skill() {
    local skill_name="$1"
    local skill_issues=0

    echo -e "${BLUE}Validating: $skill_name${NC}"

    local skill_file="$SKILLS_DIR/$skill_name/SKILL.md"
    if [[ -f "$skill_file" ]]; then
        check_frontmatter "$skill_file" || skill_issues=$?
    else
        echo -e "  ${RED}✗${NC} SKILL.md missing"
        ((skill_issues++))
    fi

    if [[ $skill_issues -eq 0 ]]; then
        echo -e "  ${GREEN}✓${NC} Valid"
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
    if [[ ! -d "$SKILLS_DIR/$SKILL_NAME" ]]; then
        echo -e "${RED}Error: Skill '$SKILL_NAME' not found${NC}"
        exit 1
    fi
    ((TOTAL_SKILLS++))
    validate_skill "$SKILL_NAME"
else
    # Validate all skills
    echo -e "${BLUE}Validating all skills...${NC}"
    echo

    for skill_dir in "$SKILLS_DIR"/*/; do
        if [[ -d "$skill_dir" ]]; then
            skill_name=$(basename "$skill_dir")
            ((TOTAL_SKILLS++))
            validate_skill "$skill_name"
        fi
    done
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
    exit 1
fi
