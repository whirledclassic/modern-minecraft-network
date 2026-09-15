# Modern Minecraft Network

A ready-to-run **modern Minecraft network**:

- **Velocity** proxy (single public address)
- **Paper lobby** (hub / spawn / server selector)
- **Paper survival** (the actual game world)

Players connect once, land in the lobby, then transfer to survival without logging out.

This repo is a **template**, not a hosted server. You run it on your own machine, VPS, or game host with Docker.

## Architecture

```
Players
   |
   |  :25565  (and optional Bedrock :19132 later)
   v
Velocity proxy
   |-- lobby     Paper  adventure hub
   `-- survival  Paper  survival world
```

Recommended stack for 2026:

| Role | Software |
| --- | --- |
| Proxy | Velocity |
| Backends | Paper |
| Runtime | Docker Compose + [itzg/minecraft-server](https://github.com/itzg/docker-minecraft-server) |
| Auth | Mojang/Microsoft online-mode on the proxy, modern player-info forwarding |

## Requirements

- Docker + Docker Compose v2
- 6 GB+ RAM free (default: proxy 512 MB, lobby 2 GB, survival 4 GB)
- Open UDP/TCP **25565** to players
- Java is **not** required on the host if you use Docker

## Quick start

```bash
git clone https://github.com/whirledclassic/modern-minecraft-network.git
cd modern-minecraft-network

cp .env.example .env
# edit .env — change VELOCITY_SECRET and MEMORY if needed

# generate a unique forwarding secret (do this once)
./scripts/new-secret.sh

docker compose up -d
docker compose logs -f
```

Connect with the Minecraft Java client to:

```
localhost:25565
```

or your VPS public IP / domain on port 25565.

First boot downloads Paper, Velocity, and plugins. That can take a few minutes.

## What you get out of the box

### Lobby

- Adventure mode, no PvP, no Nether
- Peaceful / hub-style defaults
- LuckPerms, Vault, PlaceholderAPI, ViaVersion, TAB
- Drop extra lobby plugins into `plugins/lobby/`

### Survival

- Survival, normal difficulty, PvP on, Nether on
- EssentialsX, LuckPerms, Vault, WorldGuard, CoreProtect, GriefPrevention, PlaceholderAPI, ViaVersion, Spark
- Drop extra survival plugins into `plugins/survival/`

### Proxy

- Online-mode authentication
- Modern forwarding (backends cannot be joined directly if configured correctly)
- MOTD and try-list send new players to `lobby` first

## Common commands

```bash
# start / stop / restart the whole network
docker compose up -d
docker compose down
docker compose restart

# logs
docker compose logs -f proxy
docker compose logs -f lobby
docker compose logs -f survival

# attach to a backend console (type 'stop' only if you intend to stop that container)
docker attach modern-mc-lobby
docker attach modern-mc-survival
# detach without stopping: Ctrl+P then Ctrl+Q
```

Op yourself after first join (from the survival or lobby console):

```
op YourMinecraftName
```

Then in-game:

```
/lp user YourMinecraftName permission set * true
```

## Transferring between servers

From the lobby console or an in-game command plugin:

```
/server survival
/server lobby
```

Velocity provides `/server` once a player is connected through the proxy. Add a lobby compass / NPC / GUI later with DeluxeHub, CommandPanels, Citizens, etc. See [docs/PLUGINS.md](docs/PLUGINS.md).

## Important files

| Path | Purpose |
| --- | --- |
| `docker-compose.yml` | The whole network |
| `.env` | Memory, version, secret, MOTD |
| `proxy/velocity.toml` | Proxy routes and MOTD |
| `proxy/forwarding.secret` | Shared Velocity ↔ Paper secret |
| `config/paper-global.yml` | Enables Velocity forwarding on Paper |
| `plugins/lobby/` | Extra lobby plugin jars |
| `plugins/survival/` | Extra survival plugin jars |
| `plugins/proxy/` | Extra Velocity plugin jars |

Worlds and plugin data live in Docker volumes (`lobby-data`, `survival-data`, `proxy-data`) so they persist across restarts.

## Hardening checklist

1. Replace `VELOCITY_SECRET` / `proxy/forwarding.secret` with a long random string.
2. Do **not** publish lobby/survival ports to the internet. Only `25565` on the proxy should be public.
3. Keep `online-mode = true` on Velocity.
4. Keep `online-mode=false` on Paper backends — the proxy already authenticated the player.
5. Add a whitelist or auth plugin if this is a private friends server.
6. Take backups of the Docker volumes (especially `survival-data`).

## Without Docker

See [docs/BARE-METAL.md](docs/BARE-METAL.md) if you want to run the jars directly on a VPS.

## Next steps

- Build a real lobby map and set the world spawn
- Add DeluxeHub / CommandPanels for a server selector item
- Connect LuckPerms across servers with MySQL
- Add Geyser + Floodgate for Bedrock cross-play
- Point a domain at your host (`play.example.com`)

## License

MIT. Minecraft is a trademark of Mojang/Microsoft. Paper and Velocity are from PaperMC. This repo only ships configuration and automation — you download official server software at runtime.
