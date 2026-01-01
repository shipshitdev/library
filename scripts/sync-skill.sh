#!/bin/bash
#
# Sync Skill Between Platforms
#
# Syncs a skill from one platform (Claude/Codex) to another while preserving
# platform-specific sections marked with HTML comments.
#
# Usage:
#   ./scripts/sync-skill.sh <skill-name> <source-platform> <target-platform> [--dry-run]
#
# Examples:
#   ./scripts/sync-skill.sh accessibility claude codex
#   ./scripts/sync-skill.sh skill-creator codex claude --dry-run
#
# Options:
#   --dry-run    Preview changes without applying them
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
DRY_RUN=false
SKILL_NAME=""
SOURCE_PLATFORM=""
TARGET_PLATFORM=""

# Parse command line arguments
if [[ $# -lt 3 ]]; then
    echo -e "${RED}Error: Missing required arguments${NC}"
    echo "Usage: $0 <skill-name> <source-platform> <target-platform> [--dry-run]"
    echo "Platforms: claude, codex"
    exit 1
fi

SKILL_NAME="$1"
SOURCE_PLATFORM="$2"
TARGET_PLATFORM="$3"

if [[ "$SOURCE_PLATFORM" != "claude" && "$SOURCE_PLATFORM" != "codex" ]]; then
    echo -e "${RED}Error: Invalid source platform: $SOURCE_PLATFORM${NC}"
    echo "Valid platforms: claude, codex"
    exit 1
fi

if [[ "$TARGET_PLATFORM" != "claude" && "$TARGET_PLATFORM" != "codex" ]]; then
    echo -e "${RED}Error: Invalid target platform: $TARGET_PLATFORM${NC}"
    echo "Valid platforms: claude, codex"
    exit 1
fi

if [[ "$SOURCE_PLATFORM" == "$TARGET_PLATFORM" ]]; then
    echo -e "${RED}Error: Source and target platforms must be different${NC}"
    exit 1
fi

# Check for --dry-run flag
if [[ $# -gt 3 && "$4" == "--dry-run" ]]; then
    DRY_RUN=true
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SOURCE_DIR="$REPO_ROOT/agents/.$SOURCE_PLATFORM/skills/$SKILL_NAME"
TARGET_DIR="$REPO_ROOT/agents/.$TARGET_PLATFORM/skills/$SKILL_NAME"

# Validate source directory exists
if [[ ! -d "$SOURCE_DIR" ]]; then
    echo -e "${RED}Error: Source skill directory does not exist: $SOURCE_DIR${NC}"
    exit 1
fi

# Check if target directory exists
if [[ ! -d "$TARGET_DIR" ]]; then
    echo -e "${YELLOW}Warning: Target skill directory does not exist: $TARGET_DIR${NC}"
    if [[ "$DRY_RUN" == "false" ]]; then
        read -p "Create target directory? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            mkdir -p "$TARGET_DIR"
            echo -e "${GREEN}Created target directory: $TARGET_DIR${NC}"
        else
            echo "Aborted."
            exit 1
        fi
    else
        echo -e "${YELLOW}[DRY RUN] Would create target directory: $TARGET_DIR${NC}"
    fi
fi

echo -e "${BLUE}Syncing skill: $SKILL_NAME${NC}"
echo "  Source: $SOURCE_PLATFORM ($SOURCE_DIR)"
echo "  Target: $TARGET_PLATFORM ($TARGET_DIR)"
if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "  Mode: ${YELLOW}DRY RUN (no changes will be made)${NC}"
fi
echo

# Function to sync a file
sync_file() {
    local source_file="$1"
    local target_file="$2"
    local rel_path="${source_file#$SOURCE_DIR/}"
    
    # Skip if source file doesn't exist
    if [[ ! -f "$source_file" ]]; then
        return 0
    fi
    
    # Create target directory if needed
    local target_dir="$(dirname "$target_file")"
    if [[ "$DRY_RUN" == "false" ]]; then
        mkdir -p "$target_dir"
    fi
    
    # Read source file
    local content=$(cat "$source_file")
    
    # Remove target platform-specific sections
    local target_platform_upper=$(echo "$TARGET_PLATFORM" | tr '[:lower:]' '[:upper:]')
    content=$(echo "$content" | sed "/<!-- PLATFORM-SPECIFIC-START: $TARGET_PLATFORM -->/,/<!-- PLATFORM-SPECIFIC-END: $TARGET_PLATFORM -->/d")
    
    # Replace platform references
    if [[ "$TARGET_PLATFORM" == "codex" ]]; then
        # Replace Claude references with Codex
        content=$(echo "$content" | sed "s/Claude's capabilities/Codex's capabilities/g")
        content=$(echo "$content" | sed "s/Claude will use/Codex reads/g")
        content=$(echo "$content" | sed "s/Claude determines/Codex determines/g")
        content=$(echo "$content" | sed "s/Claude reads/Codex reads/g")
        content=$(echo "$content" | sed "s/for Claude to use/for Codex to use/g")
        content=$(echo "$content" | sed "s/Claude needs/Codex needs/g")
        content=$(echo "$content" | sed "s/~\/\.claude\/skills/~\/.codex\/skills/g")
    else
        # Replace Codex references with Claude
        content=$(echo "$content" | sed "s/Codex's capabilities/Claude's capabilities/g")
        content=$(echo "$content" | sed "s/Codex reads/Claude will use/g")
        content=$(echo "$content" | sed "s/Codex determines/Claude will use/g")
        content=$(echo "$content" | sed "s/for Codex to use/for Claude to use/g")
        content=$(echo "$content" | sed "s/Codex needs/Claude needs/g")
        content=$(echo "$content" | sed "s/~\/\.codex\/skills/~\/.claude\/skills/g")
    fi
    
    # Handle frontmatter differences
    if [[ "$rel_path" == "SKILL.md" ]]; then
        # Remove source platform-specific frontmatter fields
        if [[ "$SOURCE_PLATFORM" == "codex" ]]; then
            # Remove metadata.short-description from source
            content=$(echo "$content" | sed '/^metadata:/,/^---$/d' | sed '/^  short-description:/d')
        else
            # Remove license field from source
            content=$(echo "$content" | sed '/^license: /d')
        fi
        
        # Add target platform-specific frontmatter fields if needed
        # Note: This is a simple approach - may need refinement for complex frontmatter
        if [[ "$TARGET_PLATFORM" == "codex" ]]; then
            # Check if metadata section exists, if not add it
            if ! echo "$content" | grep -q "metadata:"; then
                # Add after description line
                content=$(echo "$content" | sed "/^description: /a\\
metadata:\\
  short-description: $(echo "$SKILL_NAME" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')
")
            fi
        else
            # Add license field if not present
            if ! echo "$content" | grep -q "license:"; then
                # Check if LICENSE.txt exists
                if [[ -f "$TARGET_DIR/LICENSE.txt" ]]; then
                    content=$(echo "$content" | sed "/^description: /a\\
license: Complete terms in LICENSE.txt
")
                fi
            fi
        fi
    fi
    
    # Write to target file
    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}[DRY RUN] Would sync:${NC} $rel_path"
        echo "  Source: $source_file"
        echo "  Target: $target_file"
    else
        echo "$content" > "$target_file"
        echo -e "${GREEN}Synced:${NC} $rel_path"
    fi
}

# Function to sync a directory recursively
sync_directory() {
    local source_dir="$1"
    local target_dir="$2"
    
    # Create target directory
    if [[ "$DRY_RUN" == "false" ]]; then
        mkdir -p "$target_dir"
    fi
    
    # Sync all files
    find "$source_dir" -type f | while read -r source_file; do
        local rel_path="${source_file#$source_dir/}"
        local target_file="$target_dir/$rel_path"
        sync_file "$source_file" "$target_file"
    done
}

# Sync SKILL.md first (most important)
if [[ -f "$SOURCE_DIR/SKILL.md" ]]; then
    sync_file "$SOURCE_DIR/SKILL.md" "$TARGET_DIR/SKILL.md"
fi

# Sync other files and directories
for item in "$SOURCE_DIR"/*; do
    if [[ "$item" == "$SOURCE_DIR/SKILL.md" ]]; then
        continue  # Already synced
    fi
    
    if [[ -f "$item" ]]; then
        filename=$(basename "$item")
        sync_file "$item" "$TARGET_DIR/$filename"
    elif [[ -d "$item" ]]; then
        dirname=$(basename "$item")
        sync_directory "$item" "$TARGET_DIR/$dirname"
    fi
done

echo
if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${BLUE}Dry run complete.${NC}"
    echo "Run without --dry-run to apply changes."
else
    echo -e "${GREEN}Sync complete!${NC}"
    echo
    echo "Next steps:"
    echo "1. Review the synced skill for any manual adjustments needed"
    echo "2. Run validation: ./scripts/validate-skill-sync.sh $SKILL_NAME"
    echo "3. Test the skill on both platforms"
fi

