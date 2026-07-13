from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = REPO_ROOT / "scripts/fixtures/skill-validation"
VALIDATOR = REPO_ROOT / "scripts/validate-skill-sync.sh"


class SkillValidatorFixtureTests(unittest.TestCase):
    def run_fixture(self, name: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            skills_dir = Path(directory) / "skills"
            fixture_dir = skills_dir / name
            shutil.copytree(FIXTURES_DIR / name, fixture_dir)
            manifest = {
                "name": name,
                "version": "1.0.0",
                "description": f"Validation fixture for {name}.",
                "author": {"name": "Fixture"},
                "license": "MIT",
                "skills": ".",
            }
            (fixture_dir / "plugin.json").write_text(json.dumps(manifest))
            environment = os.environ.copy()
            environment["SKILLS_DIR_OVERRIDE"] = str(skills_dir)
            return subprocess.run(
                ["bash", str(VALIDATOR), name],
                cwd=REPO_ROOT,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

    def assert_finding(self, fixture: str, finding: str, returncode: int) -> None:
        result = self.run_fixture(fixture)
        self.assertEqual(result.returncode, returncode, result.stdout + result.stderr)
        self.assertIn(finding, result.stdout)

    def test_valid_portable_fixture_passes(self) -> None:
        result = self.run_fixture("valid-portable")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("✗", result.stdout)

    def test_allowed_tools_list_is_rejected(self) -> None:
        self.assert_finding("invalid-allowed-tools", "allowed-tools must be", 1)

    def test_nested_trigger_metadata_is_rejected(self) -> None:
        self.assert_finding("invalid-triggers", "metadata.triggers is a no-op", 1)

    def test_execution_parameter_is_reported(self) -> None:
        self.assert_finding(
            "invalid-execution-parameter",
            "Harness-owned execution parameter",
            0,
        )

    def test_missing_mutation_guard_is_reported(self) -> None:
        self.assert_finding(
            "invalid-side-effect",
            "side-effecting skill must set disable-model-invocation",
            0,
        )

    def test_platform_marker_is_rejected(self) -> None:
        self.assert_finding("invalid-platform-marker", "Inert platform marker", 1)

    def test_dangling_route_is_reported_outside_named_sections(self) -> None:
        self.assert_finding("invalid-route", "Missing local skill reference", 0)

    def test_concrete_model_is_rejected(self) -> None:
        self.assert_finding("invalid-model", "Concrete model name", 1)


if __name__ == "__main__":
    unittest.main()
