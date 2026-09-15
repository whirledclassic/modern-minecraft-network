#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== Modern Network installer =="

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required. Install Docker Desktop or docker.io first."
  exit 1
fi
if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 is required (docker compose)."
  exit 1
fi

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

chmod +x scripts/new-secret.sh scripts/backup.sh scripts/install.sh 2>/dev/null || true
./scripts/new-secret.sh

python3 - << 'PY' || true
import secrets, pathlib, re
p = pathlib.Path(".env")
t = p.read_text()
def fill(key, n=24):
    global t
    m = re.search(rf"^{key}=(.*)$", t, re.M)
    if not m:
        t += f"\n{key}={secrets.token_urlsafe(n)}\n"
        return
    val = m.group(1).strip()
    if val in ("", "change-me", "change-me-too", "change-me-admin", "change-me-to-a-long-random-string"):
        t = re.sub(rf"^{key}=.*$", f"{key}={secrets.token_urlsafe(n)}", t, flags=re.M)
fill("RCON_PASSWORD")
fill("ADMIN_PASSWORD")
fill("STORE_SECRET")
p.write_text(t)
print("Secrets checked.")
PY

echo
echo "Starting the full stack (proxy, lobby, survival, website, store, admin)..."
docker compose up -d --build

echo
echo "Done. First boot downloads Paper / Velocity / Geyser and can take several minutes."
echo
echo "  Java:          localhost:25565"
echo "  Bedrock:       localhost:19132"
echo "  Website/store: http://localhost:8080"
echo "  Admin console: http://localhost:8080/console"
echo
echo "Follow logs:  docker compose logs -f"
