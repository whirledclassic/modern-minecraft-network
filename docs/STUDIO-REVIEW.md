# Studio review

Reviewed as a network engineer / server owner, not as a feature dump.

## Verdict

This repo is a **strong starter network**. It is not yet a profitable product.

It will boot a real Java + Bedrock network, put players in a lobby, move them to survival, and grant paid ranks over RCON. That is more than most first servers ever ship.

It will not retain players or take real money safely until the gaps below are closed.

## What is already correct

- Velocity in front of Paper is the 2026 default. Do not go back to BungeeCord.
- Online-mode on the proxy, offline-mode on backends, modern forwarding: correct.
- Geyser + Floodgate on the proxy: correct place for crossplay.
- RCON published only on the Docker network: correct.
- Store does not collect card numbers: correct. Keep it that way.
- LuckPerms groups created on boot: correct foundation for ranks.
- Installer + compose: the right packaging for a one-box host.

## What will break first in production

1. **LuckPerms is not shared.** Lobby and survival each get their own LP file. A VIP granted on survival can look unranked in lobby. Before any real sales, put LuckPerms on MySQL/MariaDB and point both Paper servers at it.
2. **No scheduled backups you actually test.** `scripts/backup.sh` exists. Run it from cron and restore once on a spare folder or you do not have backups.
3. **The compass GUI plugin is not in the image.** Players must type `/server survival`. Fine for friends. Weak for public traffic.
4. **Survival spawn datapack is a stub.** First impression is still vanilla dirt. Public servers lose people in 30 seconds if spawn is ugly.
5. **`admin/` is leftover.** The live UI is `platform/`. Ignore `admin/` or delete it later.
6. **Geyser `key.pem` is generated at runtime.** Do not commit it. Do not share it.
7. **Platform status depends on RCON.** If Paper is still downloading on first boot, the site shows "warming up". That is expected, not a crash.

## What is missing before you take money

- Rules, privacy note, and refund rule on the website
- Discord (support + staff + purchase log)
- Anti-cheat appropriate to a small survival box (start with Paper defaults + CoreProtect, add more only if you have PvP problems)
- Chat format / TAB prefixes so paid ranks are visible
- One staff account that is not the Docker host password
- A domain pointed at the host (`play.` and `store.` can be the same IP)
- `DEMO_PAYMENTS=false` on the public box

## Architecture score (now / after 30 days)

| Area | Now | 30-day target |
| --- | --- | --- |
| Proxy + forwarding | 8/10 | 9/10 |
| Crossplay | 7/10 | 8/10 |
| Lobby feel | 5/10 | 8/10 |
| Survival loop | 6/10 | 8/10 |
| Ranks + store | 6/10 | 8/10 |
| Ops (backup/monitor) | 4/10 | 8/10 |
| Monetization readiness | 4/10 | 7/10 |
