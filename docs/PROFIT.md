# Profit plan

Small Minecraft networks make money from **retention**, not from adding more game modes in week one.

## Legal fence (read this)

Mojang's commercial guidelines and the Minecraft EULA allow a server to sell **cosmetics and convenience**. They do not allow you to sell the game, claim you are official, or sell combat power that turns PvP into a cash shop.

Safe to sell here:

- Chat prefix / color
- Extra homes
- Lobby flight / queue priority
- Cosmetics, pets, particle trails (later)
- Cosmetic crates (later, if the loot is cosmetic)

Do not sell:

- Pay-to-win weapons or god kits on a PvP server
- Pay-to-clear claims of other players
- Anything that looks like you are reselling Minecraft itself

This template's VIP / Elite / Champion perks are convenience + identity. Keep them there.

## Unit economics (honest)

Typical one-box host:

- VPS 8 GB: about $20–40 / month
- Domain: about $12 / year
- Your time: the real cost

Break-even on hosting alone:

- ~8× VIP at $4.99 / 30 days, or
- ~4× Elite, or
- ~2× Champion (worse for recurring revenue — do not push lifetime too hard)

A healthy mix is **mostly monthly ranks**, one expensive lifetime for whales.

Conversion on a decent small survival box is often 3–8% of weekly unique players. That means:

| Weekly uniques | Paying members at 5% |
| --- | --- |
| 40 | ~2 |
| 100 | ~5 |
| 250 | ~12 |

You do not need 2,000 online. You need a reason to log in tomorrow.

## What actually sells

1. A spawn that looks finished
2. Claims that work (already in the stack)
3. Visible ranks in chat and TAB
4. Staff that answer in Discord the same day
5. Events every weekend (build contest, treasure hunt)

Store pages do not sell ranks. The server does. The store only collects.

## 90-day model

**Days 1–14 — private beta**
Friends + one public listing. Demo payments on a local copy only. Public copy has `DEMO_PAYMENTS=false`.

**Days 15–45 — first 20 regulars**
Daily login reward (Essentials kits), one Discord ticket channel, one event. Goal: 5 monthly ranks.

**Days 46–90 — tighten the loop**
Shared LuckPerms database, better lobby map, cosmetics. Goal: hosting + domain paid for by the store.

Do not add Skyblock, BedWars, and Prison in month one. Each extra mode splits the player base and multiplies plugins you cannot staff.

## How money should move

1. Player pays you off-site (PayPal, Stripe Checkout, Ko-fi, whatever you already have).
2. You match the username to the pending order in `/console`.
3. Click **Mark paid + grant**.
4. LuckPerms applies on the live servers.

That is slower than Tebex. It is also honest and PCI-safe. When volume hurts, plug Stripe Checkout or Tebex into the same fulfill step. Do not invent a card form.

## Pricing you can defend

| SKU | Price | Why |
| --- | --- | --- |
| VIP | $4.99 / 30d | Impulse buy, should be most of the volume |
| Elite | $9.99 / 30d | The "I play here" rank |
| Champion | $24.99 lifetime | Vanity. Cap the perks so monthly still wins |

Raise prices only after people already ask for the rank in chat.
