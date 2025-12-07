#!/usr/bin/env bash
set -euo pipefail

URL="${URL:-http://localhost:5215/ocr}"
IMG="${IMG:-test.jpg}"
REQS=${REQS:-32}
CONC_LIST=( ${CONC_LIST:-1 4 8} )
OUTDIR="docs/summary"
mkdir -p "$OUTDIR"
STAMP=$(date +%F)
OUT="$OUTDIR/bench-$STAMP.md"

echo "# Bench $STAMP" > "$OUT"
echo "URL=$URL IMG=$IMG REQS=$REQS CONC_LIST=${CONC_LIST[*]}" >> "$OUT"

if [ ! -f "$IMG" ]; then
  echo "[perf] image not found: $IMG" >&2
  exit 1
fi

post_once() {
  local id="$1"
  local start end ms code
  start=$(date +%s%3N)
  code=$(curl -s -o /dev/null -w "%{http_code}" -F "file=@$IMG" "$URL" || echo 000)
  end=$(date +%s%3N)
  ms=$(( end - start ))
  echo "$ms $code"
}

run_case() {
  local conc=$1
  echo "\n## Concurrency $conc" | tee -a "$OUT"
  echo "```" >> "$OUT"
  seq 1 "$REQS" | xargs -n1 -P "$conc" -I{} bash -c 'post_once {}' post_once | tee /tmp/bench_raw.txt
  echo "```" >> "$OUT"
  awk '{print $1}' /tmp/bench_raw.txt | sort -n > /tmp/bench_ms.txt
  local count=$(wc -l < /tmp/bench_ms.txt)
  local p50_idx=$(( (count+1)*50/100 ))
  local p95_idx=$(( (count+1)*95/100 ))
  local p99_idx=$(( (count+1)*99/100 ))
  local p50=$(sed -n "${p50_idx}p" /tmp/bench_ms.txt)
  local p95=$(sed -n "${p95_idx}p" /tmp/bench_ms.txt)
  local p99=$(sed -n "${p99_idx}p" /tmp/bench_ms.txt)
  local avg=$(awk '{s+=$1} END{if(NR>0) printf "%.2f", s/NR; else print 0}' /tmp/bench_ms.txt)
  local ok=$(awk '$2==200{c++} END{print c+0}' /tmp/bench_raw.txt)
  local err=$(awk '$2!=200{c++} END{print c+0}' /tmp/bench_raw.txt)
  echo "p50=${p50}ms p95=${p95}ms p99=${p99}ms avg=${avg}ms ok=${ok} err=${err}" | tee -a "$OUT"
}

export -f post_once
for c in "${CONC_LIST[@]}"; do
  run_case "$c"
done

echo "[perf] summary written to $OUT"

