#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
URL="${1:-http://localhost:5213/}"
OUT="${2:-$ROOT/docs/summary/ui-screenshot.png}"

echo "[capture] url=$URL -> $OUT" >&2
if command -v google-chrome >/dev/null 2>&1; then
  google-chrome --headless=new --disable-gpu --virtual-time-budget=5000 \
    --window-size=1280,800 --screenshot="$OUT" "$URL"
elif command -v chromium >/dev/null 2>&1; then
  chromium --headless=new --disable-gpu --virtual-time-budget=5000 \
    --window-size=1280,800 --screenshot="$OUT" "$URL"
else
  echo "[capture] Chrome/Chromium 未找到，请手工截图或在本机安装后运行本脚本" >&2
  exit 2
fi
echo "[capture] done: $OUT" >&2
