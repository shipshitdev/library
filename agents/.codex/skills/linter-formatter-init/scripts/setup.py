#!/usr/bin/env python3
"""
Linter Formatter Setup - Initialize ESLint, Prettier, and pre-commit hooks

Usage:
    setup.py --root <path> [options]

Options:
    --root          Project root directory (required)
    --typescript    Enable TypeScript support
    --biome         Use Biome instead of ESLint + Prettier
    --no-hooks      Skip pre-commit hook setup
    --monorepo      Configure for monorepo root
    --dry-run       Show what would be done without making changes

Examples:
    setup.py --root /path/to/project
    setup.py --root /path/to/project --typescript
    setup.py --root /path/to/project --biome
    setup.py --root /path/to/project --typescript --no-hooks
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


# ============================================================================
# Configuration Templates
# ============================================================================

ESLINT_CONFIG = {
    "env": {
        "browser": True,
        "es2021": True,
        "node": True
    },
    "extends": [
        "eslint:recommended",
        "plugin:prettier/recommended"
    ],
    "parserOptions": {
        "ecmaVersion": "latest",
        "sourceType": "module"
    },
    "rules": {
        "no-console": ["warn", {"allow": ["warn", "error"]}],
        "no-unused-vars": ["error", {"argsIgnorePattern": "^_"}],
        "prefer-const": "error",
        "no-var": "error",
        "eqeqeq": ["error", "always"],
        "curly": ["error", "all"]
    }
}

ESLINT_CONFIG_TS = {
    "env": {
        "browser": True,
        "es2021": True,
        "node": True
    },
    "extends": [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended",
        "plugin:prettier/recommended"
    ],
    "parser": "@typescript-eslint/parser",
    "parserOptions": {
        "ecmaVersion": "latest",
        "sourceType": "module"
    },
    "plugins": ["@typescript-eslint"],
    "rules": {
        "no-console": ["warn", {"allow": ["warn", "error"]}],
        "@typescript-eslint/no-unused-vars": ["error", {"argsIgnorePattern": "^_"}],
        "@typescript-eslint/explicit-function-return-type": "off",
        "@typescript-eslint/no-explicit-any": "warn",
        "prefer-const": "error",
        "no-var": "error",
        "eqeqeq": ["error", "always"],
        "curly": ["error", "all"]
    }
}

PRETTIER_CONFIG = {
    "semi": True,
    "singleQuote": True,
    "tabWidth": 2,
    "trailingComma": "es5",
    "printWidth": 100,
    "bracketSpacing": True,
    "arrowParens": "always",
    "endOfLine": "lf"
}

PRETTIER_IGNORE = """# Dependencies
node_modules/

# Build outputs
dist/
build/
.next/
out/

# Cache
.cache/
.turbo/

# Coverage
coverage/

# Lock files
package-lock.json
pnpm-lock.yaml
yarn.lock

# Generated
*.min.js
*.min.css
"""

ESLINT_IGNORE = """# Dependencies
node_modules/

# Build outputs
dist/
build/
.next/
out/

# Cache
.cache/
.turbo/

