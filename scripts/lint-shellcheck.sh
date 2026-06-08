#!/bin/bash
#
# Wrapper script for shellcheck that handles optional installation
# Used by lint-staged for pre-commit hooks
#

set -euo pipefail

if [[ $# -eq 0 ]]; then
  exit 0
fi

if command -v shellcheck >/dev/null 2>&1; then
  shellcheck "$@"
else
  echo "shellcheck is not installed. Install with: brew install shellcheck (macOS) or apt-get install -y shellcheck (Linux)" >&2
  exit 1
fi
