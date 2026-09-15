# Sales consultant notes

The product is an SMP, not a cash shop. People pay after the world already feels like theirs.

## Natural progression (do not skip steps)

| Time | What they should do | Money |
| --- | --- | --- |
| Minute 1 | Join, `/server survival` | $0 |
| Minutes 2–20 | `/kit starter`, claim land, `/sethome`, mine, `/sell hand` | in-game $ |
| Session 2–4 | Base, `/baltop`, warp shop | still free |
| Week 2+ | Prefix + extra homes if they log in daily | VIP $4.99 |
| Regulars | Elite | $9.99 / 30d |
| Whales who already play | Champion | $14.99 / 30d |

If the first hour is confusing, they never see the store. Rank ads in minute one read as a cash grab.

## What was broken

1. **Bedrock checkout rejected `.Steve`.** Floodgate prefixes a dot. The store regex only allowed Java names. That is a lost sale, not a style issue.
2. **Champion at $24.99 lifetime.** Five months of Elite and they never pay again. Lifetime is for vanity at a high price, or it is a monthly prestige rank.
3. **Staff console was a stub.** Pending orders with `DEMO_PAYMENTS=false` had no grant button. You cannot run a store that staff cannot close.
4. **TAB footer pushed the store before `/kit`.** First-hour commands first.
5. **Paid iron tools** were already removed. Keep it that way.

## What good looks like

- Free loop is complete: kit → claim → home → sell → shop signs.
- Ranks buy identity and convenience, not PvP power.
- Most revenue is **monthly VIP/Elite**, not one lifetime SKU.
- Staff can grant a rank in under 30 seconds after off-site payment.
- You quote the name from `/list`, including the Bedrock dot.

## Conversion math (keep using this)

Weekly uniques × 5% ≈ paying members if the SMP is worth opening tomorrow.

8× VIP covers a cheap VPS. Do not add Skyblock to "make more SKUs." Add a weekend event so the same 40 people come back.
