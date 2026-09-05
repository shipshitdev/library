from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class BundleResourceTests(unittest.TestCase):
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
