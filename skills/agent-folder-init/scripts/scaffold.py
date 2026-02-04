#!/usr/bin/env python3
"""
Scaffold a comprehensive .agents/ folder structure for AI-first development.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path


SKILL_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"
ROOT_FILES_DIR = SKILL_DIR / "assets" / "root-files"
AGENT_CONFIGS_DIR = SKILL_DIR / "assets" / "agent-configs"
# Library root: two levels up from skill directory (e.g., ~/.claude/ or agents/.claude/)
LIBRARY_ROOT = SKILL_DIR.parent.parent


def scaffold_agent_folder(
    root: Path,
    project_name: str,
    tech_stack: str = "",
    allow_outside: bool = False,
) -> None:
    """Copy template files and customize for the project."""

    agent_dir = root / ".agent"

    if agent_dir.exists():
        print(f"Warning: {agent_dir} already exists. Merging with existing structure.")

    # Check if outside current directory
    cwd = Path.cwd()
    if not allow_outside and not root.is_relative_to(cwd):
        print(f"Error: Target path {root} is outside current directory.")
        print("Use --allow-outside to confirm this is intentional.")
        sys.exit(1)

    # Create the directory structure
    agent_dir.mkdir(parents=True, exist_ok=True)

    # Copy all template files
    if TEMPLATES_DIR.exists():
        for item in TEMPLATES_DIR.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(TEMPLATES_DIR)
                dest_path = agent_dir / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Read template content
                content = item.read_text()

                # Replace placeholders
                content = content.replace("{{PROJECT_NAME}}", project_name)
                content = content.replace("{{DATE}}", datetime.now().strftime("%Y-%m-%d"))
                content = content.replace("{{YEAR}}", str(datetime.now().year))
                content = content.replace("{{TECH_STACK}}", tech_stack or "Not specified")

                # Write customized content
                dest_path.write_text(content)
                print(f"Created: {dest_path}")
    else:
        print(f"Error: Templates directory not found at {TEMPLATES_DIR}")
        print("Creating minimal structure...")
        create_minimal_structure(agent_dir, project_name, tech_stack)

    # Create AI entry files at project root
    create_entry_files(root, project_name)

    # Copy root-level config files
    copy_root_files(root)

    # Copy agent config folders (.claude, .codex, .cursor)
    copy_agent_configs(root)

    print(f"\n✅ Agent folder created at: {agent_dir}")
    print("\nNext steps:")
    print("1. Customize SYSTEM/RULES.md with your coding standards")
    print("2. Update SYSTEM/ARCHITECTURE.md with your architecture")
    print("3. Add project-specific rules to SYSTEM/critical/CRITICAL-NEVER-DO.md")


def create_minimal_structure(agent_dir: Path, project_name: str, tech_stack: str) -> None:
    """Create minimal structure if templates are missing."""

    dirs = [
        "SYSTEM/ai",
        "SYSTEM/architecture",
        "SYSTEM/critical",
        "SYSTEM/quality",
        "TASKS",
        "SESSIONS",
        "SOP",
        "EXAMPLES",
        "FEEDBACK",
    ]

    for d in dirs:
        (agent_dir / d).mkdir(parents=True, exist_ok=True)

    # Create README.md
    readme = f"""# {project_name} - Agent Documentation

**Welcome to the {project_name} workspace!**

This is the `.agents/` folder containing AI agent documentation, session tracking, and project rules.

## Quick Start

Read `SYSTEM/ai/SESSION-QUICK-START.md` first.

## Structure

- `SYSTEM/` - Architecture, rules, and AI protocols
- `TASKS/` - Task tracking and inbox
- `SESSIONS/` - Daily session documentation
- `SOP/` - Standard operating procedures
- `EXAMPLES/` - Code patterns and examples
- `FEEDBACK/` - Improvement tracking

## Tech Stack

{tech_stack or 'Not specified'}

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
"""
    (agent_dir / "README.md").write_text(readme)


def create_entry_files(root: Path, project_name: str) -> None:
    """Create AGENTS.md, CLAUDE.md, CODEX.md at project root."""

    agents_content = f"""# {project_name}

This file provides entry points for AI agents.

## Documentation

All documentation is in `.agents/`:
- `.agents/README.md` - Navigation hub
- `.agents/SYSTEM/RULES.md` - Coding standards
- `.agents/TASKS/` - Task tracking
- `.agents/SESSIONS/` - Session history

## Quick Start

Read `.agents/SYSTEM/ai/SESSION-QUICK-START.md` before starting work.
"""

    claude_content = f"""# {project_name}

