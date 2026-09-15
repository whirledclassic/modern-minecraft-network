#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SECRET="$(openssl rand -hex 32 2>/dev/null || python3 -c 'import secrets; print(secrets.token_hex(32))')"

printf '%s\n' "$SECRET" > "$ROOT/proxy/forwarding.secret"

if [[ -f "$ROOT/.env" ]]; then
  if grep -q '^VELOCITY_SECRET=' "$ROOT/.env"; then
    tmp="$(mktemp)"
    sed "s/^VELOCITY_SECRET=.*/VELOCITY_SECRET=${SECRET}/" "$ROOT/.env" > "$tmp"
    mv "$tmp" "$ROOT/.env"
  else
    printf '\nVELOCITY_SECRET=%s\n' "$SECRET" >> "$ROOT/.env"
  fi
else
  cp "$ROOT/.env.example" "$ROOT/.env"
  tmp="$(mktemp)"
  sed "s/^VELOCITY_SECRET=.*/VELOCITY_SECRET=${SECRET}/" "$ROOT/.env" > "$tmp"
  mv "$tmp" "$ROOT/.env"
fi

echo "Wrote new Velocity forwarding secret to proxy/forwarding.secret and .env"
echo "Restart the stack: docker compose up -d"
