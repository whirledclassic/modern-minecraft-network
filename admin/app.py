#!/usr/bin/env python3
from __future__ import annotations
import base64, json, os, re, socket, struct, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

HOSTS = {
    "lobby": (os.environ.get("LOBBY_RCON_HOST", "lobby"), int(os.environ.get("LOBBY_RCON_PORT", "25575"))),
    "survival": (os.environ.get("SURVIVAL_RCON_HOST", "survival"), int(os.environ.get("SURVIVAL_RCON_PORT", "25575"))),
}
RCON_PASSWORD = os.environ.get("RCON_PASSWORD", "change-me")
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")
LISTEN = int(os.environ.get("ADMIN_PORT", "8080"))
_req_id = 1
_lock = threading.Lock()

def next_id():
    global _req_id
    with _lock:
        _req_id += 1
        return _req_id

def rcon(server: str, command: str, timeout: float = 4.0) -> str:
    host, port = HOSTS[server]
    sock = socket.create_connection((host, port), timeout=timeout)
    sock.settimeout(timeout)
    try:
        def packet(kind: int, body: str, pid: int) -> bytes:
            payload = struct.pack("<ii", pid, kind) + body.encode("utf-8") + b"\x00\x00"
            return struct.pack("<i", len(payload)) + payload
        def read():
            header = b""
            while len(header) < 4:
                chunk = sock.recv(4 - len(header))
                if not chunk:
                    raise ConnectionError("RCON closed")
                header += chunk
            (length,) = struct.unpack("<i", header)
            data = b""
            while len(data) < length:
                chunk = sock.recv(length - len(data))
                if not chunk:
                    raise ConnectionError("RCON closed")
                data += chunk
            pid, kind = struct.unpack("<ii", data[:8])
            body = data[8:-2].decode("utf-8", errors="replace")
            return pid, kind, body
        sock.sendall(packet(3, RCON_PASSWORD, next_id()))
        pid, _, _ = read()
        if pid == -1:
            raise PermissionError("RCON auth failed")
        sock.sendall(packet(2, command, next_id()))
        _, _, body = read()
        return body.strip()
    finally:
        sock.close()

def parse_list(raw: str) -> dict:
    names = []
    online = max_p = 0
    m = re.search(r"(\d+)\s+of\s+a\s+max\s+of\s+(\d+)", raw, re.I)
    if m:
        online, max_p = int(m.group(1)), int(m.group(2))
    if ":" in raw:
        names = [n.strip() for n in raw.split(":", 1)[1].split(",") if n.strip()]
    return {"online": online or len(names), "max": max_p, "players": names, "raw": raw}

def status_payload() -> dict:
    out = {"servers": {}}
    for name in HOSTS:
        try:
            listed = parse_list(rcon(name, "list"))
            tps = ""
            try:
                tps = rcon(name, "tps")
            except Exception:
                pass
            out["servers"][name] = {"ok": True, **listed, "tps": tps}
        except Exception as exc:
            out["servers"][name] = {"ok": False, "error": str(exc), "players": [], "online": 0, "max": 0, "tps": ""}
    return out

