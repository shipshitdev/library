#!/usr/bin/env python3
"""Plan or scaffold portable agent context files for an existing repository."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"
ENTRY_FILES_DIR = SKILL_DIR / "assets" / "entry-files"
ROOT_FILES_DIR = SKILL_DIR / "assets" / "root-files"

TEMPLATE_ALLOWLIST = (
    Path("README.md"),
    Path("memory/README.md"),
    Path("sessions/README.md"),
    Path("sessions/TEMPLATE.md"),
)
ROOT_FILE_ALLOWLIST = (Path(".editorconfig"),)
ENTRY_TEMPLATES = {
    "shared": (ENTRY_FILES_DIR / "AGENTS.md", Path("AGENTS.md")),
    "claude": (ENTRY_FILES_DIR / "CLAUDE.md", Path("CLAUDE.md")),
    "cursor": (
        ENTRY_FILES_DIR / "cursor-agent-context.mdc",
        Path(".cursor/rules/agent-context.mdc"),
    ),
}
SUPPORTED_PLATFORMS = {"claude", "codex", "cursor"}


@dataclass
class ActionSummary:
    planned: int = 0
    written: int = 0
    skipped: int = 0
    unchanged: int = 0


def render_template(content: str, project_name: str, tech_stack: str) -> str:
    """Replace the small, documented placeholder set."""
    now = datetime.now()
    return (
        content.replace("{{PROJECT_NAME}}", project_name)
        .replace("{{DATE}}", now.strftime("%Y-%m-%d"))
        .replace("{{YEAR}}", str(now.year))
        .replace("{{TECH_STACK}}", tech_stack or "Not specified")
    )


def validate_canonical_assets(platforms: set[str]) -> None:
    """Fail before any write when a required canonical template is unavailable."""
    required = [TEMPLATES_DIR / path for path in TEMPLATE_ALLOWLIST]
    required.extend(ROOT_FILES_DIR / path for path in ROOT_FILE_ALLOWLIST)
    required.append(ENTRY_TEMPLATES["shared"][0])

    for platform in platforms:
        if platform in {"claude", "cursor"}:
            required.append(ENTRY_TEMPLATES[platform][0])

    missing = [path for path in required if not path.is_file()]
    if missing:
        rendered = "\n".join(f"- {path}" for path in missing)
        raise FileNotFoundError(
            "Canonical scaffold templates are unavailable; no files were written:\n"
            f"{rendered}"
        )


def target_is_allowed(root: Path, allow_outside: bool) -> bool:
    """Return whether the resolved target stays within cwd or was explicitly allowed."""
    if allow_outside:
        return True

    try:
        root.relative_to(Path.cwd().resolve())
    except ValueError:
        return False
    return True


def materialize_text(
    destination: Path,
    content: str,
    *,
    write: bool,
    overwrite: bool,
    summary: ActionSummary,
) -> None:
    """Plan or perform one non-symlink text-file write."""
    exists = destination.exists() or destination.is_symlink()

    if destination.is_symlink():
        print(f"Refused symlink target: {destination}")
        summary.skipped += 1
        return

    if exists and not destination.is_file():
        print(f"Refused non-file target: {destination}")
        summary.skipped += 1
        return

    if exists:
        if destination.read_text() == content:
            print(f"Unchanged: {destination}")
            summary.unchanged += 1
            return
        if not overwrite:
            print(f"Skipped existing file: {destination}")
            summary.skipped += 1
            return
        action = "overwrite"
    else:
        action = "create"

    summary.planned += 1
    if not write:
        print(f"Would {action}: {destination}")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content)
    summary.written += 1
    print(f"{action.capitalize()}d: {destination}")


def scaffold_agent_folder(
    root: Path,
    project_name: str,
    tech_stack: str = "",
    platforms: set[str] | None = None,
    *,
    write: bool = False,
    force_entry_files: bool = False,
    allow_outside: bool = False,
) -> ActionSummary:
    """Plan by default; write only the documented allowlist when explicitly enabled."""
    selected_platforms = set(platforms or set())
    unknown = selected_platforms - SUPPORTED_PLATFORMS
    if unknown:
        names = ", ".join(sorted(unknown))
        raise ValueError(f"Unsupported platform(s): {names}")

    root = root.resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Target repository does not exist: {root}")
    if not target_is_allowed(root, allow_outside):
        raise PermissionError(
            f"Target {root} is outside {Path.cwd().resolve()}; pass --allow-outside "
            "only after verifying the target."
        )

    validate_canonical_assets(selected_platforms)
    summary = ActionSummary()

    for relative_path in TEMPLATE_ALLOWLIST:
        source = TEMPLATES_DIR / relative_path
        content = render_template(source.read_text(), project_name, tech_stack)
        materialize_text(
            root / ".agents" / relative_path,
            content,
            write=write,
            overwrite=False,
            summary=summary,
        )

    for relative_path in ROOT_FILE_ALLOWLIST:
        source = ROOT_FILES_DIR / relative_path
        materialize_text(
            root / relative_path,
            source.read_text(),
            write=write,
            overwrite=False,
            summary=summary,
        )

    entry_keys = ["shared"]
    entry_keys.extend(
        platform for platform in ("claude", "cursor") if platform in selected_platforms
    )
    for entry_key in entry_keys:
        source, relative_path = ENTRY_TEMPLATES[entry_key]
        content = render_template(source.read_text(), project_name, tech_stack)
        materialize_text(
            root / relative_path,
            content,
            write=write,
            overwrite=force_entry_files,
            summary=summary,
        )

    # Codex project instructions use the shared AGENTS.md entry. No .codex/commands
    # or other unsupported project command directory is generated.
    mode = "WRITE" if write else "DRY RUN"
    print(
        f"\n{mode}: planned={summary.planned}, written={summary.written}, "
        f"skipped={summary.skipped}, unchanged={summary.unchanged}"
    )
    if not write:
        print("Review the plan, then rerun with --write to apply it.")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan or scaffold portable .agents context for an existing repository."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Existing target repository (default: current directory)",
    )
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--tech", default="", help="Optional project tech-stack summary")
    parser.add_argument(
        "--platform",
        action="append",
        choices=sorted(SUPPORTED_PLATFORMS),
        default=[],
        help=(
            "Add a supported platform entry surface; repeat as needed. "
            "Without this flag, only shared .agents files and AGENTS.md are planned."
        ),
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Apply the reviewed plan; default behavior is dry-run only",
    )
    parser.add_argument(
        "--force-entry-files",
        action="store_true",
        help=(
            "Allow AGENTS.md, CLAUDE.md, and the Cursor entry rule to be overwritten; "
            "other existing files are always preserved"
        ),
    )
    parser.add_argument(
        "--allow-outside",
        action="store_true",
        help="Allow a verified target outside the current directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        scaffold_agent_folder(
            root=args.root,
            project_name=args.name,
            tech_stack=args.tech,
            platforms=set(args.platform),
            write=args.write,
            force_entry_files=args.force_entry_files,
            allow_outside=args.allow_outside,
        )
    except (FileNotFoundError, NotADirectoryError, PermissionError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
