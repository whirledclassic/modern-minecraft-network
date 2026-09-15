#!/usr/bin/env python3
from __future__ import annotations
import base64, json, os, re, secrets, socket, struct, threading, time, uuid
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

HOSTS = {
    "lobby": (os.environ.get("LOBBY_RCON_HOST", "lobby"), int(os.environ.get("LOBBY_RCON_PORT", "25575"))),
    "survival": (os.environ.get("SURVIVAL_RCON_HOST", "survival"), int(os.environ.get("SURVIVAL_RCON_PORT", "25575"))),
}
RCON_PASSWORD = os.environ.get("RCON_PASSWORD", "change-me")
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")
DEMO_PAYMENTS = os.environ.get("DEMO_PAYMENTS", "true").lower() in ("1", "true", "yes")
SERVER_NAME = os.environ.get("SERVER_NAME", "Modern Network")
JOIN_HOST = os.environ.get("JOIN_HOST", "localhost")
CURRENCY = os.environ.get("STORE_CURRENCY", "USD")
LISTEN = int(os.environ.get("PLATFORM_PORT", "8080"))
DATA = Path(os.environ.get("DATA_DIR", "/data")); DATA.mkdir(parents=True, exist_ok=True)
ORDERS_FILE = DATA / "orders.json"
MEMBERS_FILE = DATA / "members.json"
CATALOG = [
    {"id": "vip", "name": "VIP", "price_cents": 499, "period": "30 days", "days": 30, "group": "vip", "tag": "Most picked", "perks": ["Colored chat", "3 homes", "VIP prefix", "Queue priority"]},
    {"id": "elite", "name": "Elite", "price_cents": 999, "period": "30 days", "days": 30, "group": "elite", "tag": "Best value", "perks": ["Everything in VIP", "6 homes", "Elite kit", "Purple prefix"]},
    {"id": "champion", "name": "Champion", "price_cents": 2499, "period": "lifetime", "days": 0, "group": "champion", "tag": "Lifetime", "perks": ["Everything in Elite", "12 homes", "Champion kit", "Gold prefix"]},
]
_lock = threading.Lock(); _req_id = 1
def now():
    return datetime.now(timezone.utc)
def iso(dt):
    return dt.isoformat() if dt else None
def next_id():
    global _req_id
    with _lock:
        _req_id += 1
        return _req_id
def load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default
def save_json(path, payload):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)
def rcon(server, command, timeout=5.0):
    host, port = HOSTS[server]
    sock = socket.create_connection((host, port), timeout=timeout)
    sock.settimeout(timeout)
    try:
        def packet(kind, body, pid):
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
            return pid, kind, data[8:-2].decode("utf-8", errors="replace")
        sock.sendall(packet(3, RCON_PASSWORD, next_id()))
        pid, _, _ = read()
        if pid == -1:
            raise PermissionError("RCON auth failed")
        sock.sendall(packet(2, command, next_id()))
        _, _, body = read()
        return body.strip()
    finally:
        sock.close()
def parse_list(raw):
    names = []; online = max_p = 0
    m = re.search(r"(\d+)\s+of\s+a\s+max\s+of\s+(\d+)", raw, re.I)
    if m:
        online, max_p = int(m.group(1)), int(m.group(2))
    if ":" in raw:
        names = [n.strip() for n in raw.split(":", 1)[1].split(",") if n.strip()]
    return {"online": online or len(names), "max": max_p, "players": names}
def status_payload():
    out = {"ok": True, "name": SERVER_NAME, "join": JOIN_HOST, "servers": {}}
    total = 0
    for name in HOSTS:
        try:
            listed = parse_list(rcon(name, "list"))
            out["servers"][name] = {"ok": True, **listed}
            total += listed["online"]
        except Exception as exc:
            out["servers"][name] = {"ok": False, "error": str(exc), "players": [], "online": 0, "max": 0}
            out["ok"] = False
    out["online"] = total
    return out
def product(sku):
    return next((p for p in CATALOG if p["id"] == sku), None)
