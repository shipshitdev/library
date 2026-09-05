from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))
from cleanup import Refused, Repository  # noqa: E402


class GitFixtureTests(unittest.TestCase):
    def setUp(self):
        scratch = SKILL_DIR.parents[1] / ".tmp"
        scratch.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.root = self.directory / "repo"
        self.remote = self.directory / "origin.git"
        self.command("git", "init", "--bare", str(self.remote))
        self.command("git", "init", "-b", "main", str(self.root))
        self.repo = Repository(self.root)
        self.git("config", "user.name", "Cleanup Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("remote", "add", "origin", str(self.remote))
        self.commit("base", "base\n")
        self.git("push", "-u", "origin", "main")
        self.prs = []
        original_run = self.repo.run

        def run(*args, **kwargs):
            if args[:2] == ("gh", "repo"):
                return subprocess.CompletedProcess(args, 0, json.dumps({
                    "nameWithOwner": "owner/repo", "defaultBranchRef": {"name": "main"}
                }), "")
            if args[:2] == ("gh", "api"):
                return subprocess.CompletedProcess(args, 0, json.dumps([self.prs]), "")
            return original_run(*args, **kwargs)

        self.run_mock = patch.object(self.repo, "run", side_effect=run)
        self.run_mock.start()
        self.addCleanup(self.run_mock.stop)

    def command(self, *args, **kwargs):
        return subprocess.run(args, text=True, capture_output=True, check=True, **kwargs).stdout.strip()

    def git(self, *args):
        return self.command("git", "-C", str(self.root), *args)

    def commit(self, message, content, filename="file.txt"):
        (self.root / filename).write_text(content)
        self.git("add", filename)
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def squash(self, *, head_repo="owner/repo"):
        self.git("switch", "-c", "feature")
        self.commit("same subject", "first\n")
        head = self.commit("same subject", "second\n")
        self.git("switch", "main")
        self.git("merge", "--squash", "feature")
        self.git("commit", "-m", "same subject")
        merge = self.git("rev-parse", "HEAD")
        self.git("push", "origin", "main")
        self.prs = [{"number": 1, "state": "closed", "merged_at": "2026-01-01",
                     "merge_commit_sha": merge,
                     "head": {"ref": "feature", "sha": head, "repo": {"full_name": head_repo}},
                     "base": {"repo": {"full_name": "owner/repo"}}}]
        return head, merge

    def action_names(self, plan):
        return [action["ref"] for action in plan["actions"]]

    def test_exact_squash_head_is_proven_and_deleted_with_cas(self):
        self.squash()
        plan = self.repo.plan("local-branches")
        self.assertEqual(self.action_names(plan), ["refs/heads/feature"])
        self.assertEqual(plan["actions"][0]["proof"]["kind"], "exact-pr-head-squash")
        self.assertEqual(self.repo.apply(plan, "local-branches")[0]["result"], "removed")
        self.assertNotIn("feature", self.git("branch", "--format=%(refname:short)").splitlines())

    def test_commits_added_after_merged_pr_are_preserved(self):
        self.squash()
        self.git("switch", "feature")
        self.commit("same subject", "unmerged\n")
        self.git("switch", "main")
        self.assertEqual(self.repo.plan("local-branches")["actions"], [])

    def test_fork_pr_metadata_cannot_prove_squash(self):
        self.squash(head_repo="fork/repo")
        self.assertEqual(self.repo.plan("local-branches")["actions"], [])

    def test_missing_head_repository_cannot_prove_squash(self):
        self.squash()
        self.prs[0]["head"]["repo"] = None
        self.assertEqual(self.repo.plan("local-branches")["actions"], [])

    def test_same_subject_different_patch_is_not_proof(self):
        self.git("switch", "-c", "feature")
        self.commit("same subject", "branch only\n")
        self.git("switch", "main")
        self.commit("same subject", "trunk only\n")
        self.git("push", "origin", "main")
        self.assertEqual(self.repo.plan("local-branches")["actions"], [])

    def test_mixed_ahead_commits_are_not_hidden_by_one_matching_patch(self):
        self.git("switch", "-c", "feature")
        first = self.commit("first", "first\n")
        self.commit("second", "second\n")
        self.git("switch", "main")
        self.git("cherry-pick", first)
        self.git("push", "origin", "main")
        self.assertEqual(self.repo.plan("local-branches")["actions"], [])

    def test_patch_proof_covers_every_rebased_commit(self):
        self.git("switch", "-c", "feature")
        first = self.commit("first", "first\n")
        second = self.commit("second", "second\n")
        self.git("switch", "main")
        self.commit("other", "other\n", "other.txt")
        self.git("cherry-pick", first, second)
        self.git("push", "origin", "main")
        plan = self.repo.plan("local-branches")
        self.assertEqual(plan["actions"][0]["proof"]["kind"], "every-commit-patch")
        self.assertEqual(len(plan["actions"][0]["proof"]["ahead"]), 2)

    def test_whitespace_difference_is_not_patch_equivalence(self):
        self.git("switch", "-c", "feature")
        self.commit("indent", " x\n")
        self.git("switch", "main")
        self.commit("indent", "  x\n")
        self.git("push", "origin", "main")
        self.assertEqual(self.repo.plan("local-branches")["actions"], [])

    def test_empty_commit_and_merge_commit_are_not_silently_ignored(self):
        self.git("switch", "-c", "feature")
        self.git("commit", "--allow-empty", "-m", "empty")
        self.git("switch", "main")
        self.assertEqual(self.repo.plan("local-branches")["actions"], [])
        self.git("switch", "-c", "side")
        self.commit("side", "side\n", "side.txt")
        self.git("switch", "feature")
        self.git("merge", "--no-ff", "side", "-m", "merge")
        self.git("switch", "main")
        self.git("cherry-pick", "side")
        self.git("push", "origin", "main")
        self.assertNotIn("refs/heads/feature", self.action_names(self.repo.plan("local-branches")))

    def test_protected_branch_names_are_literal_strings(self):
        self.git("branch", "release.v1")
        self.git("branch", "releaseXv1")
        self.git("branch", "master")
        self.git("push", "origin", "release.v1")
        plan = self.repo.plan("local-branches", "release.v1")
        self.assertEqual(self.action_names(plan), ["refs/heads/releaseXv1"])

    def test_changed_ref_is_skipped(self):
        self.git("branch", "feature")
        plan = self.repo.plan("local-branches")
        self.git("switch", "feature")
        new = self.commit("new", "new\n")
        self.git("switch", "main")
        self.assertEqual(self.repo.apply(plan, "local-branches")[0]["result"], "skipped")
        self.assertEqual(self.git("rev-parse", "feature"), new)

    def test_current_head_or_trunk_change_stops_apply(self):
        self.git("branch", "feature")
        plan = self.repo.plan("local-branches")
        self.commit("new trunk", "new\n")
        with self.assertRaises(Refused):
            self.repo.apply(plan, "local-branches")

    def test_alternate_push_destination_is_rejected_before_planning(self):
        self.git("config", "remote.origin.pushurl", "https://github.com/other/repo.git")
        with self.assertRaises(Refused):
            self.repo.plan("remote-branches")

    def test_scope_and_repository_identity_are_bound_to_plan(self):
        self.git("branch", "feature")
        plan = self.repo.plan("local-branches")
        with self.assertRaises(Refused):
            self.repo.apply(plan, "all")
        plan["context"]["repository"] = "different/repo"
        with self.assertRaises(Refused):
            self.repo.apply(plan, "local-branches")

    def test_open_pr_prevents_deletion_even_when_ancestor(self):
        self.git("branch", "feature")
        self.prs = [{"state": "open", "head": {"ref": "feature", "repo": {"full_name": "owner/repo"}},
                     "base": {"repo": {"full_name": "owner/repo"}}}]
        self.assertEqual(self.repo.plan("local-branches")["actions"], [])

    def test_git_error_is_never_an_empty_success(self):
        self.git("branch", "feature")
        original = self.repo.git
        def git(*args):
            if args[0] == "rev-list":
                raise Refused("injected rev-list failure")
            return original(*args)
        with patch.object(self.repo, "git", side_effect=git):
            self.assertEqual(self.repo.plan("local-branches")["actions"], [])
        with self.assertRaises(Refused):
            self.repo.ancestor("missing-object", self.git("rev-parse", "main"))

    def make_worktree(self):
        worktree = self.root / ".worktrees" / "feature"
        self.git("worktree", "add", "-b", "feature", str(worktree), "main")
        return worktree

    def test_worktree_only_removes_checkout_and_preserves_all_refs(self):
        worktree = self.make_worktree()
        self.git("push", "origin", "feature")
        self.git("update-ref", "refs/remotes/origin/stale", self.git("rev-parse", "main"))
        before = self.git("show-ref")
        plan = self.repo.plan("worktrees")
        result = self.repo.apply(plan, "worktrees", exclusive_worktrees=True)
        self.assertEqual(result[0]["result"], "removed")
        self.assertFalse(worktree.exists())
        self.assertEqual(self.git("show-ref"), before)
        commands = [call.args for call in self.repo.run.call_args_list]
        self.assertFalse(any("fetch" in cmd or "prune" in cmd for cmd in commands))

    def test_dirty_ignored_or_changed_worktree_is_preserved(self):
        worktree = self.make_worktree()
        plan = self.repo.plan("worktrees")
        (worktree / "untracked").write_text("keep")
        self.assertEqual(self.repo.apply(plan, "worktrees", exclusive_worktrees=True)[0]["result"], "skipped")
        (worktree / "untracked").unlink()
        (worktree / ".gitignore").write_text("cache\n")
        self.command("git", "-C", str(worktree), "add", ".gitignore")
        self.command("git", "-C", str(worktree), "commit", "-m", "new head")
        self.assertEqual(self.repo.apply(plan, "worktrees", exclusive_worktrees=True)[0]["result"], "skipped")
        self.assertTrue(worktree.exists())

    def test_worktree_removal_requires_exclusive_access_assertion(self):
        worktree = self.make_worktree()
        plan = self.repo.plan("worktrees")
        self.assertEqual(self.repo.apply(plan, "worktrees")[0]["result"], "skipped")
        self.assertTrue(worktree.exists())

    def test_ignored_files_preserve_worktree(self):
        worktree = self.make_worktree()
        plan = self.repo.plan("worktrees")
        (self.root / ".git/info/exclude").write_text("cache\n")
        (worktree / "cache").write_text("valuable ignored data")
        result = self.repo.apply(plan, "worktrees", exclusive_worktrees=True)
        self.assertEqual(result[0]["result"], "skipped")
        self.assertTrue((worktree / "cache").exists())

    def test_detached_clean_worktree_ancestor_is_removable(self):
        worktree = self.root / ".worktrees/detached"
        self.git("worktree", "add", "--detach", str(worktree), "main")
        plan = self.repo.plan("worktrees")
        result = self.repo.apply(plan, "worktrees", exclusive_worktrees=True)
        self.assertEqual(result[0]["result"], "removed")
        self.assertFalse(worktree.exists())

    def test_worktree_is_rechecked_after_other_candidate_proofs(self):
        worktree = self.make_worktree()
        plan = self.repo.plan("worktrees")
        original = self.repo.plan
        def replan(*args):
            fresh = original(*args)
            (worktree / "late-file").write_text("keep")
            return fresh
        with patch.object(self.repo, "plan", side_effect=replan):
            result = self.repo.apply(plan, "worktrees", exclusive_worktrees=True)
        self.assertEqual(result[0]["result"], "skipped")
        self.assertTrue((worktree / "late-file").exists())

    def test_locked_worktree_and_checked_out_branch_are_preserved(self):
        worktree = self.make_worktree()
        self.git("worktree", "lock", str(worktree))
        self.assertEqual(self.repo.plan("all")["actions"], [])
        self.git("worktree", "unlock", str(worktree))

    def test_dry_run_does_not_mutate_refs_index_or_worktrees(self):
        self.git("branch", "feature")
        before = self.git("show-ref"), (self.root / ".git/index").read_bytes(), self.git("worktree", "list", "--porcelain")
        self.repo.plan("all")
        after = self.git("show-ref"), (self.root / ".git/index").read_bytes(), self.git("worktree", "list", "--porcelain")
        self.assertEqual(after, before)

    def test_remote_deletion_lease_rejects_ref_moved_after_revalidation(self):
        self.git("branch", "feature")
        self.git("push", "origin", "feature")
        plan = self.repo.plan("remote-branches")
        self.git("switch", "feature")
        new = self.commit("new", "new\n")
        self.git("push", "origin", "feature:staging")
        self.git("switch", "main")
        original = self.repo.git
        def git(*args):
            if args[0] == "push":
                self.command("git", "--git-dir", str(self.remote), "update-ref", "refs/heads/feature", new)
            return original(*args)
        with patch.object(self.repo, "git", side_effect=git):
            self.assertEqual(self.repo.apply(plan, "remote-branches")[0]["result"], "skipped")
        self.assertEqual(self.repo.remote_heads()["refs/heads/feature"], new)

    def test_local_cas_rejects_ref_moved_after_revalidation(self):
        self.git("branch", "feature")
        plan = self.repo.plan("local-branches")
        self.git("switch", "-c", "other")
        new = self.commit("new", "new\n")
        self.git("switch", "main")
        original = self.repo.git
        def git(*args):
            if args[0] == "update-ref":
                self.git("update-ref", "refs/heads/feature", new)
            return original(*args)
        with patch.object(self.repo, "git", side_effect=git):
            self.assertEqual(self.repo.apply(plan, "local-branches")[0]["result"], "skipped")
        self.assertEqual(self.git("rev-parse", "feature"), new)


if __name__ == "__main__":
    unittest.main()
