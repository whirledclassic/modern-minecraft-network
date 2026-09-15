# Start here if you have never hosted a server

Read this top to bottom. Do not skip.

## What you are building

One computer (or a rented VPS) will run a front door (Velocity), a lobby, a survival world with money and claims, and a website on port 8080.

Java = port 25565 TCP. Bedrock = port 19132 UDP.

## Install Docker first

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) on Windows or Mac.
   Ubuntu: `sudo apt install docker.io docker-compose-v2`
2. Leave Docker running.
3. You need about **8 GB of free RAM**.

If Docker is not running, nothing else works.

## One-time setup

Terminal in the folder that contains `docker-compose.yml`:

```bash
./scripts/install.sh
./scripts/health.sh
```

Windows if bash is missing: `.\scripts\install.ps1`

First start can take 5–15 minutes.

## Join

Java: Multiplayer → Direct → `localhost` (or the VPS IP).
Bedrock: Add Server → same IP → port `19132`.
Then `/server survival`.

## Make yourself admin

In `.env`:

```
OPS=YourExactJavaName
```

Then `docker compose up -d`, rejoin, and:

```
/lp user YourExactJavaName permission set * true
```

Website console: `http://localhost:8080/console` using `ADMIN_USER` / `ADMIN_PASSWORD` from `.env`.

## Money check

In survival: `/bal` (starts at $500) and `/kit starter`.

## Ports friends need

See [FIREWALL.md](FIREWALL.md). Never open 25575 or 3306.

## If something is wrong

[TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Daily buttons

| Want | Type |
| --- | --- |
| Is it up? | `./scripts/health.sh` |
| Logs | `docker compose logs -f` |
| Stop | `docker compose down` |
| Start | `docker compose up -d` |
| Backup | `./scripts/backup.sh` |

## Next

- [Admin commands](ADMIN-COMMANDS.md)
- [Economy](ECONOMY.md)
- [Launch checklist](LAUNCH.md)
