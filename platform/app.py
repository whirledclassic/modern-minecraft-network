#!/usr/bin/env python3
from __future__ import annotations
import base64, json, os, re, secrets, socket, struct, threading, time, uuid
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote
ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
TEMPLATES = ROOT / "templates"
HOSTS = {"lobby": (os.environ.get("LOBBY_RCON_HOST", "lobby"), int(os.environ.get("LOBBY_RCON_PORT", "25575"))), "survival": (os.environ.get("SURVIVAL_RCON_HOST", "survival"), int(os.environ.get("SURVIVAL_RCON_PORT", "25575")))}
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
    {"id": "vip", "name": "VIP", "price_cents": 499, "period": "30 days", "days": 30, "group": "vip", "tag": "Start here", "perks": ["[VIP] prefix", "3 homes", "Daily food kit"]},
    {"id": "elite", "name": "Elite", "price_cents": 999, "period": "30 days", "days": 30, "group": "elite", "tag": "Best value", "perks": ["Everything in VIP", "6 homes", "Elite prefix"]},
    {"id": "champion", "name": "Champion", "price_cents": 1499, "period": "30 days", "days": 30, "group": "champion", "tag": "Prestige", "perks": ["Everything in Elite", "12 homes", "Gold prefix"]},
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
    tmp = path.with_suffix(".tmp"); tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8"); tmp.replace(path)
def rcon(server, command, timeout=5.0):
    host, port = HOSTS[server]
    sock = socket.create_connection((host, port), timeout=timeout); sock.settimeout(timeout)
    try:
        def packet(kind, body, pid):
            payload = struct.pack("<ii", pid, kind) + body.encode("utf-8") + b"\x00\x00"
            return struct.pack("<i", len(payload)) + payload
        def read():
            header = b""
            while len(header) < 4:
                chunk = sock.recv(4 - len(header))
                if not chunk: raise ConnectionError("RCON closed")
                header += chunk
            (length,) = struct.unpack("<i", header)
            data = b""
            while len(data) < length:
                chunk = sock.recv(length - len(data))
                if not chunk: raise ConnectionError("RCON closed")
                data += chunk
            pid, kind = struct.unpack("<ii", data[:8])
            return pid, kind, data[8:-2].decode("utf-8", errors="replace")
        sock.sendall(packet(3, RCON_PASSWORD, next_id()))
        pid, _, _ = read()
        if pid == -1: raise PermissionError("RCON auth failed")
        sock.sendall(packet(2, command, next_id()))
        _, _, body = read()
        return body.strip()
    finally:
        sock.close()
def parse_list(raw):
    names = []; online = max_p = 0
    m = re.search(r"(\d+)\s+of\s+a\s+max\s+of\s+(\d+)", raw, re.I)
    if m: online, max_p = int(m.group(1)), int(m.group(2))
    if ":" in raw: names = [n.strip() for n in raw.split(":", 1)[1].split(",") if n.strip()]
    return {"online": online or len(names), "max": max_p, "players": names}
def status_payload():
    out = {"ok": True, "name": SERVER_NAME, "join": JOIN_HOST, "servers": {}}; total = 0
    for name in HOSTS:
        try:
            listed = parse_list(rcon(name, "list"))
            out["servers"][name] = {"ok": True, **listed}; total += listed["online"]
        except Exception as exc:
            out["servers"][name] = {"ok": False, "error": str(exc), "players": [], "online": 0, "max": 0}; out["ok"] = False
    out["online"] = total; return out
def product(sku):
    return next((p for p in CATALOG if p["id"] == sku), None)
def valid_name(name):
    return bool(re.fullmatch(r"\.?[A-Za-z0-9_]{3,16}", name or ""))
def fulfill(order):
    sku = product(order["sku"]); player = order["player"]; logs = []
    group = sku.get("group") if sku else None
    commands = [f"lp user {player} parent add {group}", f"say {player} joined the {sku['name']} membership."] if group else []
    for server in HOSTS:
        for cmd in commands:
            try: logs.append(f"{server}: {cmd} -> {rcon(server, cmd)}")
            except Exception as exc: logs.append(f"{server}: {cmd} FAIL {exc}")
    members = load_json(MEMBERS_FILE, {})
    expires = iso(now() + timedelta(days=int(sku["days"]))) if sku and sku.get("days") else None
    members[player.lower()] = {"player": player, "sku": order["sku"], "group": group, "started": iso(now()), "expires": expires, "order_id": order["id"]}
    save_json(MEMBERS_FILE, members); return logs
def expire_loop():
    while True:
        time.sleep(3600)
        members = load_json(MEMBERS_FILE, {}); changed = False
        for rec in members.values():
            exp = rec.get("expires")
            if not exp: continue
            try: when = datetime.fromisoformat(exp)
            except Exception: continue
            if when <= now() and not rec.get("expired"):
                if rec.get("group") and rec.get("player"):
                    for server in HOSTS:
                        try: rcon(server, f"lp user {rec['player']} parent remove {rec['group']}")
                        except Exception: pass
                rec["expired"] = True; changed = True
        if changed: save_json(MEMBERS_FILE, members)
