# Plugin guide

Core plugins are installed automatically by the Paper containers from Modrinth on first start.

## Auto-installed

### Both backends

| Plugin | Why |
| --- | --- |
| LuckPerms | Ranks and permissions |
| Vault | Economy / permission bridge |
| PlaceholderAPI | `%player_name%` and scoreboard placeholders |
| ViaVersion | Newer clients can join |

### Lobby only

| Plugin | Why |
| --- | --- |
| TAB | Header/footer, nametags, sorted tab list |

### Survival only

| Plugin | Why |
| --- | --- |
| EssentialsX | Homes, warps, kits, TPA, spawn, economy |
| WorldGuard | Protect spawn and regions |
| CoreProtect | Inspect and rollback grief |
| GriefPrevention | Player land claims with a golden shovel |
| Spark | Lag profiler |

## Drop-in folders

Put extra `.jar` files here. They are copied into the server on start:

- `plugins/lobby/` — Paper lobby plugins
- `plugins/survival/` — Paper survival plugins
- `plugins/proxy/` — Velocity plugins (not Bukkit plugins)

Restart the matching service after adding jars:

```bash
docker compose restart lobby
```

## Recommended next plugins (not auto-installed)

Download these yourself and drop them in the folders above. Check that the file is built for your exact Paper / Velocity version.

### Make the lobby feel like a real network

- **DeluxeHub** or **UltimateLobby** — double-jump, launch pads, lobby items, server selector
- **CommandPanels** or **DeluxeMenus** — GUI to click “Survival”
- **Citizens** + **DecentHolograms** — NPC that runs `/server survival`
- **WorldEdit** or **FastAsyncWorldEdit** — build the hub faster

Example selector command once DeluxeHub / a menu plugin is installed:

```
/server survival
```

That command is provided by Velocity to players connected through the proxy.

### Survival quality of life

- **EconomyShopGUI** or **ChestShop** — player shops
- **mcMMO** — skills
- **BlueMap** or **Dynmap** — live web map
- **DiscordSRV** — Discord chat bridge
- **CoreProtect** is already included; add **LWC** if you want chest locking on top of claims

### Cross-play (Bedrock phones / consoles)

Install on the **proxy** or a dedicated Geyser service:

- GeyserMC
- Floodgate

Then publish UDP `19132` as well as TCP `25565`.

### Network-wide LuckPerms

Right now each Paper server has its own LuckPerms file storage. For one rank list everywhere:

1. Stand up MariaDB / Postgres
2. Point both lobby and survival LuckPerms at the same database
3. Optionally install LuckPerms-Velocity in `plugins/proxy/`

## Permissions to set first

After you `op` yourself:

```
/lp user YourName permission set * true
```

Create basic groups on survival:

```
/lp creategroup member
/lp creategroup vip
/lp creategroup mod
/lp creategroup admin

/lp group member parent set default
/lp group default permission set essentials.spawn true
/lp group default permission set essentials.tpa true
/lp group default permission set essentials.tpahere true
/lp group default permission set essentials.home true
/lp group default permission set essentials.sethome true
/lp group default permission set essentials.msg true
/lp group default permission set essentials.balance true
/lp group default permission set velocity.command.server true
```

`velocity.command.server` lets players run `/server survival` and `/server lobby`.
