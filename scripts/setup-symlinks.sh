#!/bin/bash
# Setup symlinks for Ship Shit Dev Library
# Dynamically links ~/.claude, ~/.codex, ~/.cursor to this library's agents folder
#
# Usage: ./scripts/setup-symlinks.sh [--dry-run] [--force]
#   --dry-run  Show what would be done without making changes
#   --force    Remove existing files/directories (not just symlinks)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
DRY_RUN=false
FORCE=false
for arg in "$@"; do
    case $arg in
        --dry-run) DRY_RUN=true ;;
        --force) FORCE=true ;;
        -h|--help)
            echo "Usage: $0 [--dry-run] [--force]"
            echo "  --dry-run  Show what would be done without making changes"
            echo "  --force    Remove existing files/directories (not just symlinks)"
            exit 0
            ;;
    esac
done

# Get the absolute path to the library directory
# Works whether script is called from anywhere
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIBRARY_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
AGENTS_DIR="$LIBRARY_DIR/agents"

echo -e "${BLUE}Ship Shit Dev Library - Symlink Setup${NC}"
echo "========================================"
echo ""
echo "Library location: $LIBRARY_DIR"
echo ""

if $DRY_RUN; then
    echo -e "${YELLOW}DRY RUN MODE - No changes will be made${NC}"
    echo ""
fi

# Verify agents directory exists
if [[ ! -d "$AGENTS_DIR" ]]; then
    echo -e "${RED}Error: agents directory not found at $AGENTS_DIR${NC}"
    exit 1
fi

# Function to create a symlink
create_symlink() {
    local source="$1"
    local target="$2"
    local name="$3"

    # Check if source exists
    if [[ ! -d "$source" ]]; then
        echo -e "${YELLOW}  Skip $name: source doesn't exist ($source)${NC}"
        return
    fi

    # Create parent directory if needed
    local parent_dir="$(dirname "$target")"
    if [[ ! -d "$parent_dir" ]]; then
        if $DRY_RUN; then
            echo -e "${BLUE}  Would create directory: $parent_dir${NC}"
        else
            mkdir -p "$parent_dir"
            echo -e "${GREEN}  Created directory: $parent_dir${NC}"
        fi
    fi

    # Handle existing target
    if [[ -L "$target" ]]; then
        # It's a symlink - check if it points to the right place
        local current_target="$(readlink "$target")"
        if [[ "$current_target" == "$source" ]]; then
            echo -e "${GREEN}  ✓ $name: already correctly linked${NC}"
            return
        else
            # Wrong target - remove it
            if $DRY_RUN; then
                echo -e "${YELLOW}  Would remove broken symlink: $target -> $current_target${NC}"
            else
                rm "$target"
                echo -e "${YELLOW}  Removed broken symlink: $target -> $current_target${NC}"
            fi
        fi
    elif [[ -e "$target" ]]; then
        # It's a file or directory
        if $FORCE; then
            if $DRY_RUN; then
                echo -e "${YELLOW}  Would remove existing: $target${NC}"
            else
                rm -rf "$target"
                echo -e "${YELLOW}  Removed existing: $target${NC}"
            fi
        else
            echo -e "${RED}  ✗ $name: target exists and is not a symlink ($target)${NC}"
            echo -e "${RED}    Use --force to remove it${NC}"
            return
        fi
    fi

    # Create the symlink
    if $DRY_RUN; then
        echo -e "${BLUE}  Would link: $target -> $source${NC}"
    else
        ln -s "$source" "$target"
        echo -e "${GREEN}  ✓ $name: linked $target -> $source${NC}"
    fi
}

# Define symlinks to create
echo "Setting up Claude Code symlinks..."
create_symlink "$AGENTS_DIR/.claude/skills" "$HOME/.claude/skills" "skills"
create_symlink "$AGENTS_DIR/.claude/commands" "$HOME/.claude/commands" "commands"
create_symlink "$AGENTS_DIR/.claude/agents" "$HOME/.claude/agents" "agents"
create_symlink "$AGENTS_DIR/.claude/rules" "$HOME/.claude/rules" "rules"

echo ""
echo "Setting up Codex symlinks..."
create_symlink "$AGENTS_DIR/.codex/skills" "$HOME/.codex/skills" "skills"

echo ""
echo "Setting up Cursor symlinks..."
create_symlink "$AGENTS_DIR/.cursor/skills" "$HOME/.cursor/skills" "skills"
create_symlink "$AGENTS_DIR/.cursor/commands" "$HOME/.cursor/commands" "commands"

echo ""
echo "========================================"
if $DRY_RUN; then
    echo -e "${YELLOW}Dry run complete. Run without --dry-run to apply changes.${NC}"
else
    echo -e "${GREEN}Symlink setup complete!${NC}"
fi
echo ""
echo "Verify with: npm run check-symlinks"