def render_template(name):
    path = TEMPLATES / name
    html = path.read_text(encoding="utf-8") if path.exists() else "<h1>missing</h1>"
    return html.replace("__NAME__", SERVER_NAME).replace("__JOIN__", JOIN_HOST)
MIME = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg"}
class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.address_string(), fmt % args))
    def _send(self, code, body, ctype):
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def _json(self, code, payload):
        self._send(code, json.dumps(payload).encode(), "application/json")
    def authorized(self):
        header = self.headers.get("Authorization", "")
        if not header.startswith("Basic "): return False
        try:
            decoded = base64.b64decode(header.split(" ", 1)[1]).decode(); user, pw = decoded.split(":", 1)
        except Exception:
            return False
        return user == ADMIN_USER and pw == ADMIN_PASSWORD
    def need_admin(self):
        if self.authorized(): return True
        self.send_response(401); self.send_header("WWW-Authenticate", 'Basic realm="console"'); self.end_headers(); return False
    def body_json(self):
        length = int(self.headers.get("Content-Length", "0")); raw = self.rfile.read(length) if length else b"{}"
        try: return json.loads(raw.decode() or "{}")
        except json.JSONDecodeError: return {}
    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path in ("/", "/index.html"):
            return self._send(200, render_template("index.html").encode(), "text/html; charset=utf-8")
        if path in ("/console", "/admin"):
            if not self.need_admin(): return
            return self._send(200, render_template("console.html").encode(), "text/html; charset=utf-8")
        if path.startswith("/static/"):
            target = (STATIC / path[len("/static/"):]).resolve()
            if not str(target).startswith(str(STATIC.resolve())) or not target.is_file():
                return self._json(404, {"error": "not found"})
            return self._send(200, target.read_bytes(), MIME.get(target.suffix.lower(), "application/octet-stream"))
        if path == "/api/status": return self._json(200, status_payload())
        if path == "/api/store/catalog": return self._json(200, {"currency": CURRENCY, "demo": DEMO_PAYMENTS, "products": CATALOG})
        if path == "/api/store/orders":
            if not self.need_admin(): return
            return self._json(200, {"orders": load_json(ORDERS_FILE, [])})
        if path == "/api/store/members":
            if not self.need_admin(): return
            return self._json(200, {"members": load_json(MEMBERS_FILE, {})})
        if path == "/healthz": return self._json(200, {"ok": True})
        self._json(404, {"error": "not found"})
    def do_POST(self):
        path = urlparse(self.path).path; data = self.body_json()
        if path == "/api/store/checkout":
            sku = product(data.get("sku", "")); player = (data.get("player") or "").strip()
            if not sku: return self._json(400, {"error": "unknown plan"})
            if not valid_name(player): return self._json(400, {"error": "Use the name from /list. Bedrock often starts with a dot."})
            order = {"id": str(uuid.uuid4()), "player": player, "sku": sku["id"], "amount_cents": sku["price_cents"], "currency": CURRENCY, "status": "pending", "created": iso(now())}
            if DEMO_PAYMENTS: order["demo"] = True; order["demo_token"] = secrets.token_urlsafe(12)
            orders = load_json(ORDERS_FILE, []); orders.insert(0, order); save_json(ORDERS_FILE, orders)
            public = {k: order[k] for k in ("id", "player", "sku", "amount_cents", "status", "demo") if k in order}
            if DEMO_PAYMENTS: public["demo_token"] = order["demo_token"]
            return self._json(200, public)
        if path == "/api/store/demo-pay":
            if not DEMO_PAYMENTS: return self._json(403, {"error": "demo off"})
            orders = load_json(ORDERS_FILE, []); order = next((o for o in orders if o.get("id") == data.get("order_id")), None)
            if not order or data.get("token") != order.get("demo_token"): return self._json(403, {"error": "bad order"})
            order["status"] = "paid"; order["paid"] = iso(now()); save_json(ORDERS_FILE, orders)
            return self._json(200, {"ok": True, "logs": fulfill(order)})
        if path == "/api/store/fulfill":
            if not self.need_admin(): return
            orders = load_json(ORDERS_FILE, []); order = next((o for o in orders if o.get("id") == data.get("order_id")), None)
            if not order: return self._json(404, {"error": "missing"})
            order["status"] = "paid"; order["paid"] = iso(now()); save_json(ORDERS_FILE, orders)
            return self._json(200, {"ok": True, "logs": fulfill(order)})
        if path == "/api/command":
            if not self.need_admin(): return
            server = data.get("server", "survival"); command = (data.get("command") or "").strip()
            if server not in HOSTS or not command: return self._json(400, {"error": "bad command"})
            try: return self._json(200, {"output": rcon(server, command) or "(ok)"})
            except Exception as exc: return self._json(502, {"error": str(exc)})
        self._json(404, {"error": "not found"})
if __name__ == "__main__":
    threading.Thread(target=expire_loop, daemon=True).start()
    print(f"Platform on :{LISTEN}")
    ThreadingHTTPServer(("0.0.0.0", LISTEN), Handler).serve_forever()
