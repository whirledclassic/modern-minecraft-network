# Modern Minecraft Network

Java + Bedrock network with lobby, survival, money, ranks, website, and admin console.

**If you have never hosted a server, read [docs/START-HERE.md](docs/START-HERE.md) first.**

```bash
./scripts/install.sh
./scripts/health.sh
```

## Play loop

1. Join `localhost:25565` (Bedrock: UDP `19132`)
2. `/server survival`
3. `/bal` — you start with $500
4. `/kit starter` — tools and bread
5. Mine, `/sell hand`, `/pay` friends, `/sethome`
6. Website ranks: `http://localhost:8080`

## Staff

- In-game commands: [docs/ADMIN-COMMANDS.md](docs/ADMIN-COMMANDS.md)
- Website console: `http://localhost:8080/console`
- Put your Java name in `.env` as `OPS=YourName`

## More docs

- [Economy](docs/ECONOMY.md)
- [Launch checklist](docs/LAUNCH.md)
- [Profit plan](docs/PROFIT.md)
- [Shared ranks](docs/DATABASE.md)
- [Crossplay](docs/CROSSPLAY.md)
