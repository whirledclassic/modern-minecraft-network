# Admin panel

A small web panel ships as the `admin` service.

URL: `http://YOUR_IP:8080`

Default login comes from `.env`:

```
ADMIN_USER=admin
ADMIN_PASSWORD=change-me-admin
```

Change those before you expose port 8080.

## What it can do

- Live status for lobby + survival
- Online player lists
- Send any console command (`say`, `op`, `kick`, `whitelist`, `tps`, `save-all`)
- Broadcast an announcement

It talks to Paper over **RCON on the Docker network**. RCON is not published to the internet.

## Security

- Put the panel behind a VPN, SSH tunnel, or reverse proxy with HTTPS if this host is public.
- Use a long `ADMIN_PASSWORD` and `RCON_PASSWORD`.
- Do not map `25575` on the host.
