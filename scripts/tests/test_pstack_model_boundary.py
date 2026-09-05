from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEXT = (ROOT / "scripts/validate-skill-sync.sh").read_text()
START = TEXT.index("filter_pstack_protocol_fixtures() {")
END = TEXT.index("\ncheck_public_concrete_models()", START)
CHECK = TEXT[START:END]


class PstackModelBoundaryTests(unittest.TestCase):
    def check(self, relative: str, content: str) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "pstack"
            target = skill / relative
            target.parent.mkdir(parents=True)
            target.write_text(content)
            return subprocess.run(
                ["bash", "-c", CHECK + '\ncheck_model_references "$1"', "fixture", str(skill)],
                text=True, capture_output=True, check=False,
            )

    def test_protocol_parser_samples_are_allowed(self) -> None:
        result = self.check("scripts/runner/model-aliases.ts", 'return model === "opus";\n')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_runtime_model_defaults_outside_protocol_files_are_rejected(self) -> None:
        result = self.check("scripts/runner/commands.ts", 'const defaultModel = "gpt-4.1";\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Concrete model name", result.stdout)

    def test_prompt_named_like_a_fixture_is_still_checked(self) -> None:
        result = self.check("references/model-aliases.ts", 'Use the opus model.\n')
        self.assertNotEqual(result.returncode, 0)

    def test_installed_dependencies_do_not_become_routing_policy(self) -> None:
        result = self.check("scripts/node_modules/provider/README.md", 'Use gpt-4.1.\n')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
