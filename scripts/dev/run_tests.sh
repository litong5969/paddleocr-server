#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
echo "[tests] Installing deps..." >&2
python3 -m pip install -q -r requirements.txt pytest
echo "[tests] Running pytest..." >&2
pytest -q
