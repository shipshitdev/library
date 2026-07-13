#!/usr/bin/env python3
"""Audit local routine prompts without emitting prompt or configuration values."""

from __future__ import annotations

import argparse
import json
import re
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


APP_OWNED_CODEX_FIELDS = {
    "cwds",
    "execution_environment",
    "model",
    "reasoning_effort",
    "rrule",
    "schedule",
    "target",
}

LEAKAGE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "model",
        re.compile(
            r"\b(?:model\s*[:=]|use\s+(?:the\s+)?(?:[a-z0-9.-]+\s+)?model\b|"
            r"claude-[a-z0-9.-]+|gpt-[a-z0-9.-]+|gemini-[a-z0-9.-]+|"
            r"\b(?:sonnet|opus|haiku)\b)",
            re.IGNORECASE,
        ),
    ),
    (
        "effort",
        re.compile(
            r"\b(?:reasoning[_ -]?effort|(?:low|medium|high|xhigh|max)\s+effort)\b|"
            r"\beffort\s*[:=]",
            re.IGNORECASE,
        ),
    ),
    (
        "schedule",
        re.compile(
            r"\b(?:rrule|cron|run\s+every\s+|every\s+(?:day|week|month|hour))\b|"
            r"\bschedule\s*[:=]",
            re.IGNORECASE,
        ),
    ),
    (
        "workspace",
        re.compile(
            r"\b(?:(?:create|use|switch\s+to)\s+(?:a\s+)?worktree|"
            r"source\s+checkout)\b|\b(?:cwd|working\s+directory|workspace)\s*[:=]",
            re.IGNORECASE,
        ),
    ),
    (
        "environment",
        re.compile(
            r"\bexecution_environment\b|\benvironment\s*[:=]|"
            r"\bexport\s+[A-Z][A-Z0-9_]*=",
            re.IGNORECASE,
        ),
    ),
)


@dataclass(frozen=True)
class RoutineSource:
    identifier: str
    platform: str
    path: Path
    body: str
    frontmatter: str = ""


@dataclass(frozen=True)
class Finding:
    source: str
    platform: str
    category: str
    location: str


@dataclass(frozen=True)
class AuditResult:
    claude_sources: int
    codex_sources: int
    findings: list[Finding]
    duplicate_groups: list[list[str]]
    codex_app_fields: list[str]


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    parts = text.split("---", 2)
    if len(parts) != 3:
        return "", text
    return parts[1], parts[2]


def discover_claude_sources(root: Path) -> list[RoutineSource]:
    sources: list[RoutineSource] = []
    for index, path in enumerate(sorted(root.glob("*/SKILL.md")), 1):
        frontmatter, body = split_frontmatter(path.read_text(errors="replace"))
        sources.append(
            RoutineSource(
                identifier=f"claude-task-{index:03d}",
                platform="claude",
                path=path,
                body=body,
                frontmatter=frontmatter,
            )
        )
    return sources


def discover_codex_sources(root: Path) -> tuple[list[RoutineSource], set[str]]:
    sources: list[RoutineSource] = []
    observed_fields: set[str] = set()
    for index, path in enumerate(sorted(root.glob("*/automation.toml")), 1):
        try:
            data = tomllib.loads(path.read_text(errors="replace"))
        except (OSError, tomllib.TOMLDecodeError):
            continue
        observed_fields.update(APP_OWNED_CODEX_FIELDS.intersection(data))
        prompt = data.get("prompt", "")
        sources.append(
            RoutineSource(
                identifier=f"codex-automation-{index:03d}",
                platform="codex",
                path=path,
                body=prompt if isinstance(prompt, str) else "",
            )
        )
    return sources, observed_fields


def scan_leakage(source: RoutineSource) -> list[Finding]:
    findings: list[Finding] = []
    sections = (("frontmatter", source.frontmatter), ("body", source.body))
    for section, text in sections:
        for line_number, line in enumerate(text.splitlines(), 1):
            for category, pattern in LEAKAGE_PATTERNS:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            source=source.identifier,
                            platform=source.platform,
                            category=category,
                            location=f"{section} line {line_number}",
                        )
                    )
                    break
    return findings


