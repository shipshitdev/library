#!/bin/bash
# Setup symlinks for genfeedai projects to use centralized commands

SKILLS_REPO="/Users/decod3rs/www/agenticindiedev/skills"
GENFEEDAI_ROOT="/Users/decod3rs/www/genfeedai"
PROJECTS=("api.genfeed.ai" "genfeed.ai" "extension.genfeed.ai" "mobile.genfeed.ai" "docs.genfeed.ai" "packages.genfeed.ai")

echo "🔗 Setting up symlinks for genfeedai projects to use centralized commands"
echo ""

# Backup existing symlinks/commands
backup_symlink() {
  local target="$1"
  if [ -L "$target" ]; then
    local link_target=$(readlink "$target")
    echo "  ℹ️  Existing symlink: $target -> $link_target"
    rm "$target"
    echo "  ✅ Removed old symlink"
  elif [ -d "$target" ]; then
    mv "$target" "${target}.backup.$(date +%Y%m%d_%H%M%S)"
    echo "  ✅ Backed up existing directory"
  fi
}

# Setup symlink for a project
setup_project_symlink() {
  local project="$1"
  local project_path="$GENFEEDAI_ROOT/$project"
  local cursor_dir="$project_path/.cursor"
  
  if [ ! -d "$project_path" ]; then
    echo "  ⚠️  Project not found: $project_path (skipping)"
    return
  fi
  
  echo "📁 Processing: $project"
  
  # Create .cursor directory if it doesn't exist
  mkdir -p "$cursor_dir"
  
  # Backup and create commands symlink
  if [ -e "$cursor_dir/commands" ]; then
    backup_symlink "$cursor_dir/commands"
  fi
  
  ln -sf "$SKILLS_REPO/.cursor/commands" "$cursor_dir/commands"
  echo "  ✅ Created symlink: $cursor_dir/commands -> $SKILLS_REPO/.cursor/commands"
  
  # Keep settings.json if it exists (don't overwrite)
  if [ -f "$cursor_dir/settings.json" ]; then
    echo "  ℹ️  Keeping existing settings.json"
  fi
  
  echo ""
}

# Process each project
for project in "${PROJECTS[@]}"; do
  setup_project_symlink "$project"
done

echo "✅ Symlink setup complete!"
echo ""
echo "Summary:"
echo "- Genfeedai projects now use centralized commands from: $SKILLS_REPO/.cursor/commands"
echo "- Genfeed-specific commands remain in: $GENFEEDAI_ROOT/.cursor/commands"
echo "- Project-specific settings.json files preserved"
echo ""
echo "To verify:"
echo "  ls -la $GENFEEDAI_ROOT/[project]/.cursor/commands"
