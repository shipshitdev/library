#!/bin/bash
set -euo pipefail

# ============================================================================
# setup-dev-loop.sh — provision the AI dev loop on a GitHub repo
#
# One-shot, idempotent setup for label-driven autonomous execution. Two engine
# lanes share one label contract: the Claude lane (ready-for-agent) and the
# Codex/GPT lane (ready-for-codex).
#   1. Creates the dispatch label vocabulary (status:*, priority:*, claimed,
#      ready-for-agent, ready-for-codex, rejection:N, feature, wontfix).
#   2. Installs the Phase-2 push workflows (.github/workflows/agent-dispatch.yml
#      for Claude, codex-dispatch.yml for Codex).
#   3. Arms the Phase-2 auth secrets — CLAUDE_CODE_OAUTH_TOKEN (subscription
#      OAuth, never an API key) and OPENAI_API_KEY (Codex lane).
#   4. Prints the `gh variable set` commands for model selection (AGENT_MODEL,
#      CODEX_MODEL, CODEX_EFFORT) — non-sensitive, so repo VARIABLES not secrets.
#   5. Points you at /setup-agent-routing for the per-repo routing block.
#
# Operates on the current repo by default (resolved via `gh`); override with
# --repo owner/name. Safe to re-run — labels use --force, workflows are copied
# in place, secrets are left alone if already set.
#
# Usage:
#   setup-dev-loop.sh                       # set up the current repo
#   setup-dev-loop.sh --repo owner/name     # target a specific repo
#   setup-dev-loop.sh --dry-run             # preview without changing anything
#   setup-dev-loop.sh --skip-secrets        # skip the auth-secret steps
#   setup-dev-loop.sh --help
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKFLOW_DIR="${SCRIPT_DIR}/../.github/workflows"

# Phase-2 push workflows installed into the target repo (one per engine lane).
WORKFLOWS=(
  "agent-dispatch.yml"
  "codex-dispatch.yml"
)

REPO=""
REPO_FLAG=()
DO_LABELS=true
DO_WORKFLOW=true
DO_SECRETS=true
DRY_RUN=false
VERBOSE=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()    { echo -e "${GREEN}[✓]${NC} $*"; }
warn()   { echo -e "${YELLOW}[!]${NC} $*"; }
err()    { echo -e "${RED}[✗]${NC} $*" >&2; }
info()   { echo -e "${BLUE}[i]${NC} $*"; }
dry()    { echo -e "${YELLOW}[dry-run]${NC} $*"; }
vlog()   { $VERBOSE && echo -e "${BLUE}[v]${NC} $*" || true; }

# ============================================================================
# Dispatch label vocabulary — name|color|description.
# Mirrors skills/setup-agent-routing/references/triage-labels.md.
# ============================================================================

LABELS=(
  "status:todo|1d76db|To Do column — backlog-ready, not yet opted into agent execution"
  "status:testing|fbca04|Testing column — implemented, awaiting human QA"
  "claimed|5319e7|An agent currently holds this issue (30-min claim lock)"
  "priority:high|b60205|Queue ordering — picked first"
  "priority:medium|d93f0b|Queue ordering — picked after high"
  "priority:low|0e8a16|Queue ordering — picked last"
  "rejection:1|e99695|QA rejection count — 1st kickback from Testing"
  "rejection:2|e99695|QA rejection count — 2nd kickback from Testing"
  "rejection:3|e99695|QA rejection count — 3rd kickback from Testing"
  "ready-for-agent|006b75|Dispatch gate (human opt-in) — Claude lane runs only on issues carrying this"
  "ready-for-codex|10a37f|Dispatch gate (human opt-in) — Codex/GPT lane runs only on issues carrying this"
  "feature|a2eeef|Applied by feature-intake to PRD epics and their sub-issues"
  "wontfix|ffffff|Closed; will not be actioned"
)

# ============================================================================
# Preflight
# ============================================================================

require_gh() {
  command -v gh >/dev/null 2>&1 || {
    err "gh CLI not found — install it: https://cli.github.com"
    exit 1
  }
  gh auth status >/dev/null 2>&1 || {
    err "gh is not authenticated — run: gh auth login"
    exit 1
  }
}

resolve_repo() {
  if [[ -z "$REPO" ]]; then
    REPO="$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null || true)"
  fi
  if [[ -z "$REPO" ]]; then
    err "Could not detect a GitHub repo. Run inside a repo with a GitHub remote, or pass --repo owner/name"
    exit 1
  fi
  REPO_FLAG=(--repo "$REPO")
  vlog "repo resolved: ${REPO}"
}

