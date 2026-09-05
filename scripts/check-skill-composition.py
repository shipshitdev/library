from __future__ import annotations

import re
import json
import sys
from collections.abc import Iterator
from pathlib import Path


ROUTE = re.compile(
    r"\b(?:Run|Apply|Invoke|Use|run|apply|invoke|use)\s+(?:the\s+)?"
    r"`([a-z][a-z0-9-]*)`(?P<skill>\s+skill\b)?"
)
ADVISORY = re.compile(
    r"(?:\b(?:do not|does not|must not|should not|never)\s+(?:automatically\s+)?$|"
    r"^\s*(?:[-*]\s+|\d+[.)]\s+)?Recommend\s*:?\s*$)", re.IGNORECASE
)
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def frontmatter(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for index, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return "\n".join(lines[1:index])
    return None


def instruction_lines(text: str) -> Iterator[tuple[int, str]]:
    header = frontmatter(text)
    header_end = next(
        number for number, line in enumerate(text.splitlines()[1:], 2)
        if line.strip() == "---"
    ) if header is not None else 0
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        if number <= header_end:
            continue
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif fence[0] == token[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield number, line


def declared_delegates(lines: list[tuple[int, str]]) -> Iterator[tuple[int, str]]:
    in_delegates = False
    target = re.compile(r"`([a-z][a-z0-9-]*)`")
    connector = re.compile(r"\s*(?:,\s*(?:and\s+|or\s+)?|(?:and|or)\s+|/\s*)")
    for index, (number, line) in enumerate(lines):
        if line.strip() == "Delegates To:":
            in_delegates = True
            continue
        if line.startswith("#") or re.match(r"^[A-Z][A-Za-z /]+:$", line):
            in_delegates = False
        if not in_delegates or not line.startswith("- "):
            continue
        item = line[2:]
        for _, continuation in lines[index + 1:]:
            if not continuation.startswith("  "):
                break
            item += " " + continuation.strip()
        # Only the leading target list declares execution; Recommend/File pointer
        # entries and mode names in the explanation are not delegates.
        match = target.match(item)
        while match:
            yield number, match.group(1)
            separator = connector.match(item, match.end())
            match = target.match(item, separator.end()) if separator else None


def findings(skill_dir: Path, skills_root: Path) -> list[str]:
    result = []
    def check_target(name: str, location: str, required: bool) -> None:
        target = skills_root / name / "SKILL.md"
        if not target.is_file():
            if required:
                result.append(f"{location}: Missing execution skill: {name}")
            return
        if target.parent == skill_dir:
            return
        header = frontmatter(target.read_text())
        if header is None:
            result.append(f"{location}: Execution skill has missing or unclosed frontmatter: {name}")
        elif re.search(r"^disable-model-invocation:\s*true\s*$", header, re.M):
            result.append(f"{location}: Execution route targets user-only skill: {name}")

    if skill_dir.name.startswith("gh-"):
        result.append(f"{skill_dir.name}: Retired gh-* skill family; use the canonical workflow/provider name")
    for path in sorted(skill_dir.rglob("*.md")):
        lines = list(instruction_lines(path.read_text()))
        for number, name in declared_delegates(lines):
            check_target(name, f"{path.relative_to(skills_root)}:{number}", True)
        advisory_section = False
        for number, line in lines:
            if line.startswith("## "):
                advisory_section = line[3:].lower() in {"when not to use", "related", "related skills", "examples"}
            location = f"{path.relative_to(skills_root)}:{number}"
            for route in ROUTE.finditer(line):
                if advisory_section or ADVISORY.search(line[:route.start()]):
                    continue
                check_target(route.group(1), location, bool(route.group("skill")))
            for link in LINK.finditer(line):
                reference = link.group(1).split("#", 1)[0]
                if (not reference or ":" in reference or "<" in reference
                        or "{" in reference or reference == "URL" or reference.startswith("/")):
                    continue
                if not (path.parent / reference).exists():
                    result.append(f"{location}: Missing local resource: {reference}")
    return result


def catalog_findings(skills_root: Path) -> list[str]:
    root = skills_root.parent
    paths = sorted((root / "commands").glob("*.md"))
    paths += [root / "scripts/setup-dev-loop.sh", root / "scripts/plugin-categories.json"]
    result = []
    for path in paths:
        if not path.is_file():
            continue
        for number, line in enumerate(path.read_text().splitlines(), 1):
            line = re.sub(r"https?://[^\s)]+", "", line)
            for match in re.finditer(r"(?<![a-zA-Z0-9_-])gh-(?:address-comments|board-sync|fix-ci|inbox|pr-publish|project-board|review-suggestions)(?![a-z0-9-])", line):
                result.append(f"{path.relative_to(root)}:{number}: Retired skill reference: {match.group()}")
    # Inspect committed installation entry points as well as canonical callers.
    marketplace = root / ".claude-plugin/marketplace.json"
    if marketplace.is_file():
        for plugin in json.loads(marketplace.read_text()).get("plugins", []):
            name, source = plugin.get("name", ""), plugin.get("source")
            if name.startswith("gh-"):
                result.append(f"{marketplace.relative_to(root)}: Retired plugin identity: {name}")
            if not isinstance(source, str) or not (root / source).is_dir():
                result.append(f"{marketplace.relative_to(root)}: Missing local plugin source: {source}")
    for directory in sorted((root / "bundles").glob("*/skills/gh-*")):
        result.append(f"{directory.relative_to(root)}: Retired bundled skill identity")
    return result


def main() -> int:
    skills_root = Path(sys.argv[1]).resolve()
    if len(sys.argv) > 2 and sys.argv[2] == "--catalog":
        result = catalog_findings(skills_root)
        for finding in result:
            print(finding)
        return int(bool(result))
    selected = [skills_root / sys.argv[2]] if len(sys.argv) > 2 else sorted(skills_root.iterdir())
    result = []
    for skill_dir in selected:
        if (skill_dir / "SKILL.md").is_file():
            result.extend(findings(skill_dir, skills_root))
    for finding in result:
        print(finding)
    return int(bool(result))


if __name__ == "__main__":
    raise SystemExit(main())
