# Bare-metal setup (no Docker)

Use this if you cannot run Docker. You still need **Java 21+** (Java 25 for current Paper 26.x lines — check [Paper docs](https://docs.papermc.io/paper/getting-started/) for the version you download).

## Folders

```
network/
  proxy/          # Velocity jar + velocity.toml + forwarding.secret
  lobby/          # Paper jar + world + plugins
  survival/       # Paper jar + world + plugins
```

## 1. Download software

- Velocity: https://papermc.io/downloads/velocity
- Paper: https://papermc.io/downloads/paper

Place `velocity.jar` in `proxy/` and `paper.jar` in both `lobby/` and `survival/`.

## 2. Proxy config

Copy `proxy/velocity.toml` from this repo into `network/proxy/`.

Change backend addresses to localhost ports:

```toml
[servers]
lobby = "127.0.0.1:25566"
survival = "127.0.0.1:25567"
```

Keep `bind = "0.0.0.0:25565"`.

Create `forwarding.secret` with one long random line. Use the same value in both Paper servers.

## 3. Paper backends

In each backend `server.properties`:

```
online-mode=false
server-ip=127.0.0.1
```

Use different ports:

- lobby `server-port=25566`
- survival `server-port=25567`

Do **not** port-forward 25566/25567.

In `config/paper-global.yml` on both backends:

```yaml
proxies:
  velocity:
    enabled: true
    online-mode: true
    secret: "THE_SAME_SECRET_AS_forwarding.secret"
```

Lobby extras in `server.properties`:

```
gamemode=adventure
difficulty=peaceful
pvp=false
allow-nether=false
```

Survival extras:

```
gamemode=survival
difficulty=normal
pvp=true
allow-nether=true
```

## 4. Start order

Use three terminals or `tmux`:

```bash
# lobby
cd lobby && java -Xms2G -Xmx2G -jar paper.jar --nogui

# survival
cd survival && java -Xms4G -Xmx4G -jar paper.jar --nogui

# proxy last
cd proxy && java -Xms512M -Xmx512M -jar velocity.jar
```

Players connect to `yourip:25565`.
