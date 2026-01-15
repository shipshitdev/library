#!/usr/bin/env python3
"""
Deploy landing pages to Vercel with custom domain configuration.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def check_vercel_cli() -> bool:
    """Check if Vercel CLI is installed."""
    try:
        subprocess.run(["vercel", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_vercel_project_id(project_dir: Path) -> str | None:
    """Get Vercel project ID from .vercel directory."""
    vercel_dir = project_dir / ".vercel"
    project_json = vercel_dir / "project.json"
    if project_json.exists():
        with open(project_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("projectId")
    return None


def deploy_project(
    project_dir: Path,
    domain: str | None,
    production: bool,
    yes: bool,
) -> dict[str, Any]:
    """Deploy a single project to Vercel."""
    if not project_dir.exists():
        raise FileNotFoundError(f"Project directory not found: {project_dir}")

    cmd = ["vercel", "--yes"] if yes else ["vercel"]
    if production:
        cmd.append("--prod")

    result = subprocess.run(
        cmd,
        cwd=project_dir,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Deployment failed: {result.stderr}")

    # Extract deployment URL from output
    output = result.stdout
    deployment_url = None
    for line in output.split("\n"):
        if "https://" in line and ".vercel.app" in line:
            deployment_url = line.strip().split()[-1]
            break

    project_id = get_vercel_project_id(project_dir)

    result_info = {
        "project_dir": str(project_dir),
        "deployment_url": deployment_url,
        "project_id": project_id,
        "domain": domain,
    }

    # Add domain if provided
    if domain and project_id:
        try:
            add_domain_cmd = [
                "vercel",
                "domains",
                "add",
                domain,
                "--yes",
            ]
            domain_result = subprocess.run(
                add_domain_cmd,
                cwd=project_dir,
                capture_output=True,
                text=True,
            )
            if domain_result.returncode == 0:
                result_info["domain_added"] = True
                result_info["domain_status"] = "added"
            else:
                result_info["domain_added"] = False
                result_info["domain_error"] = domain_result.stderr
        except Exception as e:
            result_info["domain_added"] = False
            result_info["domain_error"] = str(e)

    return result_info


def batch_deploy(
    projects: list[Path],
    domains: dict[str, str] | None,
    production: bool,
    yes: bool,
) -> list[dict[str, Any]]:
    """Deploy multiple projects to Vercel."""
    results = []

    for project_dir in projects:
        project_dir = project_dir.resolve()
        slug = project_dir.name
        domain = domains.get(slug) if domains else None

        print(f"\n🚀 Deploying {slug}...")
        if domain:
            print(f"   Domain: {domain}")

        try:
            result = deploy_project(project_dir, domain, production, yes)
            results.append(result)
            print(f"✅ Deployed: {slug}")
            if result.get("deployment_url"):
                print(f"   URL: {result['deployment_url']}")
            if result.get("domain_added"):
                print(f"   Domain: {domain} (added)")
        except Exception as e:
            print(f"❌ Failed: {slug} - {e}", file=sys.stderr)
            results.append({
                "project_dir": str(project_dir),
                "error": str(e),
            })

    return results


def load_domains_from_json(json_path: Path) -> dict[str, str]:
    """Load domain mapping from JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict):
            return data
        elif isinstance(data, list):
            return {item.get("slug", ""): item.get("domain", "") for item in data}
        else:
            raise ValueError("JSON must be an object or array")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deploy landing pages to Vercel with custom domains."
    )
    parser.add_argument(
        "projects",
        nargs="+",
        type=Path,
        help="Project directories to deploy",
    )
    parser.add_argument(
        "--domain",
        type=str,
        help="Single domain to assign to first project",
    )
    parser.add_argument(
        "--domains-json",
        type=Path,
        help="JSON file mapping slugs to domains: {\"slug\": \"domain.com\"}",
    )
    parser.add_argument(
        "--prod",
        action="store_true",
        help="Deploy to production",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompts",
    )

    args = parser.parse_args()

    # Check Vercel CLI
    if not check_vercel_cli():
        print("Error: Vercel CLI not found. Install with: npm i -g vercel", file=sys.stderr)
        sys.exit(1)

    # Load domains
    domains = {}
    if args.domains_json:
        domains = load_domains_from_json(args.domains_json)
    elif args.domain:
        # Assign to first project
        if args.projects:
            domains[args.projects[0].name] = args.domain

    # Deploy
    results = batch_deploy(
        projects=args.projects,
        domains=domains if domains else None,
        production=args.prod,
        yes=args.yes,
    )

    # Summary
    print("\n" + "=" * 50)
    print("📊 Deployment Summary")
    print("=" * 50)
    for result in results:
        if "error" in result:
            print(f"❌ {Path(result['project_dir']).name}: {result['error']}")
        else:
            print(f"✅ {Path(result['project_dir']).name}")
            if result.get("deployment_url"):
                print(f"   URL: {result['deployment_url']}")
            if result.get("domain"):
                print(f"   Domain: {result['domain']}")


if __name__ == "__main__":
    main()