# ============================================================================
# Step 1 — labels
# ============================================================================

create_labels() {
  info "Creating/updating ${#LABELS[@]} dispatch labels on ${REPO}"
  local entry name color desc
  for entry in "${LABELS[@]}"; do
    IFS='|' read -r name color desc <<<"$entry"
    if $DRY_RUN; then
      dry "gh label create '${name}' --color ${color} --force"
      continue
    fi
    if gh label create "$name" --color "$color" --description "$desc" --force "${REPO_FLAG[@]}" >/dev/null 2>&1; then
      log "label: ${name}"
    else
      err "failed to create label: ${name}"
    fi
  done
}

# ============================================================================
# Step 2 — push workflow
# ============================================================================

install_workflows() {
  local repo_root
  repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
  if [[ -z "$repo_root" ]]; then
    warn "not inside a git working tree — skipping workflow copy"
    info "add these to .github/workflows/ in the target repo manually:"
    local wf
    for wf in "${WORKFLOWS[@]}"; do info "  ${WORKFLOW_DIR}/${wf}"; done
    return
  fi
  mkdir -p "${repo_root}/.github/workflows"
  local wf src dest
  for wf in "${WORKFLOWS[@]}"; do
    src="${WORKFLOW_DIR}/${wf}"
    dest="${repo_root}/.github/workflows/${wf}"
    if [[ ! -f "$src" ]]; then
      err "workflow source missing: ${src}"
      continue
    fi
    if [[ "$dest" -ef "$src" ]]; then
      info "${wf} already lives in this repo — nothing to copy"
      continue
    fi
    if $DRY_RUN; then
      dry "cp ${src} ${dest}"
      continue
    fi
    [[ -f "$dest" ]] && warn "${wf} exists — overwriting with the bundled version"
    cp "$src" "$dest"
    log "workflow installed: .github/workflows/${wf}"
  done
}

# ============================================================================
# Step 3 — auth secrets (Phase-2 auth, one per engine lane)
# ============================================================================

# setup_one_secret <NAME> <hint>
# Idempotent: leaves an already-set secret alone; otherwise prompts (interactive
# only) to set it via `gh secret set`, which reads the value with input hidden.
setup_one_secret() {
  local name="$1" hint="$2" existing reply
  existing="$(gh secret list "${REPO_FLAG[@]}" --json name --jq '.[].name' 2>/dev/null | grep -Fx "$name" || true)"
  if [[ -n "$existing" ]]; then
    log "secret ${name} already set"
    return
  fi
  warn "secret ${name} is not set on ${REPO}"
  info "${hint}"
  if $DRY_RUN; then
    dry "gh secret set ${name} ${REPO_FLAG[*]}"
    return
  fi
  if [[ ! -t 0 ]]; then
    warn "non-interactive shell — set it later:  gh secret set ${name} ${REPO_FLAG[*]}"
    return
  fi
  printf '%b' "${BLUE}[i]${NC} Set ${name} now? gh will prompt for the value (input hidden). [y/N] "
  read -r reply
  if [[ "$reply" =~ ^[Yy]$ ]]; then
    gh secret set "$name" "${REPO_FLAG[@]}"
    log "secret ${name} set"
  else
    info "skipped — set it later:  gh secret set ${name}"
  fi
}

setup_secrets() {
  # Claude lane (ready-for-agent). Subscription OAuth only — never an API key.
  setup_one_secret "CLAUDE_CODE_OAUTH_TOKEN" \
    "Claude lane — generate with:  claude setup-token   (uses your Claude subscription, never an API key)"
  # Codex/GPT lane (ready-for-codex). Skip if you only run the Claude lane.
  setup_one_secret "OPENAI_API_KEY" \
    "Codex lane — an OpenAI API key from https://platform.openai.com/api-keys (skip if you only use the Claude lane)"
}

# ============================================================================
# Step 4 — routing block (delegated to the skill)
# ============================================================================

# ============================================================================
# Step 4 — model selection (repo VARIABLES, not secrets)
# ============================================================================

# Model ids and reasoning effort are non-sensitive, so they belong in repo
# variables — change the engine without touching a workflow file. All optional:
# the workflows fall back to Sonnet (Claude) / the provider default (Codex).
print_variables_step() {
  info "Optional — pick which model each lane runs (repo VARIABLES, not secrets):"
  echo "      # Claude lane (defaults to claude-sonnet-4-6 if unset):"
  echo "      gh variable set AGENT_MODEL  --body claude-opus-4-8 ${REPO_FLAG[*]}"
  echo "      # Codex lane (leave unset for Codex defaults):"
  echo "      gh variable set CODEX_MODEL  --body gpt-5.5         ${REPO_FLAG[*]}"
  echo "      gh variable set CODEX_EFFORT --body xhigh           ${REPO_FLAG[*]}"
}

