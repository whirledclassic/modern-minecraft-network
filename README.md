# Modern Minecraft Network

All-in-one **Java + Bedrock** network with a website, membership store, and admin console.

```
./scripts/install.sh
```

## Studio take

This is a starter network that can take real players. It is not a finished commercial product.

Read these before you advertise it:

- [Studio review](docs/STUDIO-REVIEW.md) — what is solid, what will break
- [Profit plan](docs/PROFIT.md) — ranks, pricing, EULA fence, 90-day model
- [Launch checklist](docs/LAUNCH.md) — first 30 days

## What boots together

| Piece | Address |
| --- | --- |
| Java | `:25565` |
| Bedrock | UDP `:19132` |
| Website + store | `:8080` |
| Admin console | `:8080/console` |

Players land in the lobby, run `/server survival`, and buy VIP / Elite / Champion on the site. Paid orders grant LuckPerms groups over RCON.

## Install

```bash
git clone https://github.com/whirledclassic/modern-minecraft-network.git
cd modern-minecraft-network
./scripts/install.sh
```

Windows: `\scripts\install.ps1` (Docker Desktop required).

First boot downloads Paper, Velocity, Geyser, Floodgate, and plugins.

Then:

1. Join `localhost:25565`
2. Open `http://localhost:8080`
3. Console: `http://localhost:8080/console`
4. `./scripts/health.sh`

## Memberships

| Rank | Price | Perks |
| --- | --- | --- |
| VIP | $4.99 / 30d | prefix, 3 homes |
| Elite | $9.99 / 30d | VIP + more homes |
| Champion | $24.99 lifetime | Elite + fly |

`DEMO_PAYMENTS=true` is for local tests only. Public hosts must set it `false` and confirm orders in the console. No card numbers are collected.

## Ops

```bash
docker compose logs -f
./scripts/health.sh
./scripts/backup.sh
docker compose down
```

## Docs

- [Store](docs/STORE.md)
- [Crossplay](docs/CROSSPLAY.md)
- [Maps](docs/MAPS.md)
- [Plugins](docs/PLUGINS.md)

## License

MIT. Minecraft is a trademark of Mojang/Microsoft.
