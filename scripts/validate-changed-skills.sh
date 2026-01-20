#!/bin/bash
#
# Validate changed skills in pre-commit hook
# Only validates skills that have been modified
#

set -euo pipefail

# Get list of changed SKILL.md files in the main skills/ directory only
# Skip bundles/ as those are generated/derived from skills/
CHANGED_SKILLS=$(git diff --cached --name-only --diff-filter=ACMR | grep -E '^skills/[^/]+/SKILL\.md$' || true)

if [[ -z "$CHANGED_SKILLS" ]]; then
  # No skill files changed, skip validation
  exit 0
fi

# Extract unique skill names (from paths like skills/foo/SKILL.md -> foo)
SKILL_NAMES=$(echo "$CHANGED_SKILLS" | sed -E 's|^skills/([^/]+)/SKILL\.md$|\1|' | sort -u)

echo "🔍 Validating changed skills..."
echo

# Run validation for each changed skill
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

for skill_name in $SKILL_NAMES; do
  echo "Validating: $skill_name"
  if ! bash "$REPO_ROOT/scripts/validate-skill-sync.sh" "$skill_name"; then
    echo "❌ Validation failed for skill: $skill_name"
    exit 1
  fi
  echo
done

echo "✅ All changed skills validated successfully"

