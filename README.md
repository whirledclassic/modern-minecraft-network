# Modern Minecraft Network

Ready-to-run **Java + Bedrock** network:

- Velocity proxy
- Paper lobby with a generated modern hub + compass selector
- Paper survival with a spawn plaza
- Geyser + Floodgate crossplay
- Web admin panel on `:8080`

This is a template. You run it on your machine or VPS with Docker.

## Architecture

```
Java :25565 TCP ──┐
                  ├─▶ Velocity + Geyser + Floodgate
Bedrock :19132 UDP┘           │
                              ├── lobby     (adventure hub)
                              └── survival  (world + claims)
                                   │
                            admin panel :8080  (RCON)
```

## Quick start

```bash
git clone https://github.com/whirledclassic/modern-minecraft-network.git
cd modern-minecraft-network

cp .env.example .env
chmod +x scripts/new-secret.sh scripts/backup.sh
./scripts/new-secret.sh
# edit .env — set ADMIN_PASSWORD and RCON_PASSWORD

docker compose up -d --build
docker compose logs -f
```

First boot downloads Paper, Velocity, Geyser, Floodgate, and plugins. Give it a few minutes.

### Join

| Client | Address |
| --- | --- |
| Java | `localhost:25565` or `your.ip:25565` |
| Bedrock | same IP, port `19132` |
| Admin panel | `http://localhost:8080` |

In the lobby, right-click the **compass** → Survival.

Then from a server console:

```
op YourMinecraftName
```

```
/lp user YourMinecraftName permission set * true
```

## What is included

### Lobby
- Generated modern floating hub
- Compass server selector (`/servers`)
- Adventure, flight, no PvP, no weather
- LuckPerms, Vault, PlaceholderAPI, ViaVersion, TAB

### Survival
- Normal overworld + spawn plaza
- EssentialsX, WorldGuard, CoreProtect, GriefPrevention, Spark
- `/hub` returns to the lobby

### Proxy
- Online-mode Java auth
- Modern forwarding
- Geyser + Floodgate for Bedrock

### Admin panel
- Status, player list, live commands
- See [docs/ADMIN.md](docs/ADMIN.md)

## Everyday commands

```bash
docker compose up -d --build
docker compose down
docker compose logs -f proxy
docker compose logs -f lobby
docker compose logs -f survival
docker compose logs -f admin

./scripts/backup.sh
```

## Important files

| Path | Purpose |
| --- | --- |
| `docker-compose.yml` | Whole network |
| `.env` | Secrets, memory, seed, MOTD |
| `proxy/velocity.toml` | Routes |
| `config/geyser.yml` | Bedrock listener |
| `config/floodgate.yml` | Bedrock auth |
| `plugin/` | Custom hub plugin source + jar |
| `admin/` | Web admin panel |
| `plugins/*/` | Extra jars you drop in |

Worlds persist in Docker volumes `lobby-data` and `survival-data`.

## Docs

- [Crossplay](docs/CROSSPLAY.md)
- [Admin panel](docs/ADMIN.md)
- [Custom maps](docs/MAPS.md)
- [Plugins](docs/PLUGINS.md)
- [Bare metal](docs/BARE-METAL.md)

## Hardening

1. Run `./scripts/new-secret.sh` and change `ADMIN_PASSWORD` / `RCON_PASSWORD`.
2. Publish only `25565/tcp`, `19132/udp`, and maybe `8080` (prefer a tunnel for the panel).
3. Never publish backend or RCON ports.
4. Backup `survival-data` if people start building.

## License

MIT. Minecraft is a trademark of Mojang/Microsoft. Paper, Velocity, Geyser, and Floodgate belong to their authors. This repo ships configuration, a small hub plugin, and an admin UI. Server software is downloaded at runtime.