print_routing_step() {
  info "Final step — write this repo's routing block so the loop skills know your tracker + labels:"
  echo "      In Claude Code, run:  /setup-agent-routing"
  echo "      (writes the '## Agent skills' block + docs/agents/*.md, with your confirmation)"
}

print_summary() {
  echo ""
  log "Dev-loop setup complete on ${REPO}"
  $DO_LABELS   && echo "  • Labels:    dispatch vocabulary created/updated (incl. ready-for-codex)"
  $DO_WORKFLOW && echo "  • Workflows: agent-dispatch.yml (ready-for-agent) + codex-dispatch.yml (ready-for-codex)"
  $DO_SECRETS  && echo "  • Secrets:   CLAUDE_CODE_OAUTH_TOKEN (Claude) + OPENAI_API_KEY (Codex)"
  echo "  • Variables: AGENT_MODEL / CODEX_MODEL / CODEX_EFFORT (set with gh variable set)"
  echo "  • Routing:   run /setup-agent-routing in Claude Code"
  echo ""
  echo "  How to drive it:"
  echo "    1. Move an issue to To Do (status:todo)."
  echo "    2. Apply ready-for-agent (Claude lane) OR ready-for-codex (Codex lane)."
  echo "    3. Phase 1 (local):  run  /loop   to claim + work one issue (Claude)."
  echo "    4. Phase 2 (push):   the gate label alone fires its dispatch workflow headlessly."
  echo ""
  echo "  Full loop reference: .agents/SYSTEM/AI-DEV-LOOP.md"
}

usage() {
  cat <<'USAGE'
setup-dev-loop.sh — provision the AI dev loop on a GitHub repo

Usage:
  setup-dev-loop.sh                     Set up the current repo
  setup-dev-loop.sh --repo owner/name   Target a specific repo
  setup-dev-loop.sh --dry-run           Preview without changing anything

Options:
  --repo <owner/name>   Target repo (default: detected from the current remote)
  --skip-labels         Do not create/update labels
  --skip-workflow       Do not install the dispatch workflows
  --skip-secrets        Do not touch the auth secrets
  --dry-run             Preview changes without executing
  --verbose             Show detailed output
  --help                Show this help

What it does:
  1. Creates the dispatch labels (status:*, priority:*, claimed,
     ready-for-agent, ready-for-codex, rejection:N, feature, wontfix).
  2. Installs the Phase-2 push workflows: agent-dispatch.yml (Claude lane,
     ready-for-agent) and codex-dispatch.yml (Codex lane, ready-for-codex).
  3. Arms the auth secrets: CLAUDE_CODE_OAUTH_TOKEN (subscription OAuth) and
     OPENAI_API_KEY (Codex lane).
  4. Prints the gh variable set commands for model selection (AGENT_MODEL,
     CODEX_MODEL, CODEX_EFFORT) — non-sensitive, so repo variables not secrets.
  5. Points you at /setup-agent-routing for the per-repo routing block.

Examples:
  setup-dev-loop.sh
  setup-dev-loop.sh --repo shipshitdev/skills
  setup-dev-loop.sh --dry-run --skip-secrets
USAGE
}

# ============================================================================
# Main
# ============================================================================

main() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --repo)             REPO="$2"; shift 2 ;;
      --skip-labels)      DO_LABELS=false; shift ;;
      --skip-workflow)    DO_WORKFLOW=false; shift ;;
      --skip-workflows)   DO_WORKFLOW=false; shift ;;
      --skip-secrets)     DO_SECRETS=false; shift ;;
      --skip-secret)      DO_SECRETS=false; shift ;;
      --dry-run)          DRY_RUN=true; shift ;;
      --verbose)          VERBOSE=true; shift ;;
      --help|-h)          usage; exit 0 ;;
      *)                  err "Unknown option: $1"; usage; exit 1 ;;
    esac
  done

  require_gh
  resolve_repo

  $DRY_RUN && warn "DRY RUN — no changes will be made"
  info "Setting up the AI dev loop on ${REPO}"

  $DO_LABELS   && create_labels
  $DO_WORKFLOW && install_workflows
  $DO_SECRETS  && setup_secrets
  print_variables_step
  print_routing_step
  print_summary
}

main "$@"
