#!/usr/bin/env bash
set -euo pipefail

if command -v pytest >/dev/null 2>&1; then
  echo "[tests] running pytest on host..."
  pytest -q
  exit $?
fi

if command -v docker >/dev/null 2>&1; then
  echo "[tests] running pytest inside container..."
  docker compose run --rm paddleocr-server bash -lc 'pytest -q'
  exit $?
fi

echo "[tests] pytest not found and docker not available. Skipping." >&2
exit 0

