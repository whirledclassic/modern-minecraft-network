#!/usr/bin/env bash
set -euo pipefail
if ! command -v ufw >/dev/null 2>&1; then
  echo "ufw is not installed. Open 25565/tcp, 19132/udp, 8080/tcp in your cloud panel instead."
  exit 1
fi
sudo ufw allow 25565/tcp comment 'minecraft-java'
sudo ufw allow 19132/udp comment 'minecraft-bedrock'
sudo ufw allow 8080/tcp comment 'modern-mc-site'
echo "Rules added. Enable with: sudo ufw enable"