def valid_name(name):
    return bool(re.fullmatch(r"[A-Za-z0-9_]{3,16}", name or ""))
def fulfill(order):
    sku = product(order["sku"]); player = order["player"]; logs = []
    group = sku.get("group") if sku else None
    commands = []
    if group:
        commands += [f"lp user {player} parent add {group}", f"say {player} joined the {sku['name']} membership."]
    for server in HOSTS:
        for cmd in commands:
            try:
                logs.append(f"{server}: {cmd} -> {rcon(server, cmd)}")
            except Exception as exc:
                logs.append(f"{server}: {cmd} FAIL {exc}")
    members = load_json(MEMBERS_FILE, {})
    expires = iso(now() + timedelta(days=int(sku["days"]))) if sku and sku.get("days") else None
    members[player.lower()] = {"player": player, "sku": order["sku"], "group": group, "started": iso(now()), "expires": expires, "order_id": order["id"]}
    save_json(MEMBERS_FILE, members)
    return logs
def expire_loop():
    while True:
        time.sleep(3600)
        members = load_json(MEMBERS_FILE, {})
        changed = False
        for rec in members.values():
            exp = rec.get("expires")
            if not exp:
                continue
            try:
                when = datetime.fromisoformat(exp)
            except Exception:
                continue
            if when <= now() and not rec.get("expired"):
                if rec.get("group") and rec.get("player"):
                    for server in HOSTS:
                        try:
                            rcon(server, f"lp user {rec['player']} parent remove {rec['group']}")
                        except Exception:
                            pass
                rec["expired"] = True
                changed = True
        if changed:
            save_json(MEMBERS_FILE, members)