Claude-specific entry point. Documentation in `.agents/`.

## Commands

Check `.agents/SYSTEM/RULES.md` for coding standards.

## Sessions

Document all work in `.agents/SESSIONS/YYYY-MM-DD.md` (one file per day).
"""

    codex_content = f"""# {project_name}

Codex-specific entry point. Documentation in `.agents/`.

## Documentation

- `.agents/README.md` - Start here
- `.agents/SYSTEM/` - Architecture and rules
- `.agents/TASKS/` - Current tasks
"""

    (root / "AGENTS.md").write_text(agents_content)
    (root / "CLAUDE.md").write_text(claude_content)
    (root / "CODEX.md").write_text(codex_content)

    print(f"Created: {root}/AGENTS.md")
    print(f"Created: {root}/CLAUDE.md")
    print(f"Created: {root}/CODEX.md")


def copy_root_files(root: Path) -> None:
    """Copy root-level config files like .editorconfig to project root."""

    if not ROOT_FILES_DIR.exists():
        return

    for item in ROOT_FILES_DIR.rglob("*"):
        if item.is_file():
            rel_path = item.relative_to(ROOT_FILES_DIR)
            dest_path = root / rel_path

            # Don't overwrite existing files
            if dest_path.exists():
                print(f"Skipped (exists): {dest_path}")
                continue

            dest_path.parent.mkdir(parents=True, exist_ok=True)
            content = item.read_text()
            dest_path.write_text(content)
            print(f"Created: {dest_path}")


def copy_agent_configs(root: Path) -> None:
    """Copy agent config folders (.claude, .codex, .cursor) to project root.
    
    Copies from library root (e.g., ~/.claude/agents/, ~/.claude/commands/, ~/.claude/rules/)
    instead of template assets to eliminate duplication and ensure projects get the latest version.
    Falls back to template assets if library root is not available.
    """

    # Map source dirs to destination dirs
    config_mappings = [
        ("claude", ".claude"),
        ("codex", ".codex"),
        ("cursor", ".cursor"),
    ]

    for src_name, dest_name in config_mappings:
        # Try library root first (e.g., ~/.claude/agents/, ~/.claude/commands/, ~/.claude/rules/)
        library_src = LIBRARY_ROOT / src_name
        # Fallback to template assets if library root doesn't exist
        template_src = AGENT_CONFIGS_DIR / src_name if AGENT_CONFIGS_DIR.exists() else None
        
        dest_dir = root / dest_name

        # Determine which source to use
        source_dir = None
        if library_src.exists():
            source_dir = library_src
            source_type = "library"
        elif template_src and template_src.exists():
            source_dir = template_src
            source_type = "template"
        else:
            continue

        # Create destination directory
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Copy files recursively
        # Only copy agents/ and commands/ subdirectories
        # NOTE: rules/ are NOT copied - they're inherited from ~/.claude/rules/ (library level)
        # This prevents duplication since library-level rules apply to all projects
        subdirs_to_copy = ["agents", "commands"]
        copied_anything = False

        for subdir in subdirs_to_copy:
            src_subdir = source_dir / subdir
            if not src_subdir.exists():
                continue

            for item in src_subdir.rglob("*"):
                if item.is_file():
                    rel_path = item.relative_to(src_subdir)
                    dest_path = dest_dir / subdir / rel_path

                    # Don't overwrite existing files
                    if dest_path.exists():
                        continue

                    dest_path.parent.mkdir(parents=True, exist_ok=True)

                    try:
                        content = item.read_text()
                        dest_path.write_text(content)
                        copied_anything = True
                    except UnicodeDecodeError:
                        # Binary file, copy directly
                        shutil.copy2(item, dest_path)
                        copied_anything = True

        if copied_anything:
            print(f"Created: {dest_dir}/ (with commands, rules, agents) from {source_type}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a .agents/ folder structure for AI-first development."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Target directory (default: current directory)",
    )
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="Project name",
    )
    parser.add_argument(
        "--tech",
        type=str,
        default="",
        help="Tech stack (e.g., 'nextjs,nestjs,react-native')",
    )
    parser.add_argument(
        "--allow-outside",
        action="store_true",
        help="Allow creating files outside current directory",
    )

    args = parser.parse_args()

    scaffold_agent_folder(
        root=args.root.resolve(),
        project_name=args.name,
        tech_stack=args.tech,
        allow_outside=args.allow_outside,
    )


if __name__ == "__main__":
    main()
