from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "skill_composition", ROOT / "scripts/check-skill-composition.py"
)
assert SPEC and SPEC.loader
composition = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(composition)


class SkillCompositionTests(unittest.TestCase):
    def setUp(self) -> None:
        scratch = ROOT / ".tmp"
        scratch.mkdir(exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.directory.cleanup)
        self.skills = Path(self.directory.name)

    def add_skill(self, name: str, body: str = "", explicit: bool = False) -> Path:
        directory = self.skills / name
        directory.mkdir()
        restriction = "disable-model-invocation: true\n" if explicit else ""
        (directory / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Fixture.\n{restriction}---\n{body}\n"
        )
        return directory

    def test_direct_route_rejects_hidden_engine(self) -> None:
        caller = self.add_skill("caller", "1. Run the `engine` skill.")
        self.add_skill("engine", explicit=True)
        self.assertEqual(len(composition.findings(caller, self.skills)), 1)
        self.assertIn("user-only skill: engine", composition.findings(caller, self.skills)[0])

    def test_negative_condition_still_executes_its_route(self) -> None:
        caller = self.add_skill("caller", "If not configured, run the `engine` skill.")
        self.add_skill("engine", explicit=True)
        self.assertIn("user-only skill: engine", composition.findings(caller, self.skills)[0])

    def test_callable_engine_can_be_composed(self) -> None:
        caller = self.add_skill("caller", "- **run →** apply the `engine` skill.", explicit=True)
        self.add_skill("engine", "Apply only within the authorized task.")
        self.assertEqual(composition.findings(caller, self.skills), [])

    def test_recommendations_and_prohibitions_do_not_execute(self) -> None:
        caller = self.add_skill("caller", "Recommend: run the `engine` skill.\nDo not invoke `engine`.\nForce mode does not run `engine`.")
        self.add_skill("engine", explicit=True)
        self.assertEqual(composition.findings(caller, self.skills), [])

    def test_related_workflow_is_advice_not_composition(self) -> None:
        caller = self.add_skill("caller", "## When NOT to Use\nUse the `engine` skill for other work.")
        self.add_skill("engine", explicit=True)
        self.assertEqual(composition.findings(caller, self.skills), [])

    def test_code_examples_are_not_routes(self) -> None:
        caller = self.add_skill("caller", "```markdown\nRun the `engine` skill.\n```\n~~~md\nApply `engine`.\n~~~")
        self.add_skill("engine", explicit=True)
        self.assertEqual(composition.findings(caller, self.skills), [])

    def test_shorter_fence_does_not_end_a_code_example(self) -> None:
        caller = self.add_skill("caller", "````markdown\n```\nRun the `engine` skill.\n```\n````")
        self.add_skill("engine", explicit=True)
        self.assertEqual(composition.findings(caller, self.skills), [])

    def test_actual_missing_skill_differs_from_cli_command(self) -> None:
        caller = self.add_skill("caller", "Run the `missing-engine` skill.\nRun `git-status`.")
        findings = composition.findings(caller, self.skills)
        self.assertEqual(len(findings), 1)
        self.assertIn("Missing execution skill: missing-engine", findings[0])

    def test_local_resources_resolve_from_the_installed_skill(self) -> None:
        caller = self.add_skill("caller", "Read [guide](references/guide.md).")
        findings = composition.findings(caller, self.skills)
        self.assertIn("Missing local resource", findings[0])
        (caller / "references").mkdir()
        (caller / "references/guide.md").write_text("Instructions.\n")
        self.assertEqual(composition.findings(caller, self.skills), [])

    def test_remote_links_and_template_placeholders_are_not_local_files(self) -> None:
        caller = self.add_skill("caller", "[docs](https://example.com/docs) [section](#usage)\n[reference](URL) [reference]({Reference URL}) [site](/docs/concepts/resources)")
        self.assertEqual(composition.findings(caller, self.skills), [])

    def test_public_pstack_routes_are_discoverable(self) -> None:
        self.assertEqual(composition.findings(ROOT / "skills/pstack", ROOT / "skills"), [])

    def test_system_bash_parses_the_repository_validator(self) -> None:
        result = subprocess.run(
            ["/bin/bash", "-n", str(ROOT / "scripts/validate-skill-sync.sh")],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_review_workflow_leaves_model_selection_with_harness(self) -> None:
        script = r'''
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";
const source = readFileSync("skills/full-code-review/scripts/full-code-review.js", "utf8")
  .replace("export const meta", "const meta");
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
const execute = new AsyncFunction("agent", "parallel", "log", "DIFF", "CHANGED_FILES", "COMMIT_LOG", source);
for (const retro of [false, true]) {
  const labels = [];
  const agent = async (_prompt, options) => {
    assert.equal(Object.hasOwn(options, "model"), false);
    assert.equal(Object.hasOwn(options, "effort"), false);
    labels.push(options.label);
    if (options.label === "adversarial-verifier") return { verified_findings: [] };
    if (options.label.endsWith("synthesis")) return { mode: retro ? "retro" : "pr", verdict: retro ? "retro-backlog" : "approve", rationale: "Fixture", stats: {} };
    return { findings: [] };
  };
  const result = await execute(agent, (tasks) => Promise.all(tasks.map((task) => task())), () => {}, "diff", "file.ts", retro ? "commit" : "");
  assert.equal(labels.length, retro ? 6 : 5);
  assert.equal(result.mode, retro ? "retro" : "pr");
}
'''
        result = subprocess.run(["bun", "-e", script], cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
