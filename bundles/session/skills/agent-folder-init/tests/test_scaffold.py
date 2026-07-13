from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from scaffold import scaffold_agent_folder  # noqa: E402


FIXTURES_DIR = Path(__file__).parent / "fixtures"


class ScaffoldFixtureTests(unittest.TestCase):
    def fixture(self, name: str, temporary_root: Path) -> Path:
        destination = temporary_root / "repo"
        shutil.copytree(FIXTURES_DIR / name, destination)
        placeholder = destination / ".gitkeep"
        if placeholder.exists():
            placeholder.unlink()
        return destination

    def test_empty_repo_is_unchanged_in_default_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture("empty", Path(directory))
            scaffold_agent_folder(root, "Example", allow_outside=True)
            self.assertEqual(list(root.iterdir()), [])

    def test_empty_repo_writes_only_allowlisted_shared_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture("empty", Path(directory))
            scaffold_agent_folder(root, "Example", write=True, allow_outside=True)
            self.assertTrue((root / ".agents/README.md").is_file())
            self.assertTrue((root / "AGENTS.md").is_file())
            self.assertFalse((root / ".codex").exists())
            self.assertFalse((root / ".claude").exists())

    def test_existing_entry_file_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture("existing", Path(directory))
            before = (root / "AGENTS.md").read_text()
            scaffold_agent_folder(root, "Example", write=True, allow_outside=True)
            self.assertEqual((root / "AGENTS.md").read_text(), before)

    def test_force_entry_files_allows_explicit_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture("existing", Path(directory))
            scaffold_agent_folder(
                root,
                "Example",
                write=True,
                force_entry_files=True,
                allow_outside=True,
            )
            self.assertIn("# Example", (root / "AGENTS.md").read_text())

    def test_platforms_add_only_documented_entry_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture("empty", Path(directory))
            scaffold_agent_folder(
                root,
                "Example",
                platforms={"claude", "codex", "cursor"},
                write=True,
                allow_outside=True,
            )
            self.assertTrue((root / "CLAUDE.md").is_file())
            self.assertTrue((root / ".cursor/rules/agent-context.mdc").is_file())
            self.assertFalse((root / ".codex").exists())


if __name__ == "__main__":
    unittest.main()
