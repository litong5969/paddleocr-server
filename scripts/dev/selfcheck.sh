#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

echo "[selfcheck] repo=$ROOT"

# 1) Team integrity check (structure + governance files)
"$ROOT/scripts/team-integrity-check/run_team_integrity_check.sh"

# 2) Basic service smoke: prefer existing Compose service on HOST_PORT, else advise
HOST_PORT="${HOST_PORT:-5215}"
echo "[selfcheck] smoke target: http://localhost:$HOST_PORT"
if curl -fsS "http://localhost:$HOST_PORT/healthz" >/dev/null 2>&1; then
  echo "[selfcheck] service detected on $HOST_PORT"
else
  echo "[selfcheck] no service on $HOST_PORT; please start with: docker compose --compatibility up -d --build" >&2
fi

# 3) Minimal API/GUI smoke when service is up (non-fatal if not running)
set +e
curl -fsS "http://localhost:$HOST_PORT/healthz" -o /dev/null && echo "[selfcheck] /healthz OK"
curl -fsS "http://localhost:$HOST_PORT/ui" | grep -q "PaddleOCR Server — Web UI" && echo "[selfcheck] /ui OK"
curl -fsS "http://localhost:$HOST_PORT/meta" -o /dev/null && echo "[selfcheck] /meta OK"
set -e

# 4) Unit tests inside container (mount repo; FakeOCR-based tests)
if command -v docker >/dev/null 2>&1; then
  echo "[selfcheck] running tests in container (mounted repo)..."
  docker compose run --rm -v "$ROOT":/app -w /app paddleocr-server bash -lc "scripts/dev/run_tests.sh"
else
  echo "[selfcheck] docker not found; skip containerized tests" >&2
fi

echo "[selfcheck] PASS"
