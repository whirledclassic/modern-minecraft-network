# Plugin guide

Core plugins install automatically from Modrinth / Geyser downloads.

## Auto-installed

### Proxy
- Geyser-Velocity
- Floodgate-Velocity

### Both Paper servers
- ModernNetwork (custom hub / selector / maps)
- LuckPerms, Vault, PlaceholderAPI, ViaVersion

### Lobby
- TAB

### Survival
- EssentialsX, WorldGuard, CoreProtect, GriefPrevention, Spark

## Drop-in folders

- `plugins/lobby/` — extra Paper lobby jars
- `plugins/survival/` — extra Paper survival jars
- `plugins/proxy/` — Velocity jars only

Restart after adding jars:

```bash
docker compose restart lobby
```

## Useful first permissions

```
/lp user YourName permission set * true
/lp group default permission set essentials.spawn true
/lp group default permission set essentials.tpa true
/lp group default permission set essentials.home true
/lp group default permission set essentials.sethome true
/lp group default permission set velocity.command.server true
```
