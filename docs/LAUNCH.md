# 30-day launch checklist

## Day 0

- [ ] `./scripts/install.sh` on the VPS
- [ ] Change `ADMIN_PASSWORD`, `RCON_PASSWORD`, `VELOCITY_SECRET`
- [ ] `DEMO_PAYMENTS=false` on the public host
- [ ] `JOIN_HOST=play.yourdomain.com`
- [ ] Open TCP 25565, UDP 19132, TCP 8080 (or put 8080 behind a reverse proxy + HTTPS)
- [ ] Do **not** publish 25575 or backend ports

## Day 1

- [ ] Join Java and Bedrock yourself
- [ ] `/server survival` works both ways
- [ ] Op your Java account, then `/lp user You permission set * true`
- [ ] Place a rules sign at survival spawn
- [ ] Create Discord: #announcements, #chat, #support, #staff

## Day 2

- [ ] `./scripts/backup.sh` once by hand
- [ ] Restore that tarball to a temp folder so you know it opens
- [ ] Add a daily cron for `scripts/backup.sh`
- [ ] Run `./scripts/health.sh`

## First week

- [ ] 10 friends online at the same time once
- [ ] One purchase tested end-to-end (friend pays you $1, you grant VIP, they see prefix)
- [ ] CoreProtect inspect works on a test block
- [ ] GriefPrevention shovel explained in Discord

## Before public ads

- [ ] Shared LuckPerms MySQL (lobby + survival)
- [ ] TAB / chat prefix showing VIP Elite Champion
- [ ] Privacy + refund sentence on the site
- [ ] Spawn looks intentional
