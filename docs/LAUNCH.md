# 30-day launch checklist

## Day 0

- [ ] `./scripts/install.sh` on the VPS
- [ ] Confirm `DB_PASSWORD` and `RCON_PASSWORD` were generated
- [ ] `DEMO_PAYMENTS=false` on the public host
- [ ] `JOIN_HOST=play.yourdomain.com`
- [ ] Open TCP 25565, UDP 19132, TCP 8080 (or HTTPS reverse proxy)
- [ ] Do **not** publish 25575, 3306, or backend ports

## Day 1

- [ ] Join Java and Bedrock
- [ ] `/server survival` works both ways
- [ ] `./scripts/health.sh` shows MariaDB + `lp info` using MariaDB
- [ ] Op your account
- [ ] Stand on the survival plaza at `0 81 0`
- [ ] Discord: #announcements, #chat, #support, #staff

## Day 2

- [ ] `./scripts/backup.sh` by hand, then unpack it once
- [ ] Daily cron for `scripts/backup.sh`
- [ ] Demo grant on a local copy, then one real $1 grant on public with DEMO off

## Before public ads

- [ ] VIP prefix visible in chat / TAB
- [ ] CoreProtect inspect works
- [ ] GriefPrevention explained in Discord
- [ ] Privacy + refund sentence on the site
