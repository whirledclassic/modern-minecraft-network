#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="${ROOT}/backups"
mkdir -p "$OUT"
echo "Saving worlds..."
docker exec modern-mc-lobby rcon-cli save-all flush >/dev/null 2>&1 || true
docker exec modern-mc-survival rcon-cli save-all flush >/dev/null 2>&1 || true
sleep 2
echo "Copying Docker volumes to $OUT/worlds-$STAMP.tgz"
docker run --rm \
  -v modern-mc_lobby-data:/lobby:ro \
  -v modern-mc_survival-data:/survival:ro \
  -v "$OUT":/out \
  busybox:1.37 \
  tar czf "/out/worlds-$STAMP.tgz" /lobby /survival
echo "Done: $OUT/worlds-$STAMP.tgz"
