#!/usr/bin/env bash
set -euo pipefail

HOST=${HOST:-localhost}
PORT=${PORT:-5215}
BASE="http://${HOST}:${PORT}"
IMG=${IMG:-test.jpg}

echo "[test] base=$BASE"
code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/healthz" || true)
echo "[test] /healthz -> $code"; test "$code" = "200"

if [ ! -f "$IMG" ]; then
  echo "[test] image not found: $IMG" >&2
  exit 1
fi

echo "[test] POST /ocr with $IMG"
resp=$(curl -s -w "\n%{http_code}" -F "file=@$IMG" "$BASE/ocr")
body=$(echo "$resp" | head -n -1)
status=$(echo "$resp" | tail -n 1)
echo "[test] status=$status"
echo "$body" | jq '.' >/dev/null 2>&1 || echo "$body" | head -n 20
test "$status" = "200"

echo "[test] ok"
