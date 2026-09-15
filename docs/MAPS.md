# Maps

Datapacks build the first-look pads. The optional `ModernNetwork` plugin is not required.

## Lobby

Superflat void-style world. Datapack `datapacks/lobby` places a hub at `0,64,0`:

deepslate + quartz pad, beacon, glass rim, corner pillars, world spawn on the pad.

Rebuild from an op:

```
/function modernhub:build
```

## Survival

Vanilla overworld. Datapack `datapacks/survival` places a plaza at `0,80,0` on first boot (guarded by a bedrock marker at `0 1 0`):

polished deepslate pad, beacon, lanterns, tight spawn radius.

Set `SURVIVAL_SEED` in `.env` to keep terrain stable across wipes.

Rebuild:

```
/function modernspawn:build
```

## Drop in a downloaded world

1. `docker compose down`
2. Bind-mount or copy the world into the volume
3. Remove or don't run the build function if you do not want the plaza
