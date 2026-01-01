#!/usr/bin/env python3
"""
Convert all package.json files to use exact versions instead of ranges.
Queries npm registry for latest available versions.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def query_npm_latest(package_name: str) -> str | None:
    """Query npm registry for the latest version of a package."""
    try:
        # Use npm view command (most reliable)
        result = subprocess.run(
            ["npm", "view", package_name, "version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            if version and version != "undefined":
                return version

        # Fallback: query npm registry API directly
        import urllib.request
        import urllib.error
        url = f"https://registry.npmjs.org/{package_name}/latest"
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                if "version" in data:
                    return data["version"]
        except (urllib.error.URLError, json.JSONDecodeError, KeyError):
            pass

    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print(f"Warning: Could not query version for {package_name}: {e}", file=sys.stderr)
    return None


def get_latest_version_from_range(package_name: str, current_version: str) -> str:
    """Get the latest version that matches the current range, or latest if range is 'latest'."""
    # Handle "latest" tag
    if current_version == "latest" or current_version == "*":
        latest = query_npm_latest(package_name)
        if latest:
            return latest
        return current_version  # Fallback to keeping "latest"

    # Handle exact versions (no range)
    if not current_version.startswith(("^", "~", ">", "<", ">=", "<=")):
        return current_version

    # For ranges, query latest version
    # The npm registry will give us the latest version
    latest = query_npm_latest(package_name)
    if latest:
        return latest

    # Fallback: remove the range prefix and return
    return current_version.lstrip("^~>=<")


def should_skip_package(package_name: str, version: str) -> bool:
    """Check if we should skip converting this package (workspace, local, git, etc.)."""
    # Skip workspace packages
    if version.startswith("workspace:"):
        return True

    # Skip local file references
    if version.startswith("file:") or version.startswith("path:"):
        return True

    # Skip git references
    if version.startswith("git+") or version.startswith("git:"):
        return True

    # Skip npm aliases (e.g., "npm:package@version")
    if version.startswith("npm:"):
        return True

    return False


def convert_package_json(file_path: Path) -> bool:
    """Convert a single package.json file to use exact versions."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            data = json.loads(content)

        modified = False
        cache: dict[str, str] = {}  # Cache for version lookups

        # Process dependencies
        for deps_key in ["dependencies", "devDependencies", "peerDependencies", "optionalDependencies"]:
            if deps_key not in data:
                continue

            deps = data[deps_key]
            for package_name, current_version in list(deps.items()):
                # Skip special package types
                if should_skip_package(package_name, current_version):
                    continue

                # Check if version needs conversion
                if current_version == "latest" or current_version.startswith(("^", "~")):
                    # Use cache if available
                    if package_name in cache:
                        new_version = cache[package_name]
                    else:
                        new_version = get_latest_version_from_range(package_name, current_version)
                        cache[package_name] = new_version

                    if new_version != current_version:
                        deps[package_name] = new_version
                        modified = True
                        print(f"  {package_name}: {current_version} -> {new_version}")

        if modified:
            # Write back with proper formatting
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")  # Add trailing newline
            return True

        return False

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return False


def find_package_json_files(root: Path) -> list[Path]:
    """Find all package.json files, excluding node_modules."""
    package_files = []
    for path in root.rglob("package.json"):
        # Skip node_modules
        if "node_modules" in path.parts:
            continue
        package_files.append(path)
    return sorted(package_files)


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])
    else:
        # Default to workspace root (parent of library)
        root_dir = Path(__file__).parent.parent.parent

    if not root_dir.exists():
        print(f"Error: Directory {root_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning for package.json files in {root_dir}...")
    package_files = find_package_json_files(root_dir)

    if not package_files:
        print("No package.json files found.")
        return

    print(f"Found {len(package_files)} package.json files")
    print()

    modified_count = 0
    for package_file in package_files:
        rel_path = package_file.relative_to(root_dir)
        print(f"Processing {rel_path}...")
        if convert_package_json(package_file):
            modified_count += 1
            print(f"  ✓ Modified")
        else:
            print(f"  - No changes needed")
        print()

    print(f"Summary: Modified {modified_count} out of {len(package_files)} package.json files")


if __name__ == "__main__":
    main()

