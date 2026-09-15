# Shared LuckPerms

Lobby and survival now share one MariaDB database so a store grant on one box is visible on the other.

```
db:3306
database: luckperms
user: luckperms
```

Password comes from `DB_PASSWORD` in `.env` and is written into the LuckPerms configs as `CFG_LP_PASSWORD`.

## After first boot

```
docker compose logs db | tail
docker exec modern-mc-survival rcon-cli lp info
```

You want `Storage method: MariaDB`, not YAML.

## Existing worlds

If you already ran the stack with file-based LuckPerms, groups live in the Paper volumes. After this update:

1. `docker compose up -d db`
2. Restart lobby + survival
3. Recreate groups if needed (`RCON_CMDS_STARTUP` still does this)
4. Re-grant shop ranks for anyone who paid before the switch

Do not expose MariaDB on the public NIC. Compose keeps it on `mcnet` only.
