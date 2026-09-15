# Custom maps

The `ModernNetwork` plugin builds maps on first boot.

## Lobby

Void-style superflat world. The plugin places a floating modern hub at `0,64,0`:

- Deepslate / quartz / cyan concrete platform
- Beacon center
- Corner light pillars
- Glass rim
- Signs for Survival and crossplay
- Always-day, no rain, no mobs

Players join in adventure + flight with a compass. Right-click opens the server selector and sends them through Velocity.

Rebuild:

```
/hubadmin rebuild
```

(from an op account on the lobby)

## Survival

Vanilla overworld terrain (set `SURVIVAL_SEED` in `.env` if you want a known seed). On first boot the plugin flattens a small spawn plaza around world spawn:

- Stone / deepslate pad
- Lantern posts
- Rules sign
- World spawn on the plaza

Players still get a normal survival map beyond that pad. GriefPrevention claims start working as soon as someone uses a golden shovel.

## Replace with a downloaded map

1. Stop the stack: `docker compose down`
2. Copy a world folder into the volume (or change compose to bind-mount `./worlds/survival:/data/world`)
3. Set `build-on-start: false` in `plugins/survival/ModernNetwork/config.yml` so the plaza builder does not overwrite the map
4. Start again

Same idea for a custom lobby schematic / world download.
