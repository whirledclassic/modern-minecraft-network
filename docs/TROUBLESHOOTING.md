# Things that look broken but usually are not

## First boot takes forever

Paper, Velocity, Geyser, and plugin jars download on the first `compose up`. 5–15 minutes is normal. Watch:

```bash
docker compose logs -f lobby survival proxy
```

Wait until you see `Done (` on lobby and survival.

## Bedrock cannot find the server

1. Java works, Bedrock does not → **UDP 19132** is closed.
2. Cloud VPS: add a UDP 19132 inbound rule, not just TCP.
3. Home router: forward 19132 UDP to the Docker host.
4. You used port 25565 on Bedrock. Wrong. Bedrock is 19132.

## `/bal` says no permission

You are in the lobby. Type `/server survival` first.

## `/bal` works but prefix is missing in lobby

LuckPerms must be on MariaDB. `./scripts/health.sh` then `lp info` should say MariaDB. If it says YAML, the DB was not up on first boot — restart lobby and survival after `db` is healthy.

## Bought VIP, still default in lobby

Same as above, or you granted the rank on a name with a Floodgate dot. Bedrock users are `.Name` until they link. Grant the rank to the name you see in `/list`.

## Website says warming up

Paper RCON is not ready yet. Wait. If it stays down, `docker compose ps` and check the lobby/survival healthcheck.

## `forwarding secret` / cannot connect past Velocity

Run `./scripts/new-secret.sh` then `docker compose up -d`. Paper and Velocity must share the same secret.

## Out of memory on the proxy

Set `PROXY_MEMORY=1G` in `.env`. Geyser needs that.