SITE = """<!DOCTYPE html><html><head><meta charset='utf-8'/><meta name='viewport' content='width=device-width,initial-scale=1'/><title>__NAME__</title>
<style>
:root{--bg:#07080f;--line:#23283a;--text:#eef3ff;--muted:#93a0bb;--accent:#3ee0c9;--gold:#f4c46b}
*{box-sizing:border-box}body{margin:0;font-family:ui-sans-serif,system-ui,sans-serif;background:radial-gradient(1000px 500px at 0% -10%,#16343c 0%,transparent 45%),#07080f;color:var(--text)}
a{color:var(--accent);text-decoration:none}header,footer{max-width:1100px;margin:auto;padding:22px 20px;display:flex;justify-content:space-between;align-items:center;gap:12px}
nav{display:flex;gap:16px}nav a{color:var(--muted)}.hero{max-width:1100px;margin:auto;padding:28px 20px 10px}
.hero h1{font-size:clamp(36px,7vw,72px);line-height:.95;margin:0 0 12px}.hero p{color:var(--muted);max-width:640px;font-size:18px}
.row{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}.btn{background:linear-gradient(180deg,#4af0d6,#1fb8a5);color:#041210;border:0;border-radius:12px;padding:12px 16px;font-weight:800;cursor:pointer}
.btn.ghost{background:transparent;color:var(--text);border:1px solid var(--line)}.ip{font-family:ui-monospace,monospace;background:#0b0e16;border:1px solid var(--line);padding:12px 14px;border-radius:12px}
.grid{max-width:1100px;margin:auto;padding:10px 20px 40px;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.card{background:rgba(16,19,29,.9);border:1px solid var(--line);border-radius:18px;padding:18px}.price{font-size:28px;margin:8px 0}
.tag{color:var(--gold);font-size:12px;letter-spacing:.08em;text-transform:uppercase}ul{color:var(--muted)}
input{width:100%;background:#0b0e16;color:var(--text);border:1px solid var(--line);border-radius:12px;padding:10px 12px;margin:6px 0}
.ok{color:#3ee07a}.bad{color:#ff5d73}footer{color:var(--muted);font-size:13px}
</style></head><body>
<header><strong>__NAME__</strong><nav><a href='#play'>Play</a><a href='#store'>Memberships</a><a href='/console'>Console</a></nav></header>
<section class='hero'><h1>One IP.<br>Lobby. Survival.<br>Java + Bedrock.</h1>
<p>Land in the hub, jump into survival, and unlock memberships from this site. The store talks to the live servers and grants ranks automatically.</p>
<div class='row'><div class='ip'>Java __JOIN__:25565 · Bedrock UDP 19132</div><a class='btn' href='#store'>Get membership</a></div>
<p id='live' style='margin-top:16px;color:#93a0bb'>Checking servers…</p></section>
<section class='grid' id='play'>
<div class='card'><h3>Lobby</h3><p>Selector hub, flight, always day.</p><div id='lobby-stat'>—</div></div>
<div class='card'><h3>Survival</h3><p>Claims, homes, rollback. Rank perks apply here.</p><div id='survival-stat'>—</div></div>
<div class='card'><h3>Join</h3><p>Java Multiplayer → Direct. Bedrock port 19132. Then <code>/server survival</code>.</p></div>
</section>
<section class='hero' id='store'><h1>Memberships</h1><p>Buy a rank here. Demo checkout is on until you disable it.</p></section>
<section class='grid' id='plans'></section>
<footer><span>Custom store + membership ledger.</span><a href='/console'>Admin console</a></footer>
<script>
const JOIN='__JOIN__';
async function api(p,o){const r=await fetch(p,Object.assign({headers:{'Content-Type':'application/json'}},o||{}));if(!r.ok)throw new Error(await r.text());return r.json()}
async function boot(){
  try{const s=await api('/api/status');
    document.getElementById('live').innerHTML=s.ok?'<span class=ok>ONLINE</span> · '+(s.online||0)+' playing':'<span class=bad>Servers warming up</span>';
    ['lobby','survival'].forEach(n=>{const d=s.servers[n]||{};document.getElementById(n+'-stat').textContent=d.ok?(d.online+' online'):'offline'});
  }catch(e){document.getElementById('live').textContent='Status unavailable'}
  const catalog=await api('/api/store/catalog');
  document.getElementById('plans').innerHTML=catalog.products.map(p=>`<div class='card'><div class='tag'>${p.tag||''}</div><h3>${p.name}</h3><div class='price'>$${(p.price_cents/100).toFixed(2)} <span style='font-size:14px;color:#93a0bb'>/ ${p.period}</span></div><ul>${p.perks.map(x=>'<li>'+x+'</li>').join('')}</ul><input placeholder='Minecraft username' id='u-${p.id}'/><button class='btn' onclick="buy('${p.id}')">Unlock ${p.name}</button><div id='m-${p.id}' style='margin-top:8px;color:#93a0bb;font-size:13px'></div></div>`).join('');
}
async function buy(sku){
  const player=document.getElementById('u-'+sku).value.trim(); const box=document.getElementById('m-'+sku);
  box.textContent='Creating order…';
  try{
    const order=await api('/api/store/checkout',{method:'POST',body:JSON.stringify({sku,player})});
    if(order.demo){await api('/api/store/demo-pay',{method:'POST',body:JSON.stringify({order_id:order.id,token:order.demo_token})});box.innerHTML='<span class=ok>Paid.</span> Rank granted to <b>'+player+'</b>';return;}
    box.textContent='Order '+order.id.slice(0,8)+' pending. Staff will confirm it in the console.';
  }catch(e){box.innerHTML='<span class=bad>'+e.message+'</span>'}
}
boot();
</script></body></html>"""

