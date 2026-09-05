#!/usr/bin/env python3
"""Plan cleanup from immutable Git evidence; apply only an unchanged scoped plan."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


SCOPES = {
    "all": {"local", "remote", "worktree"},
    "branches": {"local", "remote"},
    "local-branches": {"local"},
    "remote-branches": {"remote"},
    "worktrees": {"worktree"},
}


class Refused(RuntimeError):
    """Evidence is missing, changed, or unsafe."""


class Repository:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def run(self, *args: str, input_text: str | None = None,
            accepted: tuple[int, ...] = (0,)) -> subprocess.CompletedProcess:
        env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_NO_REPLACE_OBJECTS="1")
        result = subprocess.run(args, cwd=self.root, text=True, input=input_text,
                                capture_output=True, env=env, check=False)
        if result.returncode not in accepted:
            raise Refused(f"{args[0]} {args[1]} failed ({result.returncode}); no proof")
        return result

    def git(self, *args: str) -> str:
        return self.run("git", *args).stdout.strip()

    def oid(self, ref: str) -> str:
        return self.git("rev-parse", "--verify", f"{ref}^{{commit}}")

    def ancestor(self, older: str, newer: str) -> bool:
        return self.run("git", "merge-base", "--is-ancestor", older, newer,
                        accepted=(0, 1)).returncode == 0

    def patch_id(self, patch: str) -> str:
        # Exact whitespace matters for a deletion proof; --stable ignores it.
        output = self.run("git", "patch-id", "--verbatim", input_text=patch).stdout.split()
        return output[0] if output else ""

    def patch(self, older: str, newer: str) -> str:
        return self.patch_id(self.git("diff", "--no-ext-diff", "--no-textconv",
                                      "--binary", older, newer, "--"))

    def worktrees(self) -> list[dict]:
        records = []
        for block in self.run("git", "worktree", "list", "--porcelain", "-z").stdout.split("\0\0"):
            record = {}
            for line in block.split("\0"):
                key, _, value = line.partition(" ")
                if key:
                    record[key] = value
            if record:
                records.append(record)
        return records

    def worktree_state(self, record: dict) -> dict:
        path = Path(record["worktree"])
        if path.is_symlink() or not path.is_dir():
            raise Refused("missing or symlink worktree")
        head = self.git("-C", str(path), "rev-parse", "HEAD")
        branch = self.run("git", "-C", str(path), "symbolic-ref", "-q", "HEAD",
                          accepted=(0, 1)).stdout.strip()
        status = self.run("git", "-C", str(path), "status", "--porcelain=v1", "-z",
                          "--untracked-files=all", "--ignored", "--ignore-submodules=none").stdout
        if status or "locked" in record or "prunable" in record:
            raise Refused("dirty, ignored files, locked, or stale worktree")
        return {"path": str(path.resolve()), "oid": head, "ref": branch}

    def remote_heads(self) -> dict[str, str]:
        return {ref: oid for oid, ref in (line.split("\t") for line in
                self.git("ls-remote", "--heads", "origin").splitlines())}

    def context(self, trunk: str | None = None) -> dict:
        metadata = json.loads(self.run("gh", "repo", "view", "--json",
                                       "nameWithOwner,defaultBranchRef").stdout)
        trunk = trunk or metadata["defaultBranchRef"]["name"]
        self.git("check-ref-format", f"refs/heads/{trunk}")
        remote = self.git("remote", "get-url", "origin")
        push_urls = self.git("remote", "get-url", "--push", "--all", "origin").splitlines()
        if push_urls != [remote]:
            raise Refused("origin push destination differs or has multiple URLs")
        # Resolve the origin itself: gh's inferred repository may be a parent fork.
        origin_metadata = json.loads(self.run("gh", "repo", "view", remote, "--json",
                                              "nameWithOwner").stdout)
        if origin_metadata["nameWithOwner"].lower() != metadata["nameWithOwner"].lower():
            raise Refused("origin repository differs from selected GitHub repository")
        remote_oid = self.remote_heads().get(f"refs/heads/{trunk}")
        if not remote_oid or self.oid(remote_oid) != remote_oid:
            raise Refused("remote trunk object unavailable; refresh separately without pruning")
        current = self.run("git", "symbolic-ref", "-q", "HEAD", accepted=(0, 1)).stdout.strip()
        return {"root": str(self.root), "common": self.git("rev-parse", "--path-format=absolute", "--git-common-dir"),
                "repository": metadata["nameWithOwner"], "remote": remote,
                "trunk": trunk, "trunk_oid": remote_oid, "current": current,
                "head": self.oid("HEAD")}

    def pull_requests(self, repository: str, branch: str) -> list[dict]:
        owner = repository.split("/")[0]
        pages = json.loads(self.run("gh", "api", "--method", "GET", "--paginate", "--slurp",
                                    f"repos/{repository}/pulls", "-f", "state=all", "-f",
                                    f"head={owner}:{branch}", "-f", "per_page=100").stdout)
        records = []
        for page in pages:
            for pr in page:
                head = pr.get("head") or {}
                head_repo = head.get("repo") or {}
                base_repo = (pr.get("base") or {}).get("repo") or {}
                if (head_repo.get("full_name", "").lower() == repository.lower()
                        and base_repo.get("full_name", "").lower() == repository.lower()
                        and head.get("ref") == branch):
                    records.append(pr)
        return records

    def proof(self, oid: str, trunk: str, prs: list[dict]) -> dict:
        if any(pr.get("state") == "open" for pr in prs):
            raise Refused("in-flight open PR")
        ahead = self.git("rev-list", trunk + ".." + oid).splitlines()
        if self.ancestor(oid, trunk):
            return {"kind": "ancestor", "ahead": ahead}
        # Every non-upstream commit is accounted for. Merge commits and empty
        # patches are deliberately not silently omitted as they are by git cherry.
        upstream = self.git("rev-list", "--max-count=500", trunk).splitlines()
        upstream_patches = set()
        for commit in upstream:
            parents = self.git("rev-list", "--parents", "-n", "1", commit).split()[1:]
            if len(parents) == 1:
                patch = self.patch(parents[0], commit)
                if patch:
                    upstream_patches.add(patch)
        covered = []
        for commit in ahead:
            parents = self.git("rev-list", "--parents", "-n", "1", commit).split()[1:]
            if len(parents) == 1 and self.patch(parents[0], commit) in upstream_patches:
                covered.append(commit)
        if ahead and covered == ahead:
            return {"kind": "every-commit-patch", "ahead": ahead}
        # Squash proof binds the entire candidate history to the exact merged
        # PR head, then compares its cumulative content with the landed commit.
        for pr in prs:
            merge = pr.get("merge_commit_sha")
            if not pr.get("merged_at") or pr["head"].get("sha") != oid or not merge:
                continue
            if not self.ancestor(merge, trunk):
                continue
            parents = self.git("rev-list", "--parents", "-n", "1", merge).split()[1:]
            if len(parents) != 1:
                continue
            base = self.git("merge-base", oid, parents[0])
            candidate_patch = self.patch(base, oid)
            if candidate_patch and candidate_patch == self.patch(parents[0], merge):
                return {"kind": "exact-pr-head-squash", "pr": pr["number"],
                        "head": oid, "merge": merge, "ahead": ahead}
        raise Refused("candidate history not proven in trunk")

    def plan(self, scope: str, trunk: str | None = None) -> dict:
        context = self.context(trunk)
        protected = {"main", "master", "HEAD", context["trunk"],
                     context["current"].removeprefix("refs/heads/")}
        worktrees = self.worktrees()
        remote_heads = self.remote_heads()
        candidates = []
        if "worktree" in SCOPES[scope]:
            for record in worktrees:
                path = record["worktree"]
                if Path(path).resolve() == self.root or record == worktrees[0]:
                    continue
                candidates.append({"kind": "worktree", "path": path,
                                   "ref": record.get("branch", ""), "oid": record.get("HEAD", ""),
                                   "record": record})
        if "local" in SCOPES[scope]:
            for line in self.git("for-each-ref", "--format=%(refname) %(objectname)", "refs/heads/").splitlines():
                ref, oid = line.split(" ")
                candidates.append({"kind": "local", "ref": ref, "oid": oid})
        if "remote" in SCOPES[scope]:
            for ref, oid in remote_heads.items():
                candidates.append({"kind": "remote", "ref": ref, "oid": oid})
        actions, skipped, pr_cache = [], [], {}
        for candidate in candidates:
            record = candidate.pop("record", None)
            branch = candidate["ref"].removeprefix("refs/heads/")
            try:
                if branch in protected:
                    raise Refused("protected branch")
                if candidate["kind"] == "worktree":
                    candidate.update(self.worktree_state(record))
                elif candidate["kind"] == "local" and any(
                    wt.get("branch") == candidate["ref"] for wt in worktrees
                ):
                    raise Refused("branch checked out; remove worktree, then replan")
                self.oid(candidate["oid"])
                if branch and branch not in pr_cache:
                    pr_cache[branch] = self.pull_requests(context["repository"], branch)
                candidate["proof"] = self.proof(candidate["oid"], context["trunk_oid"], pr_cache.get(branch, []))
                actions.append(candidate)
            except Refused as error:
                skipped.append({**candidate, "reason": str(error)})
        return {"version": 1, "scope": scope, "context": context, "actions": actions, "skipped": skipped}

    def revalidate(self, context: dict, action: dict) -> None:
        if self.context(context["trunk"]) != context:
            raise Refused("repository changed immediately before deletion")
        if action["kind"] == "remote":
            if self.remote_heads().get(action["ref"]) != action["oid"]:
                raise Refused("remote ref changed immediately before deletion")
        elif action["kind"] == "local":
            if self.oid(action["ref"]) != action["oid"]:
                raise Refused("local ref changed immediately before deletion")
            if any(wt.get("branch") == action["ref"] for wt in self.worktrees()):
                raise Refused("branch checked out immediately before deletion")
        elif action["kind"] == "worktree":
            records = [wt for wt in self.worktrees() if wt["worktree"] == action["path"]]
            if len(records) != 1:
                raise Refused("worktree registration changed immediately before deletion")
            state = self.worktree_state(records[0])
            if any(state[key] != action[key] for key in ("path", "oid", "ref")):
                raise Refused("worktree HEAD changed immediately before deletion")

    def apply(self, plan: dict, scope: str, *, exclusive_worktrees: bool = False) -> list[dict]:
        if plan.get("version") != 1 or plan.get("scope") != scope:
            raise Refused("plan format or authorized scope differs")
        if self.context(plan["context"]["trunk"]) != plan["context"]:
            raise Refused("repository, trunk, or current checkout changed; replan")
        results = []
        for action in plan["actions"]:
            try:
                if action["kind"] == "worktree" and not exclusive_worktrees:
                    raise Refused("exclusive worktree access not established")
                # Recompute proof and state immediately before each mutation.
                fresh = self.plan(scope, plan["context"]["trunk"])
                if fresh["context"] != plan["context"] or action not in fresh["actions"]:
                    raise Refused("candidate or repository changed; replan")
                self.revalidate(plan["context"], action)
                if action["kind"] == "local":
                    # CAS prevents deleting newer commits; never branch -D.
                    self.git("update-ref", "--no-deref", "-d", action["ref"], action["oid"])
                elif action["kind"] == "remote":
                    self.git("push", f"--force-with-lease={action['ref']}:{action['oid']}",
                             "origin", f":{action['ref']}")
                elif action["kind"] == "worktree":
                    self.git("worktree", "remove", "--", action["path"])
                else:
                    raise Refused("unknown action")
                results.append({**action, "result": "removed"})
            except Refused as error:
                results.append({**action, "result": "skipped", "reason": str(error)})
        return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("verify", "dry-run", "prune"), nargs="?", default="dry-run")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--scope", choices=SCOPES, default="all")
    parser.add_argument("--trunk")
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--confirmed", action="store_true")
    parser.add_argument("--exclusive-worktrees", action="store_true",
                        help="Assert exclusive access to candidate worktrees before removal")
    args = parser.parse_args()
    try:
        for executable in ("git", "gh", "jq"):
            if not shutil.which(executable):
                raise Refused(f"missing prerequisite: {executable}")
        repo = Repository(args.root)
        if args.mode == "prune":
            if not args.confirmed or not args.plan:
                raise Refused("prune requires the reviewed --plan and existing authorization via --confirmed")
            result = repo.apply(json.loads(args.plan.read_text()), args.scope,
                                exclusive_worktrees=args.exclusive_worktrees)
        else:
            result = repo.plan(args.scope, args.trunk)
        print(json.dumps(result, indent=2))
        return 0
    except (Refused, OSError, ValueError, KeyError, TypeError) as error:
        print(f"Cleanup stopped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
