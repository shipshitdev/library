from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "audit-routines.py"
SPEC = importlib.util.spec_from_file_location("audit_routines", MODULE_PATH)
assert SPEC and SPEC.loader
audit_routines = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = audit_routines
SPEC.loader.exec_module(audit_routines)


class RoutineAuditTests(unittest.TestCase):
    def test_reports_leakage_without_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            claude_dir = root / "claude"
            codex_dir = root / "codex"
            task_dir = claude_dir / "task-a"
            automation_dir = codex_dir / "automation-a"
            task_dir.mkdir(parents=True)
            automation_dir.mkdir(parents=True)
            (task_dir / "SKILL.md").write_text(
                "---\nname: task-a\ndescription: Audit fixture.\n---\n"
                "Use the sonnet model.\n"
                "Set effort: high.\n"
            )
            (automation_dir / "automation.toml").write_text(
                'model = "do-not-print-model"\n'
                'reasoning_effort = "do-not-print-effort"\n'
                'cwds = ["/do/not/print/path"]\n'
                'prompt = "Create a worktree, then report findings."\n'
            )

            result = audit_routines.audit(claude_dir, codex_dir, 0.92)
            sources = audit_routines.discover_claude_sources(claude_dir)
            codex_sources, _ = audit_routines.discover_codex_sources(codex_dir)
            labels = audit_routines.source_labels(sources + codex_sources, False)
            output = audit_routines.render_text(result, labels)

            self.assertIn("model directive", output)
            self.assertIn("effort directive", output)
            self.assertIn("workspace directive", output)
            self.assertNotIn("do-not-print", output)
            self.assertNotIn("/do/not/print/path", output)

    def test_groups_parameterized_duplicate_bodies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            claude_dir = root / "claude"
            for name, repository in (("task-a", "org/alpha"), ("task-b", "org/beta")):
                task_dir = claude_dir / name
                task_dir.mkdir(parents=True)
                (task_dir / "SKILL.md").write_text(
                    "---\n"
                    f"name: {name}\n"
                    "description: Audit fixture.\n"
                    "---\n"
                    "Review dependency health and return a prioritized report with "
                    "source evidence. Do not update files or send messages.\n"
                    f"Repository: {repository}\n"
                )

            result = audit_routines.audit(claude_dir, root / "codex", 0.92)

            self.assertEqual(len(result.duplicate_groups), 1)
            self.assertEqual(len(result.duplicate_groups[0]), 2)


if __name__ == "__main__":
    unittest.main()