def normalize_body(text: str) -> str:
    normalized = text.lower()
    normalized = re.sub(r"https?://\S+", "<url>", normalized)
    normalized = re.sub(r"(?<!\w)/(?:[^\s/]+/)+[^\s]+", "<path>", normalized)
    normalized = re.sub(r"\b[a-z0-9_.-]+/[a-z0-9_.-]+\b", "<repository>", normalized)
    normalized = re.sub(r"\b[0-9a-f]{8}-[0-9a-f-]{27,}\b", "<identifier>", normalized)
    normalized = re.sub(r"\$\{?[A-Z][A-Z0-9_]*\}?", "<parameter>", normalized)
    normalized = re.sub(r"`[^`\n]+`", "<parameter>", normalized)
    normalized = re.sub(
        r"(?im)^\s*(?:project|repository|repo|workspace)\s*[:=].*$",
        "<project-parameter>",
        normalized,
    )
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def duplicate_groups(
    sources: list[RoutineSource], similarity: float
) -> list[list[str]]:
    normalized = [normalize_body(source.body) for source in sources]
    signatures: list[frozenset[tuple[str, ...]]] = []
    for body in normalized:
        tokens = body.split()
        signatures.append(
            frozenset(tuple(tokens[index : index + 5]) for index in range(len(tokens) - 4))
        )
    parents = list(range(len(sources)))

    def find(index: int) -> int:
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parents[right_root] = left_root

    for left in range(len(sources)):
        if len(normalized[left]) < 80:
            continue
        for right in range(left + 1, len(sources)):
            if len(normalized[right]) < 80:
                continue
            union_size = len(signatures[left] | signatures[right])
            ratio = (
                len(signatures[left] & signatures[right]) / union_size
                if union_size
                else 0.0
            )
            if ratio >= similarity:
                union(left, right)

    grouped: dict[int, list[str]] = {}
    for index, source in enumerate(sources):
        grouped.setdefault(find(index), []).append(source.identifier)
    return sorted(
        (members for members in grouped.values() if len(members) > 1),
        key=lambda members: (-len(members), members),
    )


def audit(claude_dir: Path, codex_dir: Path, similarity: float) -> AuditResult:
    claude_sources = discover_claude_sources(claude_dir)
    codex_sources, observed_fields = discover_codex_sources(codex_dir)
    sources = claude_sources + codex_sources
    findings = [finding for source in sources for finding in scan_leakage(source)]
    return AuditResult(
        claude_sources=len(claude_sources),
        codex_sources=len(codex_sources),
        findings=findings,
        duplicate_groups=duplicate_groups(sources, similarity),
        codex_app_fields=sorted(observed_fields),
    )


def source_labels(sources: Iterable[RoutineSource], show_paths: bool) -> dict[str, str]:
    return {
        source.identifier: str(source.path) if show_paths else source.identifier
        for source in sources
    }


def render_text(
    result: AuditResult,
    labels: dict[str, str],
) -> str:
    lines = [
        "Routine audit (read-only)",
        f"Sources: Claude {result.claude_sources}, Codex {result.codex_sources}",
        f"App-parameter leakage findings: {len(result.findings)}",
    ]
    for finding in result.findings:
        lines.append(
            f"- {labels[finding.source]}: {finding.category} directive "
            f"({finding.location})"
        )
    lines.append(f"Duplicate routine families: {len(result.duplicate_groups)}")
    for index, group in enumerate(result.duplicate_groups, 1):
        members = ", ".join(labels[source] for source in group)
        lines.append(f"- family-{index:03d}: {members}")
    fields = ", ".join(result.codex_app_fields) or "none"
    lines.append(f"Codex app-owned fields observed (names only): {fields}")
    lines.append("Prompt bodies and configuration values were not emitted.")
    return "\n".join(lines)


def render_json(result: AuditResult, labels: dict[str, str]) -> str:
    payload = asdict(result)
    for finding in payload["findings"]:
        finding["source"] = labels[finding["source"]]
    payload["duplicate_groups"] = [
        [labels[source] for source in group] for group in result.duplicate_groups
    ]
    payload["value_redaction"] = "Prompt bodies and configuration values omitted."
    return json.dumps(payload, indent=2, sort_keys=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit Claude scheduled-task and Codex automation prompt bodies."
    )
    parser.add_argument(
        "--claude-dir",
        type=Path,
        default=Path("~/.claude/scheduled-tasks").expanduser(),
    )
    parser.add_argument(
        "--codex-dir",
        type=Path,
        default=Path("~/.codex/automations").expanduser(),
    )
    parser.add_argument("--similarity", type=float, default=0.92)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--show-paths", action="store_true")
    parser.add_argument("--fail-on-findings", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 0.0 <= args.similarity <= 1.0:
        raise SystemExit("--similarity must be between 0 and 1")

    result = audit(args.claude_dir, args.codex_dir, args.similarity)
    claude_sources = discover_claude_sources(args.claude_dir)
    codex_sources, _ = discover_codex_sources(args.codex_dir)
    labels = source_labels(claude_sources + codex_sources, args.show_paths)
    output = (
        render_json(result, labels)
        if args.format == "json"
        else render_text(result, labels)
    )
    print(output)
    has_findings = bool(result.findings or result.duplicate_groups)
    return 1 if args.fail_on_findings and has_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
