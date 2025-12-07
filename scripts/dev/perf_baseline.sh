#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

URL="${URL:-http://localhost:${HOST_PORT:-5215}/ocr}"
IMG="${IMG:-$ROOT/test.jpg}"
REQS="${REQS:-16}"
CONC_LIST="${CONC_LIST:-1 4 8}"
OUT="${OUT:-$ROOT/docs/summary/bench-$(date +%F).md}"

echo "[perf] url=$URL img=$IMG reqs=$REQS conc=($CONC_LIST) out=$OUT"
mkdir -p "$(dirname "$OUT")"

run_python() {
  python3 - <<PY
import sys
print('ok')
PY
}

bench_cmd() {
  local c=$1
  python3 scripts/bench/bench_ocr.py --url "$URL" --image "$IMG" --concurrency "$c" --requests "$REQS"
}

if run_python >/dev/null 2>&1; then
  echo "[perf] using host python3"
  {
    echo "# OCR Bench — $(date +%F)"
    echo
    for c in $CONC_LIST; do
      bench_cmd "$c"
    done
  } | tee -a "$OUT"
elif command -v docker >/dev/null 2>&1; then
  echo "[perf] using docker python:3.11"
  CIMG="$IMG"
  if [[ "$CIMG" == "$ROOT"* ]]; then CIMG="/w${CIMG#$ROOT}"; fi
  URL_IN_CONTAINER="$URL"
  if [[ "$URL_IN_CONTAINER" == http://localhost:* || "$URL_IN_CONTAINER" == http://127.0.0.1:* ]]; then
    URL_IN_CONTAINER="http://paddleocr-server:5000/ocr"
  fi
  NET="${COMPOSE_PROJECT_NAME:-$(basename "$ROOT")}_default"
  for c in $CONC_LIST; do
    docker run --rm --network "$NET" -v "$ROOT":"/w" -w /w python:3.11 bash -lc "pip -q install httpx && python scripts/bench/bench_ocr.py --url '$URL_IN_CONTAINER' --image '$CIMG' --concurrency '$c' --requests '$REQS'" | tee -a "$OUT"
  done
else
  echo "[perf] no python3 or docker available; abort" >&2
  exit 2
fi

echo "[perf] results appended to $OUT"
