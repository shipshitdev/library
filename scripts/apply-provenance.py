#!/usr/bin/env python3
"""Apply upstream provenance to a skill's SKILL.md frontmatter + README.md.

Idempotent. Operates ONLY inside the `metadata:` block of the YAML frontmatter
(never touches a top-level `license:`). Strips any pre-existing provenance keys
inside that block, then inserts a canonical provenance block right after the
`version:` line. Generates/refreshes the README `## Upstream` section.

Driven by a JSON manifest on argv[1]:
  { "skills": [ { skill, desc, source, source_path, upstream_repo, upstream_ref,
                  upstream_commit, last_synced, license, modifications, mode,
                  upstream_version, upstream_latest } ] }
mode: "rolling" (main + commit) | "tagged" (upstream_version/upstream_latest)
"""
import json
import sys
import pathlib

PROV_KEYS = {
    "source", "upstream_repo", "upstream_ref", "upstream_commit",
    "upstream_version", "upstream_latest", "last_synced",
}  # metadata-block `license` is managed here too; top-level `license:` untouched.

SKILLS_DIR = pathlib.Path(__file__).resolve().parent.parent / "skills"


def split_frontmatter(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise ValueError("no frontmatter")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], lines[i + 1:]
    raise ValueError("unterminated frontmatter")


def edit_metadata(fm_lines, entry):
    start = next((i for i, l in enumerate(fm_lines) if l.rstrip() == "metadata:"), None)
    if start is None:
        raise ValueError("no metadata: block")
    end = len(fm_lines)
    for i in range(start + 1, len(fm_lines)):
        l = fm_lines[i]
        if l.strip() == "":
            continue
        if not l.startswith("  "):
            end = i
            break
    block = fm_lines[start + 1:end]
    drop = PROV_KEYS | {"license"}
    if entry.get("drop_author"):
        drop = drop | {"author"}
    kept = [l for l in block
            if (l.strip().split(":", 1)[0] if ":" in l else "") not in drop]
    prov = [f"  source: {entry['source']}"]
    if entry.get("mode") == "tagged":
        prov.append(f"  upstream_version: {entry['upstream_version']}")
        prov.append(f"  upstream_latest: {entry['upstream_latest']}")
    else:
        prov.append(f"  upstream_repo: {entry['upstream_repo']}")
        prov.append(f"  upstream_ref: {entry['upstream_ref']}")
        prov.append(f"  upstream_commit: {entry['upstream_commit']}")
    prov.append(f'  last_synced: "{entry["last_synced"]}"')
    prov.append(f"  license: {entry['license']}")
    vidx = next((i for i, l in enumerate(kept) if l.strip().startswith("version:")), -1)
    at = vidx + 1 if vidx >= 0 else 0
    new_block = kept[:at] + prov + kept[at:]
    return fm_lines[:start + 1] + new_block + fm_lines[end:]


def render_readme(entry):
    name = entry["skill"]
    repo = entry["upstream_repo"]
    src = entry["source"]
    src_label = f"`{entry['source_path']}`"
    rows = [f"| Source | [{src_label}]({src}) |"]
    if entry.get("mode") == "tagged":
        rows.append(f"| Forked at | `{entry['upstream_version']}` |")
        rows.append(f"| Upstream latest | `{entry['upstream_latest']}` |")
        check = f"diff [{src_label}]({src}) against tag `{entry['upstream_version']}`"
    else:
        rows.append(f"| Upstream ref | `{entry['upstream_ref']}` |")
        rows.append(f"| Synced at commit | `{entry['upstream_commit']}` |")
        check = (f"diff [{src_label}]({src}) on `{entry['upstream_ref']}` since commit "
                 f"`{entry['upstream_commit']}`")
    rows.append(f"| Last synced | {entry['last_synced']} |")
    rows.append(f"| License | {entry['license']} |")
    table = "\n".join(rows)
    desc = entry.get("desc", "").strip()
    desc_block = f"\n{desc}\n" if desc else ""
    repo_url = f"https://github.com/{repo}"
    return f"""# {name}
{desc_block}
## Upstream

Derived from **[{repo}]({repo_url})** ({entry['license']}).

| Field | Value |
|-------|-------|
{table}

**Local modifications:** {entry['modifications']}

**Checking for upstream changes:** when upstream has moved ahead of the synced marker above, {check}, port anything worth bringing home, then bump `metadata.upstream_commit` (or `metadata.upstream_version`) and `metadata.last_synced` in `SKILL.md` and this table.
"""


def main():
    manifest = json.loads(pathlib.Path(sys.argv[1]).read_text())
    for entry in manifest["skills"]:
        sd = SKILLS_DIR / entry["skill"]
        sk = sd / "SKILL.md"
        fm, body = split_frontmatter(sk.read_text())
        fm2 = edit_metadata(fm, entry)
        body_text = "\n".join(body)
        sk.write_text("---\n" + "\n".join(fm2) + "\n---\n" + body_text.lstrip("\n"))
        (sd / "README.md").write_text(render_readme(entry))
        print(f"✓ {entry['skill']}")


if __name__ == "__main__":
    main()
