# Modern Minecraft Network

All-in-one **Java + Bedrock** network with a website, membership store, shared ranks, and admin console.

```
./scripts/install.sh
```

## Studio take

Starter network that can take real players. Not a finished commercial product.

- [Studio review](docs/STUDIO-REVIEW.md)
- [Profit plan](docs/PROFIT.md)
- [Launch checklist](docs/LAUNCH.md)
- [Shared LuckPerms](docs/DATABASE.md)

## What boots together

| Piece | Address |
| --- | --- |
| Java | `:25565` |
| Bedrock | UDP `:19132` |
| Website + store | `:8080` |
| Admin console | `:8080/console` |
| MariaDB | internal only |

Players land in the lobby plaza, run `/server survival`, and stand on a spawn pad at `0,81,0`. Shop ranks write to one LuckPerms database, so VIP is visible on both servers.

## Install

```bash
git clone https://github.com/whirledclassic/modern-minecraft-network.git
cd modern-minecraft-network
./scripts/install.sh
./scripts/health.sh
```

Windows: `scripts/install.ps1`.

1. Join `localhost:25565`
2. Site `http://localhost:8080`
3. Console `http://localhost:8080/console`

## Memberships

| Rank | Price | Perks |
| --- | --- | --- |
| VIP | $4.99 / 30d | `[VIP]` prefix, 3 homes |
| Elite | $9.99 / 30d | VIP + 6 homes |
| Champion | $24.99 lifetime | Elite + fly |

`DEMO_PAYMENTS=true` is local only. Public hosts set `false` and confirm orders in the console.

## Ops

```bash
docker compose logs -f
./scripts/health.sh
./scripts/backup.sh
```

## Docs

- [Store](docs/STORE.md) · [Maps](docs/MAPS.md) · [Crossplay](docs/CROSSPLAY.md) · [Plugins](docs/PLUGINS.md)

## License

MIT. Minecraft is a trademark of Mojang/Microsoft.
