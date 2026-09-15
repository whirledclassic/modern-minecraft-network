# Evening research notes (Sep 2026)

What current public docs and hosting practice say, and what we changed because of it.

## Stack choice — still correct

Paper + Velocity + Geyser-Velocity + Floodgate-Velocity is the default 2026 small-network shape. Do not go back to BungeeCord. Do not put Geyser on every Paper box unless you have a reason.

Geyser's own docs: Floodgate lives on the **proxy**. Paper Floodgate is only for the Floodgate API / skins without a server switch. We stay proxy-only so you do not have to copy `key.pem` by hand.

Bedrock is **UDP 19132**. If phones cannot see the server, the firewall is wrong. Not Geyser.

## RAM

Velocity-with-Geyser hosts now recommend about **1 GB** on the proxy, not 512 MB. 512 MB is fine for a bare proxy. Geyser is not bare.

Default `PROXY_MEMORY` is now `1G`.

## Forwarding secret

Modern forwarding only works if the same secret is on Velocity and both Paper boxes. `scripts/new-secret.sh` writes `proxy/forwarding.secret` and `VELOCITY_SECRET` together. Do not commit a real secret. The file in git is a placeholder.

## Economy vs Mojang rules (2026 reading)

Usage guidelines still allow cosmetics and convenience. They do not allow selling combat power.

| We sell | Why it is OK |
| --- | --- |
| Prefix / color | Cosmetic |
| Extra homes | Convenience |
| Starter kit for everyone | Not paid |

| We stopped selling | Why |
| --- | --- |
| VIP iron pickaxe kit | Paid gear is the usual EULA complaint |
| Champion `/fly` on survival | Movement advantage in PvP |

In-game `$` from mining and `/sell` is fine. Do not sell dollars for real money.

Sources we used: Geyser/Floodgate wiki, itzg RCON/env-replace docs, Bloom Velocity RAM notes, Minecraft usage-guidelines writeups from mid-2026. None of those pages are Mojang legal advice.

## itzg details that matter here

- `RCON_CMDS_STARTUP` is a real hook. Our rank and eco permissions run there.
- `REPLACE_ENV_VARIABLES` + `CFG_` rewrites LuckPerms DB password inside `/data`.
- LuckPerms config is mounted before first plugin extract. If LP later rewrites the file, check `lp info` still says MariaDB.

## Still not done (intentionally)

- HTTPS in front of `:8080` — needs a domain and Caddy/nginx on the host
- Floodgate on Paper for skins — needs `key.pem` copy
- Anti-cheat pack — add only after you have PvP problems
- Tebex/Stripe Checkout — attach to the existing fulfill step when volume hurts
