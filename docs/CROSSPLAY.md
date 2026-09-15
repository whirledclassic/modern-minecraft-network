# Java + Bedrock crossplay

Geyser and Floodgate run on the **Velocity proxy**.

| Client | Address | Port |
| --- | --- |
| Java Edition | your IP or domain | `25565` TCP |
| Bedrock (phone, console, Windows Bedrock) | same IP | `19132` UDP |

Bedrock players show up with a `.` prefix (example: `.Steve`) unless they link a Java account.

## Firewall

Open **TCP 25565** and **UDP 19132**. Do not open backend or RCON ports.

## First Bedrock join

1. Start the stack once so Floodgate can generate `key.pem`.
2. Xbox Live login on the Bedrock client.
3. Add server → IP of your host, port `19132`.

If Bedrock cannot see the server, the UDP port is almost always blocked.

## Optional: link Java + Bedrock skins / names

Global linking is enabled in `config/floodgate.yml`. Players can use Floodgate's link flow so a Bedrock account uses a Java username.

Putting Floodgate on the Paper backends is only required if you want the Floodgate API inside lobby/survival plugins. The default template does not do that.
