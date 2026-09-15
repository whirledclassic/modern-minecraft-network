# Economy

Survival uses **EssentialsX + Vault**. That is a real currency. It is not decorative.

## What players get

- **$500** the first time they join survival
- `/bal` shows their money
- `/pay Name 10` sends $10
- `/baltop` richest players
- `/kit starter` stone tools + bread (once per day)
- `/sell hand` sells the item they hold, using prices in `config/worth.yml`
- Buy/sell **signs** at spawn (you place these once)

## Player commands you should tell them

```
/bal
/pay <player> <amount>
/baltop
/kit starter
/sell hand
/worth
/home
/sethome
/tpa <player>
```

## Place the spawn shop (you, once)

1. Go to the plaza at `0 81 0`.
2. Place a sign. Type exactly these four lines:

Buy food:

```
[Buy]
8
$20
cooked_beef
```

Sell iron:

```
[Sell]
16
$24
iron_ingot
```

Balance check:

```
[Balance]
```

3. Walk away and right-click the sign as a non-op test account if you can.
4. `/setwarp shop` while standing there so `/warp shop` works.

Players need `essentials.signs.use.buy` (already given to `default` on boot).
You need `essentials.signs.create.buy` (ops have it).

## Staff money commands

```
/eco give Steve 1000
/eco take Steve 50
/eco set Steve 500
```

Use this when you confirm a website order that included cash, or to refund.

## Change prices

Edit `config/worth.yml`, then:

```
/essentials reload
```

`/worth` in-game shows the live sell price of the item in your hand.

## Why `/bal` might fail

- You are in the **lobby**. Economy lives on **survival**. `/server survival` first.
- LuckPerms has not finished first-boot commands. Wait a minute, or paste the permission lines from `config/rcon-startup-survival.txt`.
- You mounted an old world from before this update. Run the permission lines by hand.

## What we are not selling for cash

Do not sell swords that beat everyone in PvP. Sell prefixes, homes, kits, cosmetics. See [PROFIT.md](PROFIT.md).
