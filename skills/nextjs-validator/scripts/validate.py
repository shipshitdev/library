#!/usr/bin/env python3
"""
Next.js 16 Validator

Validates Next.js 16 configuration and detects deprecated patterns.
Ensures proxy.ts, Turbopack, App Router, and modern patterns are used.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple


class Issue(NamedTuple):
    severity: str  # 'error' | 'warning'
    file: str
    line: int | None
    message: str
    fix: str | None


class ValidationResult:
    def __init__(self):
        self.issues: list[Issue] = []
        self.passed: list[str] = []
        self.next_version: str | None = None

    def add_issue(self, severity: str, file: str, message: str, line: int | None = None, fix: str | None = None):
        self.issues.append(Issue(severity, file, line, message, fix))

    def add_passed(self, message: str):
        self.passed.append(message)

    @property
    def has_errors(self) -> bool:
        return any(i.severity == 'error' for i in self.issues)


def check_next_version(root: Path, result: ValidationResult) -> bool:
    """Check if Next.js v16+ is installed."""
    pkg_path = root / 'package.json'
    if not pkg_path.exists():
        result.add_issue('error', 'package.json', 'package.json not found')
        return False

    try:
        with open(pkg_path) as f:
            pkg = json.load(f)
    except json.JSONDecodeError:
        result.add_issue('error', 'package.json', 'Invalid JSON')
        return False

    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}

    if 'next' not in deps:
        result.add_issue('error', 'package.json', 'next not found in dependencies',
                        fix='bun add next@latest')
        return False

    version = deps['next']
    result.next_version = version

    version_match = re.search(r'(\d+)\.', version)
    if version_match:
        major = int(version_match.group(1))
        if major < 16:
            result.add_issue('error', 'package.json',
                           f'Next.js {major} detected. Must use v16+',
                           fix='bun add next@latest')
            return False
        result.add_passed(f'Next.js version: {version}')
        return True

    result.add_issue('warning', 'package.json', f'Could not parse Next.js version: {version}')
    return True


def check_directory_structure(root: Path, result: ValidationResult):
    """Check for App Router vs Pages Router."""
    app_dir = root / 'app'
    src_app_dir = root / 'src' / 'app'
    pages_dir = root / 'pages'
    src_pages_dir = root / 'src' / 'pages'

    has_app = app_dir.exists() or src_app_dir.exists()
    has_pages = pages_dir.exists() or src_pages_dir.exists()

    if has_app:
        result.add_passed('Using app/ directory (App Router)')
    else:
        result.add_issue('error', 'Directory Structure',
                        'No app/ directory found - App Router required for Next.js 16',
                        fix='Create app/ directory with layout.tsx and page.tsx')

    if has_pages:
        # Check if it's just API routes (acceptable) or actual pages (not acceptable)
        pages_path = pages_dir if pages_dir.exists() else src_pages_dir
        has_page_files = False
        for f in pages_path.rglob('*.tsx'):
            if 'api' not in str(f):
                has_page_files = True
                break
        for f in pages_path.rglob('*.jsx'):
            if 'api' not in str(f):
                has_page_files = True
                break

        if has_page_files:
            result.add_issue('error', 'pages/',
                           'Found pages/ directory with page files - migrate to App Router',
                           fix='Move pages to app/ directory, use Server Components')
        else:
            result.add_passed('pages/ only contains API routes (acceptable)')


def check_proxy_middleware(root: Path, result: ValidationResult):
    """Check for proxy.ts vs deprecated middleware.ts."""
    # Check common locations
    locations = [root, root / 'src']

    proxy_found = False
    middleware_found = False

    for loc in locations:
        if (loc / 'proxy.ts').exists():
            proxy_found = True
            result.add_passed(f'Found proxy.ts in {loc.relative_to(root) if loc != root else "root"}')

        if (loc / 'middleware.ts').exists():
            middleware_found = True
            result.add_issue('error', str((loc / 'middleware.ts').relative_to(root)),
                           'middleware.ts is deprecated in Next.js 16',
                           fix='Rename to proxy.ts and update to use createProxy()')

        if (loc / 'middleware.js').exists():
            middleware_found = True
            result.add_issue('error', str((loc / 'middleware.js').relative_to(root)),
                           'middleware.js is deprecated in Next.js 16',
                           fix='Rename to proxy.ts and update to use createProxy()')

    if not proxy_found and not middleware_found:
        result.add_passed('No middleware/proxy (optional)')


def check_deprecated_patterns(root: Path, result: ValidationResult):
    """Check for deprecated patterns in code."""
    # Find all TSX/JSX files
    patterns = {
        'getServerSideProps': 'Use Server Components with async/await',
        'getStaticProps': 'Use Server Components with generateStaticParams',
        'getInitialProps': 'Use Server Components',
        'from \'next/router\'': 'Use next/navigation instead',
        'from "next/router"': 'Use next/navigation instead',
    }

    # Search in app/ and src/ directories
    search_dirs = ['app', 'src/app', 'pages', 'src/pages', 'components', 'src/components']

    for dir_name in search_dirs:
        dir_path = root / dir_name
        if not dir_path.exists():
            continue

        for ext in ['*.tsx', '*.ts', '*.jsx', '*.js']:
            for file_path in dir_path.rglob(ext):
                if 'node_modules' in str(file_path):
                    continue

                try:
                    content = file_path.read_text()
                    rel_path = file_path.relative_to(root)

                    for pattern, fix in patterns.items():
                        if pattern in content:
                            # Find line number
                            lines = content.split('\n')
                            for i, line in enumerate(lines, 1):
                                if pattern in line:
                                    result.add_issue('error', str(rel_path),
                                                   f'Found deprecated pattern: {pattern}',
                                                   line=i,
                                                   fix=fix)
                                    break
                except:
                    pass


def check_config_file(root: Path, result: ValidationResult):
    """Check next.config format."""
    ts_config = root / 'next.config.ts'
    mts_config = root / 'next.config.mts'
    js_config = root / 'next.config.js'
    mjs_config = root / 'next.config.mjs'

    if ts_config.exists() or mts_config.exists():
        result.add_passed('Using TypeScript config (next.config.ts)')
    elif js_config.exists() or mjs_config.exists():
        result.add_issue('warning', 'next.config.js',
                        'Consider using next.config.ts for type safety',
                        fix='Rename to next.config.ts and add types')
    else:
        result.add_passed('No next.config (using defaults)')


def check_use_cache(root: Path, result: ValidationResult):
    """Check for 'use cache' directive usage."""
    search_dirs = ['app', 'src/app']
    use_cache_found = False

    for dir_name in search_dirs:
        dir_path = root / dir_name
        if not dir_path.exists():
            continue

        for file_path in dir_path.rglob('*.tsx'):
            if 'node_modules' in str(file_path):
                continue
            try:
                content = file_path.read_text()
                if "'use cache'" in content or '"use cache"' in content:
                    use_cache_found = True
                    break
            except:
                pass

    if use_cache_found:
        result.add_passed('Using Cache Components (use cache)')
    else:
        result.add_issue('warning', 'Cache Components',
                        'Consider using \'use cache\' for cacheable pages',
                        fix='Add \'use cache\' directive to cacheable Server Components')


def print_report(result: ValidationResult, verbose: bool = False):
    """Print validation report."""
    print("\n" + "=" * 50)
    print("  Next.js 16 Validation Report")
    print("=" * 50 + "\n")

    if result.next_version:
        print(f"Package Version: next@{result.next_version.lstrip('^~>=')}")
        print()

    if verbose and result.passed:
        print("Passed Checks:")
        for msg in result.passed:
            print(f"  [PASS] {msg}")
        print()

    if result.issues:
        errors = [i for i in result.issues if i.severity == 'error']
        warnings = [i for i in result.issues if i.severity == 'warning']

        if errors:
            print("Errors:")
            for issue in errors:
                line_info = f":{issue.line}" if issue.line else ""
                print(f"  [ERROR] {issue.file}{line_info}")
                print(f"          {issue.message}")
                if issue.fix:
                    print(f"          Fix: {issue.fix}")
            print()

        if warnings:
            print("Warnings:")
            for issue in warnings:
                line_info = f":{issue.line}" if issue.line else ""
                print(f"  [WARN] {issue.file}{line_info}")
                print(f"         {issue.message}")
                if issue.fix:
                    print(f"         Fix: {issue.fix}")
            print()

    print("-" * 50)
    error_count = len([i for i in result.issues if i.severity == 'error'])
    warning_count = len([i for i in result.issues if i.severity == 'warning'])

    if error_count == 0 and warning_count == 0:
        print("Result: All checks passed! Project is using Next.js 16 correctly.")
    else:
        print(f"Result: {error_count} error(s), {warning_count} warning(s)")

    print()


def main():
    parser = argparse.ArgumentParser(description='Validate Next.js 16 configuration')
    parser.add_argument('--root', '-r', type=str, default='.', help='Project root directory')
    parser.add_argument('--strict', action='store_true', help='Treat warnings as errors')
    parser.add_argument('--ci', action='store_true', help='CI mode: exit with non-zero on errors')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show passed checks')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()
    root = Path(args.root).resolve()

    if not root.exists():
        print(f"Error: Directory not found: {root}")
        sys.exit(1)

    result = ValidationResult()

    # Run all checks
    check_next_version(root, result)
    check_directory_structure(root, result)
    check_proxy_middleware(root, result)
    check_deprecated_patterns(root, result)
    check_config_file(root, result)
    check_use_cache(root, result)

    # Output
    if args.json:
        output = {
            'next_version': result.next_version,
            'passed': result.passed,
            'issues': [
                {
                    'severity': i.severity,
                    'file': i.file,
                    'line': i.line,
                    'message': i.message,
                    'fix': i.fix
                }
                for i in result.issues
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print_report(result, verbose=args.verbose)

    # Exit code
    if args.ci or args.strict:
        if result.has_errors:
            sys.exit(1)
        if args.strict and any(i.severity == 'warning' for i in result.issues):
            sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
