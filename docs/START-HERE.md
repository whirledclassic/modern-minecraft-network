# Start here if you have never hosted a server

Read this top to bottom. Do not skip. You do not need to know Docker, Linux, or Java.

## What you are building

One computer (or a rented VPS) will run:

- a front door players connect to (Velocity)
- a lobby world
- a survival world with money, homes, claims, and shops
- a website + shop at port 8080

Players type **one IP**. Java uses port 25565. Bedrock uses port 19132.

## What you must install first

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) on Windows or Mac.
   On Ubuntu: `sudo apt install docker.io docker-compose-v2`
2. Leave Docker running. The whale / Docker icon should be awake.
3. You need about **8 GB of free RAM** for lobby + survival together.

If Docker is not running, nothing else works. That is the #1 failure.

## One-time setup

Open a terminal **in the project folder** (the folder that contains `docker-compose.yml`).

Windows: open the folder in File Explorer, click the address bar, type `powershell`, press Enter.

Then run:

```bash
./scripts/install.sh
```

Windows if bash is missing:

```powershell
.\scripts\install.ps1
```

The first start downloads Minecraft server files. That can take 5–15 minutes. Go make coffee. Do not close the window if it is still printing text.

## Did it work?

```bash
./scripts/health.sh
```

You want to see words like `running` next to:

- modern-mc-db
- modern-mc-lobby
- modern-mc-survival
- modern-mc-platform
- modern-mc-proxy

If lobby/survival say `starting` for a long time, wait. First boot is slow.

If it says `missing`, you are in the wrong folder. `cd` into the repo and try again.

## Join the game

**Java**

1. Open Minecraft Java.
2. Multiplayer → Direct Connection.
3. Type `localhost` if the server is on this same PC.
4. If the server is a VPS, type that machine's IP, like `203.0.113.10`.
5. Join. You spawn in the lobby.
6. Type `/server survival` and press Enter.

**Bedrock (phone, console, Windows Bedrock)**

1. Servers → Add Server.
2. Address: same IP as Java.
3. Port: `19132`.
4. Join, then `/server survival`.

## Make yourself admin

1. Open `.env` in a text editor.
2. Add a line (use your exact Java username):

```
OPS=Steve
```

3. Save.
4. Run:

```bash
docker compose up -d
```

5. Rejoin. You should be op.
6. In survival chat type:

```
/lp user Steve permission set * true
```

Replace Steve. You now have every staff command.

Website admin:

- Open `http://localhost:8080/console`
- Login is `ADMIN_USER` and `ADMIN_PASSWORD` from `.env`
- Change those passwords before anyone else can reach port 8080

## Money check

In survival type `/bal`. You should see dollars.
Type `/kit starter`. You should get tools and bread.
Type `/pay` to see usage.

If `/bal` says you do not have permission, you started an old container. Run `docker compose up -d` again after pulling, then `/lp group default permission set essentials.bal true`.

## Tell friends how to join

They use **your public IP** or a domain you pointed at the VPS.

- Java: `your.ip.here`
- Bedrock: same IP, port `19132`
- Website: `http://your.ip.here:8080`

On a home PC you must port-forward 25565 TCP, 19132 UDP, and 8080 TCP on the router. On a VPS, open those ports in the cloud firewall.

Never open port 25575 or 3306.

## Daily buttons

| What you want | What you type |
| --- | --- |
| Is it up? | `./scripts/health.sh` |
| Read logs | `docker compose logs -f` |
| Stop | `docker compose down` |
| Start | `docker compose up -d` |
| Backup worlds | `./scripts/backup.sh` |

## Next pages

- [Admin commands](ADMIN-COMMANDS.md) — copy/paste staff tools
- [Economy](ECONOMY.md) — money, shops, kits
- [Launch checklist](LAUNCH.md) — before you post the IP in public
