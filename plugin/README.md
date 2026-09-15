# ModernNetwork plugin

Custom Paper plugin shipped with this template.

On first boot `bootstrap` decodes `ModernNetwork.jar.b64` into:

- `plugins/lobby/ModernNetwork.jar` with `server-id: lobby`
- `plugins/survival/ModernNetwork.jar` with `server-id: survival`

## Lobby features

- Builds the floating modern hub
- Compass server selector
- Adventure + flight + always day
- Transfers players to `survival` through Velocity

## Survival features

- Builds a small spawn plaza
- `/hub` returns to the lobby

## Rebuild

```
/hubadmin rebuild
```

Source: `plugin/src/net/modernmc/ModernNetwork.java`
