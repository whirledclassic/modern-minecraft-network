# Modern Minecraft Network

All-in-one **Java + Bedrock** network with a website, membership store, and admin console.

```
./scripts/install.sh
```

That installer writes `.env`, generates secrets, and starts every service.

## What boots together

| Piece | Address |
| --- | --- |
| Java | `:25565` |
| Bedrock | UDP `:19132` |
| Website + store | `:8080` |
| Admin console | `:8080/console` |
| Lobby | Velocity backend |
| Survival | Velocity backend |

Players land in the lobby, run `/server survival`, and buy VIP / Elite / Champion on the site. Paid orders grant LuckPerms groups over RCON.

## One-command install

```bash
git clone https://github.com/whirledclassic/modern-minecraft-network.git
cd modern-minecraft-network
./scripts/install.sh
```

Windows (Docker Desktop required):

```powershell
.\scripts\install.ps1
```

First start downloads Paper, Velocity, Geyser, Floodgate, and plugins. Give it a few minutes, then:

1. Join `localhost:25565`
2. Open `http://localhost:8080`
3. Log into `http://localhost:8080/console` with `ADMIN_USER` / `ADMIN_PASSWORD`

## Memberships

| Rank | Default price | Perks |
| --- | --- | --- |
| VIP | $4.99 / 30d | prefix, 3 homes |
| Elite | $9.99 / 30d | VIP + more homes |
| Champion | $24.99 lifetime | Elite + fly permission |

`DEMO_PAYMENTS=true` completes test checkouts so you can see ranks apply. Set it to `false` before taking real money, then confirm orders in the console. The store never asks for card numbers.

Details: [docs/STORE.md](docs/STORE.md)

## Everyday commands

```bash
docker compose logs -f
docker compose ps
./scripts/backup.sh
docker compose down
```

## Docs

- [Store & memberships](docs/STORE.md)
- [Crossplay](docs/CROSSPLAY.md)
- [Maps](docs/MAPS.md)
- [Plugins](docs/PLUGINS.md)

## License

MIT. Minecraft is a trademark of Mojang/Microsoft. Paper, Velocity, Geyser, and Floodgate belong to their authors.
