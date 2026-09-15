# Java + Bedrock crossplay

Geyser + Floodgate run on **Velocity only**.

| Client | Port |
| --- | --- |
| Java | 25565 TCP |
| Bedrock | 19132 UDP |

Bedrock names get a `.` prefix (`.Steve`) until they link a Java account. Grant shop ranks to the name you see in `/list`.

`auth-type` is `floodgate`. `use-proxy-protocol` stays false unless you put TCPShield or similar in front.

Firewall: [FIREWALL.md](FIREWALL.md). If Java works and Bedrock does not, UDP 19132 is closed.

Floodgate on Paper is optional and needs a copied `key.pem`. This template does not do that.