CONSOLE = """<!DOCTYPE html><html><head><meta charset='utf-8'/><meta name='viewport' content='width=device-width,initial-scale=1'/><title>Console</title>
<style>
body{margin:0;font-family:ui-sans-serif,system-ui,sans-serif;background:#07080d;color:#e8edf7}
header{display:flex;justify-content:space-between;padding:18px 22px;border-bottom:1px solid #1e2433}
main{display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:18px;max-width:1200px;margin:auto}
.card{background:#10131c;border:1px solid #1e2433;border-radius:16px;padding:16px}
h2{margin:0 0 10px;font-size:13px;color:#8b95ab;letter-spacing:.08em;text-transform:uppercase}
.ok{color:#3ee07a}.bad{color:#ff5d73}input,select{width:100%;background:#0b0e16;color:#e8edf7;border:1px solid #1e2433;border-radius:10px;padding:9px 11px;margin:6px 0}
button{background:#3ee0c9;color:#041210;border:0;border-radius:10px;padding:9px 12px;font-weight:700;cursor:pointer;margin:4px 4px 0 0}
.ghost{background:transparent;color:#e8edf7;border:1px solid #1e2433}pre{background:#0b0e16;border:1px solid #1e2433;border-radius:10px;padding:10px;min-height:120px;overflow:auto;font-size:12px}
.tag{display:inline-block;background:#171c28;border:1px solid #1e2433;padding:3px 8px;border-radius:8px;margin:2px;font-size:12px}
.span2{grid-column:1/-1}@media(max-width:900px){main{grid-template-columns:1fr}}
</style></head><body>
<header><strong>Network console</strong><a href='/' style='color:#3ee0c9'>Public site</a></header>
<main>
<div class='card'><h2>Lobby</h2><div id='lobby-ok'>…</div><div id='lobby-players'></div></div>
<div class='card'><h2>Survival</h2><div id='survival-ok'>…</div><div id='survival-players'></div></div>
<div class='card span2'><h2>Command</h2><select id='target'><option>lobby</option><option>survival</option></select>
<input id='cmd' placeholder='lp user Notch parent add vip'/>
<button onclick='runCmd()'>Send</button><button class='ghost' onclick='quick("list")'>list</button><button class='ghost' onclick='quick("save-all")'>save-all</button>
<pre id='out'>Ready.</pre></div>
<div class='card span2'><h2>Orders</h2><div id='orders'>Loading…</div></div>
<div class='card span2'><h2>Members</h2><div id='members'>Loading…</div></div>
</main>
<script>
async function api(p,o){const r=await fetch(p,Object.assign({headers:{'Content-Type':'application/json'}},o||{}));if(!r.ok)throw new Error(await r.text());return r.json()}
function tags(arr){return (arr||[]).map(x=>'<span class=tag>'+x+'</span>').join('')}
async function refresh(){
  const s=await api('/api/status');
  ['lobby','survival'].forEach(n=>{const d=s.servers[n]||{};document.getElementById(n+'-ok').innerHTML=d.ok?'<span class=ok>ONLINE</span> · '+(d.online||0)+' players':'<span class=bad>DOWN</span>';document.getElementById(n+'-players').innerHTML=tags(d.players)});
  const store=await api('/api/store/orders');
  document.getElementById('orders').innerHTML=store.orders.map(o=>`<div style="margin:8px 0;border-top:1px solid #1e2433;padding-top:8px"><b>${o.player}</b> · ${o.sku} · ${o.status} · ${o.id.slice(0,8)} ${o.status!=='paid'?`<button onclick=\"fulfill('${o.id}')\">Mark paid + grant</button>`:''}</div>`).join('')||'No orders yet.';
  const mem=await api('/api/store/members');
  document.getElementById('members').innerHTML=Object.values(mem.members||{}).map(m=>`<span class=tag>${m.player} · ${m.sku}</span>`).join('')||'No members yet.';
}
async function runCmd(command){const server=document.getElementById('target').value;const cmd=command||document.getElementById('cmd').value;if(!cmd)return;const data=await api('/api/command',{method:'POST',body:JSON.stringify({server,command:cmd})});document.getElementById('out').textContent=data.output||data.error||'(ok)';refresh()}
function quick(c){document.getElementById('cmd').value=c;runCmd(c)}
async function fulfill(id){const data=await api('/api/store/fulfill',{method:'POST',body:JSON.stringify({order_id:id})});document.getElementById('out').textContent=(data.logs||[]).join('\n')||'granted';refresh()}
refresh();setInterval(refresh,5000);
</script></body></html>"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.address_string(), fmt % args))
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
    def _json(self, code, payload):
        self._send(code, json.dumps(payload).encode("utf-8"), "application/json")
    def _html(self, template):
        html = template.replace("__NAME__", SERVER_NAME).replace("__JOIN__", JOIN_HOST)
        self._send(200, html.encode("utf-8"), "text/html; charset=utf-8")
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
    def need_admin(self):
        if self.authorized():
            return True
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Modern Network Console"')
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"auth required")
        return False
    def body_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            return json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return {}
    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            return self._html(SITE)
        if path in ("/console", "/admin"):
            if not self.need_admin():
                return
            return self._html(CONSOLE)
        if path == "/api/status":
            return self._json(200, status_payload())
        if path == "/api/store/catalog":
            return self._json(200, {"currency": CURRENCY, "demo": DEMO_PAYMENTS, "products": CATALOG})
        if path == "/api/store/orders":
            if not self.need_admin():
                return
            return self._json(200, {"orders": load_json(ORDERS_FILE, [])})
        if path == "/api/store/members":
            if not self.need_admin():
                return
            return self._json(200, {"members": load_json(MEMBERS_FILE, {})})
        if path == "/healthz":
            return self._json(200, {"ok": True})
        self._json(404, {"error": "not found"})
    def do_POST(self):
        path = urlparse(self.path).path
        data = self.body_json()
        if path == "/api/store/checkout":
            sku = product(data.get("sku", ""))
            player = (data.get("player") or "").strip()
            if not sku:
                return self._json(400, {"error": "unknown plan"})
            if not valid_name(player):
                return self._json(400, {"error": "Enter a valid Java username (3-16 letters/numbers/_)"})
            order = {"id": str(uuid.uuid4()), "player": player, "sku": sku["id"], "amount_cents": sku["price_cents"], "currency": CURRENCY, "status": "pending", "created": iso(now())}
            if DEMO_PAYMENTS:
                order["demo"] = True
                order["demo_token"] = secrets.token_urlsafe(12)
            orders = load_json(ORDERS_FILE, [])
            orders.insert(0, order)
            save_json(ORDERS_FILE, orders)
            public = {k: order[k] for k in ("id", "player", "sku", "amount_cents", "status", "demo") if k in order}
            if DEMO_PAYMENTS:
                public["demo_token"] = order["demo_token"]
            return self._json(200, public)
        if path == "/api/store/demo-pay":
            if not DEMO_PAYMENTS:
                return self._json(403, {"error": "demo payments disabled"})
            orders = load_json(ORDERS_FILE, [])
            order = next((o for o in orders if o.get("id") == data.get("order_id")), None)
            if not order:
                return self._json(404, {"error": "order not found"})
            if data.get("token") != order.get("demo_token"):
                return self._json(403, {"error": "bad token"})
            order["status"] = "paid"; order["paid"] = iso(now()); order["provider"] = "internal-demo"
            save_json(ORDERS_FILE, orders)
            return self._json(200, {"ok": True, "logs": fulfill(order)})
        if path == "/api/store/fulfill":
            if not self.need_admin():
                return
            orders = load_json(ORDERS_FILE, [])
            order = next((o for o in orders if o.get("id") == data.get("order_id")), None)
            if not order:
                return self._json(404, {"error": "order not found"})
            order["status"] = "paid"; order["paid"] = iso(now()); order["provider"] = "staff"
            save_json(ORDERS_FILE, orders)
            return self._json(200, {"ok": True, "logs": fulfill(order)})
        if path == "/api/command":
            if not self.need_admin():
                return
            server = data.get("server", "survival")
            command = (data.get("command") or "").strip()
            if server not in HOSTS:
                return self._json(400, {"error": "unknown server"})
            if not command:
                return self._json(400, {"error": "empty command"})
            try:
                return self._json(200, {"output": rcon(server, command) or "(ok)"})
            except Exception as exc:
                return self._json(502, {"error": str(exc)})
        self._json(404, {"error": "not found"})

if __name__ == "__main__":
    threading.Thread(target=expire_loop, daemon=True).start()
    print(f"Platform on :{LISTEN}  site=/  console=/console  demo={DEMO_PAYMENTS}")
    ThreadingHTTPServer(("0.0.0.0", LISTEN), Handler).serve_forever()
