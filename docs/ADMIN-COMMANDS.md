# Admin commands (copy and paste)

Type these in **survival chat** unless it says console.
You need to be op, or have `lp user You permission set * true`.

The website console at `/console` can send the same commands without you being in-game. Pick the server dropdown first (lobby or survival).

## You, ranks, and staff

```
/lp user Steve permission set * true
/lp user Steve parent add champion
/lp user Alex parent add staff
/lp user Alex parent remove vip
/lp group default listmembers
/lp info
```

`staff` is a helper group created on boot. Give it to moderators. Do not give `*` to random helpers.

## Money

```
/bal
/bal Steve
/baltop
/eco give Steve 1000
/eco take Steve 50
/eco set Steve 500
/eco reset Steve
/pay Steve 25
```

`/eco` is staff-only. `/pay` is for players.

## Kits and spawn

```
/kit starter
/kit vip
/createkit vip 86400
/setspawn
/spawn
/setwarp shop
/warp shop
```

`/createkit vip 86400` saves whatever is in your inventory as the VIP kit, 24 hour cooldown.

Stand on the plaza, then `/setspawn` so deaths return there.

## Players in trouble

```
/gm spectator
/tp Steve
/tphere Steve
/kick Steve stop that
/ban Steve cheating
/pardon Steve
/mute Steve 1h
/invsee Steve
/seen Steve
/whois Steve
```

Switch back with `/gm survival`.

## Grief and rollback (CoreProtect)

Look at a block, then:

```
/co i
```

Click the block. You will see who broke or placed it.

```
/co rollback u:Steve t:1h r:20
/co restore u:Steve t:1h r:20
/co lookup u:Steve t:24h
```

`t:1h` = last hour. `r:20` = 20 block radius. You must stand near the damage.

## Claims (GriefPrevention)

Give a golden shovel. Players right-click two corners.

```
/claims list
/transferclaim Steve
/abandonallclaims
```

Staff can `/ignoreclaims` then build inside someone else's claim to fix it. Type it again to turn off.

## WorldGuard (lock the plaza)

Stand in one corner, then the opposite corner:

```
//wand
//pos1
//pos2
/rg define spawn
/rg flag spawn pvp deny
/rg flag spawn creeper-explosion deny
/rg addowner spawn Steve
```

WorldEdit wand is not installed by default. Use WorldGuard's own selection if `//wand` fails:

```
/wg wand
```

or select with `/rg define` after using WorldGuard positions.

## Server switch and proxy

```
/server lobby
/server survival
```

From the website console you can also:

```
say Event starts in 10 minutes. Meet at spawn.
save-all
list
tps
```

## Store ranks

1. Player buys on the website or pays you off-site.
2. Open `http://YOUR_IP:8080/console`
3. Find the order.
4. Click **Mark paid + grant**.

Or in-game:

```
/lp user Steve parent add vip
```

## Do not run these unless you mean it

```
/stop
op Steve
deop Steve
whitelist on
whitelist add Steve
```

`/stop` inside a container just restarts that world if Compose is set to `unless-stopped`. To shut the whole network down use `docker compose down` on the host.
