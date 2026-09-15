#!/usr/bin/env bash
set -euo pipefail
echo "== Modern Network health =="
docker compose ps || { echo "compose not running in this folder"; exit 1; }
echo
for c in modern-mc-db modern-mc-proxy modern-mc-lobby modern-mc-survival modern-mc-platform; do
  if docker inspect "$c" >/dev/null 2>&1; then
    state=$(docker inspect -f '{{.State.Status}}' "$c")
    echo "$c  $state"
  else
    echo "$c  missing"
  fi
done
echo
echo "RCON list (survival):"
docker exec modern-mc-survival rcon-cli list || echo "survival rcon not ready"
echo "RCON list (lobby):"
docker exec modern-mc-lobby rcon-cli list || echo "lobby rcon not ready"
echo "LuckPerms storage:"
docker exec modern-mc-survival rcon-cli lp info || echo "lp not ready"
echo
curl -fsS "http://127.0.0.1:${PLATFORM_PORT:-8080}/healthz" && echo || echo "platform /healthz failed"