# Coverage
coverage/
"""

VSCODE_SETTINGS = {
    "editor.formatOnSave": True,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": "explicit"
    },
    "[javascript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[javascriptreact]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[typescript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[typescriptreact]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[json]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[jsonc]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[markdown]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    }
}

LINT_STAGED_CONFIG = {
    "*.{js,jsx,ts,tsx}": [
        "eslint --fix",
        "prettier --write"
    ],
    "*.{json,md,yml,yaml,css,scss}": [
        "prettier --write"
    ]
}

BIOME_CONFIG = {
    "$schema": "https://biomejs.dev/schemas/1.4.1/schema.json",
    "organizeImports": {
        "enabled": True
    },
    "linter": {
        "enabled": True,
        "rules": {
            "recommended": True,
            "complexity": {
                "noForEach": "off"
            },
            "style": {
                "noNonNullAssertion": "off"
            }
        }
    },
    "formatter": {
        "enabled": True,
        "indentStyle": "space",
        "indentWidth": 2,
        "lineWidth": 100
    },
    "javascript": {
        "formatter": {
            "quoteStyle": "single",
            "trailingComma": "es5",
            "semicolons": "always"
        }
    }
}

PRE_COMMIT_HOOK = """#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
"""


# ============================================================================
# Helper Functions
# ============================================================================

def detect_package_manager(root: Path) -> str:
    """Detect which package manager is used in the project."""
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    elif (root / "yarn.lock").exists():
        return "yarn"
    elif (root / "bun.lockb").exists():
        return "bun"
    else:
        return "npm"


def detect_framework(root: Path) -> list:
    """Detect frameworks used in the project."""
    frameworks = []
    
    pkg_json = root / "package.json"
    if pkg_json.exists():
        try:
            pkg = json.loads(pkg_json.read_text())
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            
            if "next" in deps:
                frameworks.append("nextjs")
            if "react" in deps:
                frameworks.append("react")
            if "@nestjs/core" in deps:
                frameworks.append("nestjs")
            if "express" in deps:
                frameworks.append("express")
            if "vue" in deps:
                frameworks.append("vue")
        except:
            pass
    
    return frameworks


def run_command(cmd: list, cwd: Path, dry_run: bool = False) -> bool:
    """Run a shell command."""
    cmd_str = " ".join(cmd)
    if dry_run:
        print(f"  [DRY-RUN] Would run: {cmd_str}")
        return True
    
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ⚠️  Command failed: {cmd_str}")
            if result.stderr:
                print(f"     {result.stderr[:200]}")
            return False
        return True
    except Exception as e:
        print(f"  ❌ Error running command: {e}")
        return False


def write_json(path: Path, data: dict, dry_run: bool = False):
    """Write JSON to file."""
    if dry_run:
        print(f"  [DRY-RUN] Would write: {path}")
        return
    
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"  ✅ Created: {path.name}")


def write_text(path: Path, content: str, dry_run: bool = False):
    """Write text to file."""
    if dry_run:
        print(f"  [DRY-RUN] Would write: {path}")
        return
    
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  ✅ Created: {path.name}")


def update_package_json(root: Path, scripts: dict, lint_staged: dict, dry_run: bool = False):
    """Update package.json with scripts and lint-staged config."""
    pkg_path = root / "package.json"
    
    if not pkg_path.exists():
        print("  ⚠️  No package.json found, skipping script additions")
        return
    
    if dry_run:
        print(f"  [DRY-RUN] Would update: package.json")
        return
    
    try:
        pkg = json.loads(pkg_path.read_text())
        
        # Add scripts
        if "scripts" not in pkg:
            pkg["scripts"] = {}
        pkg["scripts"].update(scripts)
        
        # Add lint-staged
        pkg["lint-staged"] = lint_staged
        
        pkg_path.write_text(json.dumps(pkg, indent=2) + "\n")
        print("  ✅ Updated: package.json")
    except Exception as e:
        print(f"  ❌ Error updating package.json: {e}")


# ============================================================================
# Setup Functions
# ============================================================================

def setup_eslint_prettier(root: Path, typescript: bool, dry_run: bool):
    """Set up ESLint and Prettier."""
    print("\n📦 Installing ESLint + Prettier dependencies...")
    
    pm = detect_package_manager(root)
    install_cmd = {
        "npm": ["npm", "install", "-D"],
        "pnpm": ["pnpm", "add", "-D"],
        "yarn": ["yarn", "add", "-D"],
        "bun": ["bun", "add", "-D"]
    }[pm]
    
    # Base dependencies
    deps = [
        "eslint",
        "prettier",
        "eslint-config-prettier",
        "eslint-plugin-prettier"
    ]
    
    # TypeScript dependencies
    if typescript:
        deps.extend([
            "@typescript-eslint/parser",
            "@typescript-eslint/eslint-plugin"
        ])
    
    # Detect frameworks and add plugins
    frameworks = detect_framework(root)
    if "react" in frameworks or "nextjs" in frameworks:
        deps.extend(["eslint-plugin-react", "eslint-plugin-react-hooks"])
    if "nextjs" in frameworks:
        deps.append("@next/eslint-plugin-next")
    
    run_command(install_cmd + deps, root, dry_run)
    
    print("\n📝 Creating configuration files...")
    
    # ESLint config
    eslint_config = ESLINT_CONFIG_TS if typescript else ESLINT_CONFIG
    
    # Add React config if detected
    if "react" in frameworks or "nextjs" in frameworks:
        eslint_config["extends"].insert(1, "plugin:react/recommended")
        eslint_config["extends"].insert(2, "plugin:react-hooks/recommended")
        eslint_config["plugins"] = eslint_config.get("plugins", []) + ["react", "react-hooks"]
        eslint_config["settings"] = {"react": {"version": "detect"}}
        eslint_config["rules"]["react/react-in-jsx-scope"] = "off"
        eslint_config["rules"]["react/prop-types"] = "off"
    
    if "nextjs" in frameworks:
        eslint_config["extends"].insert(1, "next/core-web-vitals")
    
    write_json(root / ".eslintrc.json", eslint_config, dry_run)
    write_json(root / ".prettierrc", PRETTIER_CONFIG, dry_run)
    write_text(root / ".prettierignore", PRETTIER_IGNORE, dry_run)
    write_text(root / ".eslintignore", ESLINT_IGNORE, dry_run)
    
    # npm scripts
    ext = ".js,.jsx,.ts,.tsx" if typescript else ".js,.jsx"
    scripts = {
        "lint": f"eslint . --ext {ext}",
        "lint:fix": f"eslint . --ext {ext} --fix",
        "format": "prettier --write .",
        "format:check": "prettier --check ."
    }
    
    update_package_json(root, scripts, LINT_STAGED_CONFIG, dry_run)


def setup_biome(root: Path, dry_run: bool):
    """Set up Biome as alternative to ESLint + Prettier."""
    print("\n📦 Installing Biome...")
    
    pm = detect_package_manager(root)
    install_cmd = {
        "npm": ["npm", "install", "-D"],
        "pnpm": ["pnpm", "add", "-D"],
        "yarn": ["yarn", "add", "-D"],
        "bun": ["bun", "add", "-D"]
    }[pm]
    
    run_command(install_cmd + ["@biomejs/biome"], root, dry_run)
    
    print("\n📝 Creating configuration files...")
    
    write_json(root / "biome.json", BIOME_CONFIG, dry_run)
    
    scripts = {
        "lint": "biome lint .",
        "lint:fix": "biome lint --apply .",
        "format": "biome format --write .",
        "format:check": "biome format .",
        "check": "biome check .",
        "check:fix": "biome check --apply ."
    }
    
    lint_staged = {
        "*.{js,jsx,ts,tsx,json,css}": ["biome check --apply"]
    }
    
    update_package_json(root, scripts, lint_staged, dry_run)


def setup_husky(root: Path, dry_run: bool):
    """Set up Husky pre-commit hooks."""
    print("\n🪝 Setting up pre-commit hooks...")
    
    pm = detect_package_manager(root)
    install_cmd = {
        "npm": ["npm", "install", "-D"],
        "pnpm": ["pnpm", "add", "-D"],
        "yarn": ["yarn", "add", "-D"],
        "bun": ["bun", "add", "-D"]
    }[pm]
    
    run_command(install_cmd + ["husky", "lint-staged"], root, dry_run)
    
    # Initialize husky
    run_command(["npx", "husky", "install"], root, dry_run)
    
    # Create pre-commit hook
    husky_dir = root / ".husky"
    if not dry_run:
        husky_dir.mkdir(exist_ok=True)
    
    pre_commit_path = husky_dir / "pre-commit"
    write_text(pre_commit_path, PRE_COMMIT_HOOK, dry_run)
    
    if not dry_run:
        pre_commit_path.chmod(0o755)
    
    # Add prepare script to package.json
    pkg_path = root / "package.json"
    if pkg_path.exists() and not dry_run:
        pkg = json.loads(pkg_path.read_text())
        if "scripts" not in pkg:
            pkg["scripts"] = {}
        pkg["scripts"]["prepare"] = "husky install"
        pkg_path.write_text(json.dumps(pkg, indent=2) + "\n")


def setup_vscode(root: Path, biome: bool, dry_run: bool):
    """Set up VS Code / Cursor settings."""
    print("\n⚙️  Setting up editor configuration...")
    
    vscode_dir = root / ".vscode"
    settings_path = vscode_dir / "settings.json"
    
    settings = VSCODE_SETTINGS.copy()
    
    if biome:
        # Override for Biome
        settings["editor.defaultFormatter"] = "biomejs.biome"
        for key in list(settings.keys()):
            if key.startswith("["):
                settings[key]["editor.defaultFormatter"] = "biomejs.biome"
    
    # Merge with existing settings if present
    if settings_path.exists() and not dry_run:
        try:
            existing = json.loads(settings_path.read_text())
            existing.update(settings)
            settings = existing
        except:
            pass
    
    write_json(settings_path, settings, dry_run)


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Set up linting and formatting for JS/TS projects"
    )
    parser.add_argument("--root", required=True, help="Project root directory")
    parser.add_argument("--typescript", action="store_true", help="Enable TypeScript support")
    parser.add_argument("--biome", action="store_true", help="Use Biome instead of ESLint + Prettier")
    parser.add_argument("--no-hooks", action="store_true", help="Skip pre-commit hook setup")
    parser.add_argument("--monorepo", action="store_true", help="Configure for monorepo root")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    
    args = parser.parse_args()
    
    root = Path(args.root).resolve()
    
    if not root.exists():
        print(f"❌ Error: Directory does not exist: {root}")
        sys.exit(1)
    
    if not (root / "package.json").exists():
        print(f"❌ Error: No package.json found in {root}")
        print("   Run 'npm init' first to create a package.json")
        sys.exit(1)
    
    print(f"🚀 Setting up linting and formatting")
    print(f"   Project: {root}")
    print(f"   TypeScript: {'Yes' if args.typescript else 'No'}")
    print(f"   Tool: {'Biome' if args.biome else 'ESLint + Prettier'}")
    print(f"   Pre-commit hooks: {'No' if args.no_hooks else 'Yes'}")
    
    if args.dry_run:
        print("\n⚠️  DRY RUN MODE - No changes will be made\n")
    
    # Detect frameworks
    frameworks = detect_framework(root)
    if frameworks:
        print(f"   Detected: {', '.join(frameworks)}")
    
    # Run setup
    if args.biome:
        setup_biome(root, args.dry_run)
    else:
        setup_eslint_prettier(root, args.typescript, args.dry_run)
    
    if not args.no_hooks:
        setup_husky(root, args.dry_run)
    
    setup_vscode(root, args.biome, args.dry_run)
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("  1. Review the generated config files")
    print("  2. Run 'npm run lint' to check for issues")
    print("  3. Run 'npm run format' to format all files")
    if not args.no_hooks:
        print("  4. Make a commit to test the pre-commit hook")
    
    if not args.biome:
        print("\nRecommended VS Code extensions:")
        print("  - ESLint (dbaeumer.vscode-eslint)")
        print("  - Prettier (esbenp.prettier-vscode)")
    else:
        print("\nRecommended VS Code extension:")
        print("  - Biome (biomejs.biome)")


if __name__ == "__main__":
    main()
