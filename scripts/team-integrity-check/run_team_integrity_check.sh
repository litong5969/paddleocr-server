#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PASS=true

log() { echo "[team-integrity-check] $*"; }
fail() { echo "[team-integrity-check][FAIL] $*"; PASS=false; }

log "root: $ROOT"

# 1) Agents + Routing + Policies
[[ -f "$ROOT/AGENTS.md" ]] || fail "Missing AGENTS.md"
[[ -f "$ROOT/docs/TEAM_OVERVIEW.md" ]] || fail "Missing TEAM_OVERVIEW.md"
[[ -f "$ROOT/docs/TASK_AGENT_MATRIX.md" ]] || fail "Missing TASK_AGENT_MATRIX.md"
[[ -f "$ROOT/runtime/mcp/registry.yml" ]] || fail "Missing MCP registry"
[[ -f "$ROOT/runtime/mcp/policies.yml" ]] || fail "Missing MCP policies"

# 2) MCP registry/tools loadable (basic yaml existence)
[[ -d "$ROOT/runtime/mcp/tools" ]] || fail "Missing MCP tools dir"

# 3) context7 provider connectivity (placeholder)
[[ -f "$ROOT/runtime/context7/providers.json" ]] || fail "Missing context7 providers.json"

# 4) summary-validator placeholder check
[[ -f "$ROOT/runtime/codex/config/codex.config.json" ]] || fail "Missing Codex config"

# 5) CR-Audit structure
[[ -d "$ROOT/docs/audit" ]] || fail "Missing audit docs"

# 6) PM_BOOTSTRAP / lifecycle
[[ -f "$ROOT/docs/governance/PM_BOOTSTRAP.md" ]] || fail "Missing PM_BOOTSTRAP"
[[ -d "$ROOT/docs/lifecycle" ]] || fail "Missing lifecycle docs"

# 7) Logs bootstrap (directories may be created by caller)
mkdir -p "$ROOT/../docs/summary/pm_sessions" >/dev/null 2>&1 || true
mkdir -p "$ROOT/../ops/logs/pm" >/dev/null 2>&1 || true

if $PASS; then
  log "Integrity: PASS"
  exit 0
else
  log "Integrity: FAIL"
  exit 1
fi
