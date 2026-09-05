from __future__ import annotations

import re
import sys
from collections.abc import Iterator
from pathlib import Path


ROUTE = re.compile(
    r"\b(?:Run|Apply|Invoke|Use|run|apply|invoke|use)\s+(?:the\s+)?"
    r"`([a-z][a-z0-9-]*)`(?P<skill>\s+skill\b)?"
)
ADVISORY = re.compile(
    r"(?:\b(?:do not|does not|must not|should not|never)\s+(?:automatically\s+)?$|"
    r"\b(?:recommend|named|example)\b)", re.IGNORECASE
)
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def instruction_lines(text: str) -> Iterator[tuple[int, str]]:
    frontmatter = text.startswith("---\n")
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        if frontmatter:
            if number > 1 and line == "---":
                frontmatter = False
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


def findings(skill_dir: Path, skills_root: Path) -> list[str]:
    result = []
    for path in sorted(skill_dir.rglob("*.md")):
        advisory_section = False
        for number, line in instruction_lines(path.read_text()):
            if line.startswith("## "):
                advisory_section = line[3:].lower() in {"when not to use", "related", "related skills", "examples"}
            location = f"{path.relative_to(skills_root)}:{number}"
            for route in ROUTE.finditer(line):
                if advisory_section or ADVISORY.search(line[:route.start()]):
                    continue
                target = skills_root / route.group(1) / "SKILL.md"
                if not target.is_file():
                    if route.group("skill"):
                        result.append(f"{location}: Missing execution skill: {route.group(1)}")
                    continue
                if target.parent == skill_dir:
                    continue
                frontmatter = target.read_text().split("---", 2)[1]
                if re.search(r"^disable-model-invocation:\s*true\s*$", frontmatter, re.M):
                    result.append(
                        f"{location}: Execution route targets user-only skill: {route.group(1)}"
                    )
            for link in LINK.finditer(line):
                reference = link.group(1).split("#", 1)[0]
                if (not reference or ":" in reference or "<" in reference
                        or "{" in reference or reference == "URL" or reference.startswith("/")):
                    continue
                if not (path.parent / reference).exists():
                    result.append(f"{location}: Missing local resource: {reference}")
    return result


def main() -> int:
    skills_root = Path(sys.argv[1]).resolve()
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
