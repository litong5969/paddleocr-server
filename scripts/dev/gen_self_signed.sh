#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-ops/certs}"
CN="${CN:-localhost}"
mkdir -p "$OUT_DIR"
CRT="$OUT_DIR/dev.crt"
KEY="$OUT_DIR/dev.key"

if command -v openssl >/dev/null 2>&1; then
  echo "[cert] generating self-signed cert for CN=$CN -> $CRT / $KEY"
  openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
    -subj "/C=CN/ST=NA/L=NA/O=Dev/OU=Dev/CN=$CN" \
    -keyout "$KEY" -out "$CRT" >/dev/null 2>&1
  echo "[cert] done"
else
  echo "openssl not found" >&2
  exit 1
fi

echo "Usage to enable HTTPS: set env SSL_CERTFILE=/app/certs/dev.crt SSL_KEYFILE=/app/certs/dev.key and mount files."

