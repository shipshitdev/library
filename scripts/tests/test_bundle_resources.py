from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class BundleResourceTests(unittest.TestCase):
    def test_ci_fixture_discovery_never_executes_dependency_tests(self) -> None:
        workflow = (ROOT / ".github/workflows/ci.yml").read_text()
        command = next(line.strip() for line in workflow.splitlines() if line.strip().startswith("find skills "))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            owned = root / "skills/example/owned.test.mjs"
            dependency = root / "skills/pstack/scripts/node_modules/provider/unowned.test.mjs"
            owned.parent.mkdir(parents=True)
            dependency.parent.mkdir(parents=True)
            owned.write_text("import test from 'node:test'; test('owned fixture', () => {});\n")
            dependency.write_text("throw new Error('dependency tests must not execute');\n")
            result = subprocess.run(["bash", "-c", command], cwd=root, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("owned fixture", result.stdout)
            self.assertNotIn("unowned.test", result.stdout + result.stderr)

    def test_runtime_dependencies_stay_out_of_bundles_but_sources_and_lock_ship(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scripts = root / "scripts"
            scripts.mkdir()
            shutil.copy2(ROOT / "scripts/generate-marketplace-bundles.js", scripts)
            (root / "package.json").write_text(json.dumps({"version": "1.0.0", "type": "module"}))
            (scripts / "plugin-categories.json").write_text(json.dumps({
                "bundles": {"fixture": {"description": "Fixture bundle", "skills": ["pstack"]}},
            }))
            source = root / "skills/pstack"
            resources = [
                "SKILL.md", "scripts/bun.lock", "scripts/runner/cli.ts",
                "adapters/hooks/session-start", "LICENSE",
            ]
            ignored = [
                "scripts/node_modules/dependency/index.ts",
                "scripts/__pycache__/helper.pyc", ".git/config", ".DS_Store",
            ]
            for name in resources + ignored:
                path = source / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture\n")
            subprocess.run(["node", str(scripts / "generate-marketplace-bundles.js")],
                           check=True, capture_output=True)
            destination = root / "bundles/fixture/skills/pstack"
            for name in resources:
                self.assertEqual((destination / name).read_bytes(), (source / name).read_bytes())
            for name in ignored:
                self.assertFalse((destination / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