PAGE = """<!DOCTYPE html><html><head><meta charset='utf-8'/><meta name='viewport' content='width=device-width,initial-scale=1'/>
<title>Modern Network Admin</title>
<style>
:root{--bg:#07080d;--line:#1e2433;--text:#e8edf7;--muted:#8b95ab;--accent:#3ee0c9;--danger:#ff5d73;--ok:#3ee07a}
*{box-sizing:border-box}body{margin:0;font-family:ui-sans-serif,system-ui,sans-serif;background:radial-gradient(1200px 600px at 10% -10%,#12343a 0%,transparent 50%),#07080d;color:var(--text);min-height:100vh}
header{display:flex;justify-content:space-between;align-items:center;padding:22px 28px;border-bottom:1px solid var(--line)}
h1{margin:0;font-size:18px;letter-spacing:.12em;text-transform:uppercase}h1 span{color:var(--accent)}
.pill{font-size:12px;color:var(--muted);border:1px solid var(--line);padding:6px 10px;border-radius:999px}
main{display:grid;grid-template-columns:1fr 1fr;gap:18px;padding:22px;max-width:1200px;margin:0 auto}
.card{background:rgba(16,19,28,.9);border:1px solid var(--line);border-radius:18px;padding:18px}
h2{margin:0 0 12px;font-size:14px;color:var(--muted);letter-spacing:.08em;text-transform:uppercase}
.row{display:flex;justify-content:space-between;margin:8px 0}.ok{color:var(--ok)}.bad{color:var(--danger)}
.players{display:flex;flex-wrap:wrap;gap:8px;min-height:28px}
.tag{background:#171c28;border:1px solid var(--line);padding:4px 8px;border-radius:8px;font-size:13px}
input,select{width:100%;background:#0b0e16;color:var(--text);border:1px solid var(--line);border-radius:12px;padding:10px 12px}
button{background:linear-gradient(180deg,#4af0d6,#1fb8a5);color:#041210;border:0;border-radius:12px;padding:10px 14px;font-weight:700;cursor:pointer}
.ghost{background:transparent;color:var(--text);border:1px solid var(--line)}.danger{background:linear-gradient(180deg,#ff7b8b,#d63b52);color:#fff}
.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
pre{background:#0b0e16;border:1px solid var(--line);border-radius:12px;padding:12px;min-height:140px;overflow:auto;font-size:12px;color:#c9d4ea}
.span2{grid-column:1/-1}@media(max-width:860px){main{grid-template-columns:1fr}.span2{grid-column:auto}}
</style></head><body>
<header><h1>Modern <span>Network</span> Admin</h1><div class='pill' id='clock'>live</div></header>
<main>
<div class='card'><h2>Lobby</h2><div class='row'><span>Status</span><strong id='lobby-ok'>…</strong></div><div class='row'><span>Players</span><strong id='lobby-count'>—</strong></div><div class='players' id='lobby-players'></div></div>
<div class='card'><h2>Survival</h2><div class='row'><span>Status</span><strong id='survival-ok'>…</strong></div><div class='row'><span>Players</span><strong id='survival-count'>—</strong></div><div class='players' id='survival-players'></div></div>
<div class='card span2'><h2>Command console</h2>
<select id='target' style='max-width:220px;margin-bottom:8px'><option value='lobby'>lobby</option><option value='survival'>survival</option></select>
<input id='cmd' placeholder='say Hello  |  op Notch  |  kick Steve'/>
<div class='actions'><button onclick='runCmd()'>Send command</button><button class='ghost' onclick='quick("list")'>list</button><button class='ghost' onclick='quick("tps")'>tps</button><button class='ghost' onclick='announce()'>announce</button><button class='danger' onclick='quick("save-all")'>save-all</button></div>
<pre id='out'>Ready.</pre></div>
</main>
<script>
async function api(path,opts){const res=await fetch(path,Object.assign({headers:{'Content-Type':'application/json'}},opts||{}));if(!res.ok)throw new Error(await res.text());return res.json()}
function renderServer(name,data){const ok=document.getElementById(name+'-ok');const count=document.getElementById(name+'-count');const wrap=document.getElementById(name+'-players');ok.textContent=data.ok?'ONLINE':'DOWN';ok.className=data.ok?'ok':'bad';count.textContent=data.ok?(data.online+' / '+(data.max||'—')):(data.error||'unreachable');wrap.innerHTML='';(data.players||[]).forEach(p=>{const s=document.createElement('span');s.className='tag';s.textContent=p;wrap.appendChild(s)})}
async function refresh(){try{const data=await api('/api/status');renderServer('lobby',data.servers.lobby||{});renderServer('survival',data.servers.survival||{});document.getElementById('clock').textContent=new Date().toLocaleTimeString()}catch(e){document.getElementById('clock').textContent=e.message}}
async function runCmd(command){const server=document.getElementById('target').value;const cmd=command||document.getElementById('cmd').value;if(!cmd)return;document.getElementById('out').textContent='Running on '+server+'\u2026';try{const data=await api('/api/command',{method:'POST',body:JSON.stringify({server,command:cmd})});document.getElementById('out').textContent=data.output||'(no output)';refresh()}catch(e){document.getElementById('out').textContent=e.message}}
function quick(c){document.getElementById('cmd').value=c;runCmd(c)}
function announce(){const msg=prompt('Announcement');if(msg)runCmd('say '+msg)}
document.getElementById('cmd').addEventListener('keydown',e=>{if(e.key==='Enter')runCmd()});refresh();setInterval(refresh,5000);
</script></body></html>"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.address_string(), fmt % args))
    def _unauthorized(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Modern Network Admin"')
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"auth required")
    def authorized(self):
        header = self.headers.get("Authorization", "")
        if not header.startswith("Basic "):
            return False
        try:
            decoded = base64.b64decode(header.split(" ", 1)[1]).decode("utf-8")
            user, pw = decoded.split(":", 1)
        except Exception:
            return False
        return user == ADMIN_USER and pw == ADMIN_PASSWORD
    def _json(self, code, payload):
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
    def do_GET(self):
        if not self.authorized():
            return self._unauthorized()
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            body = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if path == "/api/status":
            return self._json(200, status_payload())
        self._json(404, {"error": "not found"})
    def do_POST(self):
        if not self.authorized():
            return self._unauthorized()
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return self._json(400, {"error": "bad json"})
        if path == "/api/command":
            server = data.get("server", "survival")
            command = (data.get("command") or "").strip()
            if server not in HOSTS:
                return self._json(400, {"error": "unknown server"})
            if not command:
                return self._json(400, {"error": "empty command"})
            try:
                output = rcon(server, command)
                return self._json(200, {"output": output or "(ok)"})
            except Exception as exc:
                return self._json(502, {"error": str(exc)})
        self._json(404, {"error": "not found"})

if __name__ == "__main__":
    httpd = ThreadingHTTPServer(("0.0.0.0", LISTEN), Handler)
    print(f"Admin panel on :{LISTEN}  user={ADMIN_USER}")
    httpd.serve_forever()
