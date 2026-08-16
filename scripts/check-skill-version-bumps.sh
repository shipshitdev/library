#!/bin/bash
#
# Require a metadata.version bump for every skill whose content changed.
#
# Compares HEAD against BASE_REF (default: origin/master). For each
# skills/<name>/ with a changed file other than plugin.json, the SKILL.md
# metadata.version at HEAD must differ from the version at BASE_REF.
#
#   - New skills (no SKILL.md at base) pass.
#   - Deleted skills (no SKILL.md at HEAD) pass.
#   - plugin.json-only edits pass: that file is metadata sync, not content,
#     and validate-skill-sync.sh already forces it to mirror SKILL.md.
#
# Usage:
#   bash scripts/check-skill-version-bumps.sh            # BASE_REF=origin/master
#   BASE_REF=origin/main bash scripts/check-skill-version-bumps.sh
#

set -euo pipefail

BASE_REF="${BASE_REF:-origin/master}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if ! git rev-parse --verify --quiet "$BASE_REF" >/dev/null; then
  echo -e "${RED}✗ BASE_REF '$BASE_REF' is not a known ref (need fetch-depth: 0 in CI).${NC}"
  exit 2
fi

MERGE_BASE=$(git merge-base "$BASE_REF" HEAD)

# Skill directories with any change other than plugin.json.
CHANGED_SKILLS=$(git diff --name-only "$MERGE_BASE" HEAD -- skills/ \
  | grep -E '^skills/[^/]+/' \
  | grep -vE '^skills/[^/]+/plugin\.json$' \
  | sed -E 's|^skills/([^/]+)/.*|\1|' \
  | sort -u || true)

if [[ -z "$CHANGED_SKILLS" ]]; then
  echo -e "${GREEN}✓ No skill content changed vs $BASE_REF — nothing to bump.${NC}"
  exit 0
fi

# Extract metadata.version from a SKILL.md blob at a given rev ("" if absent).
skill_version_at() {
  local rev="$1" name="$2"
  git show "$rev:skills/$name/SKILL.md" 2>/dev/null | awk '
    NR == 1 && $0 != "---" { exit }
    NR > 1 && $0 == "---" { exit }
    /^metadata:$/ { in_metadata = 1; next }
    in_metadata && /^[A-Za-z0-9_-]+:/ { in_metadata = 0 }
    in_metadata && /^  version:/ {
      sub(/^  version:[[:space:]]*/, "")
      gsub(/["'"'"']/, "")
      print
      exit
    }
  ' || true
}

failures=0
for name in $CHANGED_SKILLS; do
  base_version=$(skill_version_at "$MERGE_BASE" "$name")
  head_version=$(skill_version_at HEAD "$name")

  if [[ -z "$base_version" ]]; then
    echo -e "${GREEN}✓${NC} $name — new skill (${head_version:-no version}), no bump required"
    continue
  fi
  if [[ -z "$head_version" ]]; then
    echo -e "${GREEN}✓${NC} $name — removed at HEAD, no bump required"
    continue
  fi
  if [[ "$base_version" == "$head_version" ]]; then
    echo -e "${RED}✗${NC} $name — content changed but metadata.version is still $head_version (bump it in SKILL.md and mirror plugin.json)"
    ((++failures))
  else
    echo -e "${GREEN}✓${NC} $name — $base_version → $head_version"
  fi
done

echo
if [[ $failures -gt 0 ]]; then
  echo -e "${RED}✗ $failures skill(s) changed without a version bump.${NC}"
  echo -e "${YELLOW}  Bump metadata.version in skills/<name>/SKILL.md, then set the same version in skills/<name>/plugin.json.${NC}"
  exit 1
fi
echo -e "${GREEN}✓ Every changed skill carries a version bump.${NC}"
