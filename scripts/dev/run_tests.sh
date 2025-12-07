#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "[tests] Installing deps..." >&2
python3 -m pip install --upgrade pip >/dev/null
python3 -m pip install -q -r requirements.txt pytest "httpx==0.27.*"
echo "[tests] Running pytest..." >&2
PYTHONPATH=. pytest -q
