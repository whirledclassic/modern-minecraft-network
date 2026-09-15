# Ports

Open these on the VPS / router:

| Port | Proto | Why |
| --- | --- | --- |
| 25565 | TCP | Java |
| 19132 | UDP | Bedrock |
| 8080 | TCP | Website (or 443 if you add HTTPS later) |

Do **not** open:

| Port | Why |
| --- | --- |
| 25575 | RCON |
| 3306 | MariaDB |
| 25566+ | Paper backends |

Ubuntu example:

```bash
sudo ufw allow 25565/tcp
sudo ufw allow 19132/udp
sudo ufw allow 8080/tcp
sudo ufw enable
```

Or: `sudo ./scripts/firewall-ufw.sh`
