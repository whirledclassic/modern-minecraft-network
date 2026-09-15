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

That internal ledger is the payment system included in this repo. It does **not** collect card numbers. For real money, take payment however you want (PayPal Friends, bank, Stripe later) and confirm the matching order in the console.

## Ranks granted

| Plan | LuckPerms group | Length |
| --- | --- | --- |
| VIP | `vip` | 30 days |
| Elite | `elite` | 30 days |
| Champion | `champion` | lifetime |

Expired timed ranks are removed about once an hour.

## Go live

```
DEMO_PAYMENTS=false
JOIN_HOST=play.yourdomain.com
```

Then restart `platform`.
