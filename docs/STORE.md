# Website, store, and memberships

The `platform` container is the all-in-one web client:

| URL | What |
| --- | --- |
| `http://HOST:8080/` | Public site + live status + membership shop |
| `http://HOST:8080/console` | Admin console (Basic auth) |

## How a purchase works

1. Player enters their Java username and picks VIP / Elite / Champion.
2. The site creates an order in `/data/orders.json`.
3. If `DEMO_PAYMENTS=true`, checkout completes immediately and LuckPerms is updated over RCON.
4. If `DEMO_PAYMENTS=false`, the order stays **pending**. Staff open `/console` and click **Mark paid + grant**.

That internal ledger does **not** collect card numbers. Take payment off-site, then confirm the order.

Sell convenience and identity only. See [PROFIT.md](PROFIT.md) for the EULA fence.

## Ranks granted

| Plan | LuckPerms group | Length | Prefix |
| --- | --- | --- | --- |
| VIP | `vip` | 30 days | `[VIP]` |
| Elite | `elite` | 30 days | `[Elite]` |
| Champion | `champion` | lifetime | `[Champion]` |

Timed ranks are removed about once an hour after expiry.

## Go live

```
DEMO_PAYMENTS=false
JOIN_HOST=play.example.com
```

Restart `platform`. Confirm one real $1 test order before you post the IP anywhere public.
