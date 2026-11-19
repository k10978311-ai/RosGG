import asyncio
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import ssl
import struct
import threading

CERT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs")
HTTPS_PORT = 443

HOST_IP = "0.0.0.0"          # Listen on all interfaces
LOCAL_SERVER_IP = os.environ.get("ROS_PC_IP", "192.168.100.137")  # match real/server_list_ad.local.txt
HTTP_PORT = 80
GATE_TCP_PORT = 20001
CURRENT_BF_KEY = None
CURRENT_SESSION_U32 = None

# Hosts still alive at NetEase: requests are passed through to the real server (resolved via 8.8.8.8).
PASSTHROUGH_HOSTS = {
    "whoami.nie.easebar.com", "who.nie.easebar.com",
    "sdk-os.mpsdk.easebar.com", "sdk.mpsdk.easebar.com", "mpsdk.easebar.com",
}
_real_ip_cache = {}


def resolve_real(host):
    """Resolve host via public DNS (our own DNS server would answer with the PC IP)."""
    if host in _real_ip_cache:
        return _real_ip_cache[host]
    import socket as s, struct, random
    q = struct.pack(">HHHHHH", random.randint(0, 65535), 0x0100, 1, 0, 0, 0)
    q += b"".join(bytes([len(p)]) + p.encode() for p in host.split(".")) + b"\x00" + struct.pack(">HH", 1, 1)
    sock = s.socket(s.AF_INET, s.SOCK_DGRAM); sock.settimeout(3)
    sock.sendto(q, ("8.8.8.8", 53)); resp = sock.recv(4096); sock.close()
    # take the last A record in the answer section
    ip = None
    i = len(resp) - 1
    for off in range(12, len(resp) - 10):
        if resp[off:off + 4] == b"\x00\x01\x00\x01" and resp[off + 8:off + 10] == b"\x00\x04":
            ip = ".".join(str(b) for b in resp[off + 10:off + 14])
    _real_ip_cache[host] = ip
    return ip


def passthrough(handler, body=None):
    import http.client, socket as s
    host = handler.headers.get("Host").split(":")[0]
    ip = resolve_real(host)
    https = isinstance(handler.connection, ssl.SSLSocket)
    if https:
        conn = http.client.HTTPSConnection(host, 443, timeout=15, context=ssl._create_unverified_context())
        raw = s.create_connection((ip, 443), timeout=15)
        conn.sock = conn._context.wrap_socket(raw, server_hostname=host)
    else:
        conn = http.client.HTTPConnection(ip, 80, timeout=15)
    headers = {k: v for k, v in handler.headers.items() if k.lower() not in ("connection", "accept-encoding")}
    conn.request(handler.command, handler.path, body=body, headers=headers)
    r = conn.getresponse()
    data = r.read()
    print(f"  -> PASSTHROUGH {host} ({ip}) {r.status} {data[:300]!r}")
    handler.send_response(r.status)
    for k, v in r.getheaders():
        if k.lower() not in ("transfer-encoding", "connection", "content-length"):
            handler.send_header(k, v)
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


class RoSMockHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Clean console logging of every incoming request from the game
        print(f"[HTTP {self.command}] Host: {self.headers.get('Host')} | Path: {self.path}")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        ua = self.headers.get("User-Agent", "")
        raw_path = self.path
        if "://" in raw_path:
            after_host = raw_path.split("://", 1)[1]
            path_clean = "/" + after_host.split("/", 1)[1] if "/" in after_host else "/"
        else:
            path_clean = raw_path
        path_clean = path_clean.split("?")[0]
        path_lower = path_clean.lower()

        print(f"[GET] https?={isinstance(self.connection, ssl.SSLSocket)} Host={self.headers.get('Host')} Path={path_clean} UA={ua[:80]}")
        if (self.headers.get("Host") or "").split(":")[0] in PASSTHROUGH_HOSTS:
            print(f"  headers: {dict(self.headers)}")
            return passthrough(self)

        # 0. Static files captured from the real update server (real/ folder)
        static_map = {
            "/pl/h45na_hc": ("h45na_hc", "application/octet-stream"),
            "/pl/npk_version_na_android.plist": ("npk_version_na_android.patched.plist", "text/plain"),
            "/server_list_ad.txt": ("server_list_ad.local.txt", "text/plain"),
            "/notice_pc_hw.txt": ("notice_pc_hw.txt", "text/plain"),
        }
        route = static_map.get(path_clean)
        if route:
            fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "real", route[0])
            with open(fpath, "rb") as f:
                body = f.read()
            print(f"  -> Serving real/{route[0]} ({len(body)} bytes)")
            self.send_response(200)
            self.send_header("Content-Type", route[1])
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # 1. Catch file_list_res requests (no extra patch resource files needed)
        if "file_list" in path_lower:
            self.send_response(404)
            self.end_headers()
            return

        # 2. Catch Patch List / Version Check Requests
        if "patch" in path_lower or "version" in path_lower or "update" in path_lower:
            print(f"  -> Serving Mock Patch Manifest (Up-to-date) for {path_clean}")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            patch_response = {
                "code": 200,
                "status": 0,
                "need_update": False,
                "latest_version": "1.610637.617289",
                "engine_version": "1.610637",
                "res_version": "617289",
                "patch_list": [],
                "filelist": []
            }
            self.wfile.write(json.dumps(patch_response).encode("utf-8"))
            return

        # 3. Catch Server List Requests
        if "server_list" in path_lower or "serverlist" in path_lower:
            fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "real", "server_list_ad.local.txt")
            print(f"  -> Serving Text Server List from {fpath}")
            with open(fpath, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # 4. Default Catch-All (UniSDK / Announcements / Notices)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"code": 200, "status": 1, "msg": "OK"}).encode("utf-8"))

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len)
        host = (self.headers.get("Host") or "").split(":")[0]

        # Forge login success: NetEase's live server returns 1003 "service stopped" (guest)
        # or 2003 "User does not exist" (auto-login sdk_token re-validation).
        if host.endswith("mpsdk.easebar.com") and "/users/login/" in self.path:
            import time as _t
            uid = "9000000001"
            forged = {
                "code": 0, "alert_type": 0, "msg": "ok",
                "user": {
                    "id": uid, "token": "localguesttoken0001",
                    "username": "GuestLocal", "nickname": "GuestLocal",
                    "login_channel": "guest", "login_type": 7, "is_guest": True,
                    "is_bind": False, "avatar": "", "pc_ext_info": "",
                    "create_time": int(_t.time()),
                },
                "config": {},
            }
            body = json.dumps(forged).encode()
            print(f"[FORGE guest-login] -> {body[:200]!r}")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if host in PASSTHROUGH_HOSTS:
            print(f"[POST passthrough] {self.headers.get('Host')}{self.path} body={post_body[:300]!r}")
            return passthrough(self, post_body)
        print(f"[HTTP POST] Host: {self.headers.get('Host')} | Path: {self.path} | Body: {post_body[:200]}")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        # Mock UniSDK Token / Login Verification
        auth_response = {
            "code": 200,
            "status": 1,
            "uid": "100001",
            "token": "local_mock_token_123456",
            "username": "LocalPlayer"
        }
        self.wfile.write(json.dumps(auth_response).encode("utf-8"))


# Asyncio Raw TCP Listener for the NeoX Gate/Lobby Connection
async def handle_gate_client(reader, writer):
    addr = writer.get_extra_info('peername')
    port = writer.get_extra_info('sockname')[1]
    print(f"\n[TCP GATE:{port}] Connection from {addr}")
    root = os.path.dirname(os.path.abspath(__file__))
    tcp_log = os.path.join(root, "tcp_gate_capture.bin")
    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break
            print(f"[TCP GATE:{port}] {len(data)}B: {data[:128].hex()}{'...' if len(data)>128 else ''}")
            with open(tcp_log, "ab") as f:
                f.write(struct.pack("<H", len(data)))
                f.write(data)
            # Stay open; real gate handshake TBD (see tcp_gate_capture.bin). Optional no-op ack:
            if os.environ.get("TCP_GATE_ECHO", "off") == "on":
                writer.write(data)
                await writer.drain()
    except Exception as e:
        print(f"[TCP GATE:{port}] error: {e}")
    finally:
        print(f"[TCP GATE:{port}] closed {addr}")
        writer.close()

class GateUDP(asyncio.DatagramProtocol):
    def __init__(self, port):
        self.port = port
        self._login_replied = {}   # addr -> True, to track post-login packets
        self._server_seq = 0
        self._base_player_created = False
        self._heartbeat_task = None
        self._heartbeat_addr = None
        self._probe_replied = set()
        self._summarised = False

    def connection_made(self, transport):
        self.transport = transport

    async def _heartbeat_loop(self, addr, bf_key):
        import time as _t, loginapp
        game_time = 100
        while True:
            await asyncio.sleep(0.5)
            try:
                game_time += 5
                header = struct.pack("<H", 0x0008)
                msg_time = b"\x02" + struct.pack("<I", game_time)
                cleartext = header + msg_time
                pad_len = 8 - (len(cleartext) % 8) or 8
                padded = cleartext + b"\x00" * (pad_len - 1) + bytes([pad_len])
                enc = loginapp.custom_bf_encrypt(bytes(bf_key), padded)
                self.transport.sendto(enc, addr)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"      [HEARTBEAT ERR] {e}")

    def datagram_received(self, data, addr):
        import time as _t
        is_login = data[:4] == b"\x01\x00\x00\x84"

        if is_login:
            print(f"[UDP GATE:{self.port}] LOGIN from {addr} {len(data)}B seq={data[5:7].hex()}")
        else:
            print(f"[UDP GATE:{self.port}] NON-LOGIN from {addr} {len(data)}B: {data.hex()}")

        # Always capture to gate_capture.bin
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gate_capture.bin"), "ab") as f:
            f.write(data)

        # --- Login reply handler ---
        reply_variant_env = os.environ.get("REPLY_VARIANT", "24")
        if self.port == 25000 and is_login and reply_variant_env != "off":
            try:
                import loginapp, importlib
                importlib.reload(loginapp)
                if reply_variant_env != "sweep":
                    msgid = int(reply_variant_env)
                else:
                    sf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sweep_msgid.txt")
                    try:
                        msgid = int(open(sf).read().strip())
                    except Exception:
                        msgid = 0
                    with open(sf, "w") as fh:
                        fh.write(str((msgid + 1) & 0xFF))
                res = loginapp.build_reply(data, LOCAL_SERVER_IP, 25000, msgid)
                if res:
                    global CURRENT_BF_KEY
                    pkt, params, bf = res
                    global CURRENT_SESSION_U32
                    CURRENT_BF_KEY = bf
                    CURRENT_SESSION_U32 = loginapp.extract_session_u32(params)
                    if bf:
                        try:
                            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "latest_bf_key.bin"), "wb") as f:
                                f.write(bf)
                        except Exception:
                            pass
                    sk = CURRENT_SESSION_U32.hex()
                    print(f"  [{_t.strftime('%H:%M:%S')}] [LOGIN] TRY msgid={msgid} (0x{msgid:02x}) -> {len(pkt)}B: {pkt.hex()}")
                    print(f"      user={params.get('username')} session_u32={sk} rest={params.get('rest',b'').hex()} bf={bf.hex() if bf else None}")
                    self.transport.sendto(pkt, addr)
                    self._login_replied[addr] = True
                    self._server_seq = 0
                    self._base_player_created = False
                    self._probe_replied = set()
                    self._summarised = False
                    if self._heartbeat_task and not self._heartbeat_task.done():
                        self._heartbeat_task.cancel()
                        self._heartbeat_task = None
            except Exception as e:
                import traceback
                print(f"  [REPLY ERROR] {e}\n{traceback.format_exc()}")
            return

        # --- BaseApp Mercury channel handler ---
        if self.port == 25000 and not is_login:
            ts = _t.strftime('%H:%M:%S')
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "baseapp_capture.bin"), "ab") as f:
                f.write(len(data).to_bytes(2, 'little') + data)

            try:
                import loginapp
                bf_key = CURRENT_BF_KEY
                if not bf_key:
                    try:
                        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "latest_bf_key.bin"), "rb") as f:
                            bf_key = f.read().strip()
                    except Exception:
                        bf_key = bytes.fromhex("aa6a4a51")

                session_key = CURRENT_SESSION_U32
                if not session_key or len(session_key) != 4:
                    session_key = struct.pack("<I", 0x11223344)

                def _send_enc(addr, cleartext, label):
                    pad_len = 8 - (len(cleartext) % 8) or 8
                    padded = cleartext + b"\x00" * (pad_len - 1) + bytes([pad_len])
                    enc = loginapp.custom_bf_encrypt(bytes(bf_key), padded)
                    self.transport.sendto(enc, addr)
                    print(f"  [{ts}] [BASEAPP SEND] {label} ({len(enc)}B)")

                # Cleartext baseAppLogin probe — single 0xFF reply per reply_id
                if data[:4] == b"\x01\x00\x00\x0b":
                    probe = loginapp.parse_baseapp_login_probe(data)
                    if not probe:
                        return
                    reply_ids = []
                    if probe["reply_id"] not in (b"\x00\x00\x00\x00",):
                        reply_ids.append(probe["reply_id"])
                    if b"\x01\x00\x00\x00" not in reply_ids:
                        reply_ids.append(b"\x01\x00\x00\x00")
                    for rid in reply_ids:
                        if rid in self._probe_replied:
                            continue
                        stub = bytearray(data)
                        stub[7:11] = rid
                        enc_reply = loginapp.build_baseapp_probe_reply_encrypted(
                            stub, bytes(bf_key), session_key
                        )
                        if enc_reply:
                            self.transport.sendto(enc_reply, addr)
                            self._probe_replied.add(rid)
                            print(
                                f"  [{ts}] [BASEAPP LOGIN REPLY] 0xFF reply_id={rid.hex()} "
                                f"sess={session_key.hex()}"
                            )
                    return

                # Cleartext on-channel identify (authenticate + identifyVersionPoint), no 0xFF
                if len(data) % 8 != 0:
                    wrapped = data if data[:2] == b"\x08\x00" else (b"\x08\x00" + data if data[:1] == b"\x01" else None)
                    if wrapped and not self._summarised:
                        ident = loginapp.extract_identify_version_point(wrapped)
                        if ident:
                            summarise = loginapp.build_summarise_version_point(ident)
                            _send_enc(addr, struct.pack("<H", 0x0018) + summarise, "summariseVersionPoint")
                            self._summarised = True
                            return

                # Encrypted BaseApp traffic (channel established)
                if len(data) % 8 == 0:
                    pt = loginapp.custom_bf_decrypt(bytes(bf_key), data)
                    wastage = pt[-1]
                    if wastage <= 8:
                        pkt = bytes(pt[:-wastage])
                    else:
                        pkt = bytes(pt)
                else:
                    pkt = data
                
                flags = struct.unpack("<H", pkt[:2])[0]
                print(f"  [{ts}] [BASEAPP RECV] {len(pkt)}B flags=0x{flags:04x} pt={pkt.hex()}")
                
                # Unpack Mercury footers from end of packet:
                off = len(pkt)
                n_acks = 0
                acks = []
                if flags & 0x0004:  # HAS_ACKS
                    n_acks = pkt[off - 1]
                    off -= 1
                    for _ in range(n_acks):
                        ack = struct.unpack("<I", pkt[off - 4 : off])[0]
                        acks.append(ack)
                        off -= 4
                
                client_seq = None
                if flags & 0x0040:  # HAS_SEQUENCE
                    client_seq = struct.unpack("<I", pkt[off - 4 : off])[0]
                    off -= 4
                
                body_in = pkt[2:off]
                print(f"      [BASEAPP] client_seq={client_seq} acks={acks} body={body_in.hex()}")

                ident = loginapp.extract_identify_version_point(pkt)
                if ident and not self._summarised:
                    summarise = loginapp.build_summarise_version_point(ident)
                    _send_enc(addr, struct.pack("<H", 0x0018) + summarise, "summariseVersionPoint (enc path)")
                    self._summarised = True

                # If BasePlayer has not been created yet for this session:
                if not self._base_player_created:
                    entity_type = int(os.environ.get("BASE_ENTITY_TYPE", "1"))
                    msg_reset = b"\x03\x00"
                    msg_time = b"\x02" + struct.pack("<I", 100)
                    msg_create = (
                        b"\x04"
                        + struct.pack("<H", 6)
                        + struct.pack("<I", 10001)
                        + struct.pack("<H", entity_type)
                    )
                    body = msg_reset + msg_time + msg_create
                    header = struct.pack("<H", 0x005c)
                    ack_seq = client_seq if client_seq is not None else 0
                    footer = struct.pack("<I", self._server_seq) + struct.pack("<I", ack_seq) + b"\x01"
                    self._server_seq += 1
                    self._base_player_created = True
                    _send_enc(
                        addr,
                        header + body + footer,
                        f"ClientInterface reset+setGameTime+createBasePlayer type={entity_type} "
                        f"seq={self._server_seq - 1} ack={ack_seq}",
                    )
                    if self._heartbeat_task is None or self._heartbeat_task.done():
                        self._heartbeat_addr = addr
                        loop = asyncio.get_running_loop()
                        self._heartbeat_task = loop.create_task(self._heartbeat_loop(addr, bf_key))
                        print(f"  [{ts}] [BASEAPP HEARTBEAT] Started for {addr}")
                    return

                # Client sent a reliable packet on an established channel:
                if client_seq is not None:
                    header = struct.pack("<H", 0x000c)  # ON_CHANNEL | HAS_ACKS
                    footer = struct.pack("<I", client_seq) + b"\x01"
                    cleartext = header + footer
                    pad_len = 8 - (len(cleartext) % 8) or 8
                    padded = cleartext + b"\x00" * (pad_len - 1) + bytes([pad_len])

                    enc = loginapp.custom_bf_encrypt(bytes(bf_key), padded)
                    self.transport.sendto(enc, addr)
                    print(f"  [{ts}] [BASEAPP SEND] Sent on-channel ACK ({len(enc)}B, ack={client_seq})")
                else:
                    print(f"  [{ts}] [BASEAPP] Client packet unsequenced (acks={acks}), heartbeat active.")
            except Exception as e:
                import traceback
                print(f"  [{ts}] [BASEAPP ERROR] {e}\n{traceback.format_exc()}")


async def start_tcp_gate():
    loop = asyncio.get_event_loop()
    servers = []
    for port in (GATE_TCP_PORT, 25000):   # 25000 = game server port from server_list_ad.txt
        servers.append(await asyncio.start_server(handle_gate_client, HOST_IP, port))
        print(f"[*] NeoX TCP Gate Listener started on {HOST_IP}:{port}")
        await loop.create_datagram_endpoint(lambda p=port: GateUDP(p), local_addr=(HOST_IP, port))
        print(f"[*] NeoX UDP Gate Listener started on {HOST_IP}:{port}")
    await asyncio.gather(*(s.serve_forever() for s in servers))

def start_http_server():
    httpd = ThreadingHTTPServer((HOST_IP, HTTP_PORT), RoSMockHTTPHandler)
    print(f"[*] HTTP Patch/UniSDK Listener started on {HOST_IP}:{HTTP_PORT}")
    httpd.serve_forever()


class Stub8080Handler(BaseHTTPRequestHandler):
    """Minimal OK stub so UniSDK JNI stops blocking on PC:8080 ConnectException."""

    def log_message(self, fmt, *args):
        print(f"[HTTP:8080] {self.address_string()} {fmt % args}")

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"code":0,"status":"ok"}')

    def do_POST(self):
        self.do_GET()


def start_stub_8080():
    if os.environ.get("STUB_8080", "on") != "on":
        return
    httpd = ThreadingHTTPServer((HOST_IP, 8080), Stub8080Handler)
    print(f"[*] UniSDK stub HTTP on {HOST_IP}:8080 (STUB_8080=off to disable)")
    httpd.serve_forever()


class LoggingTLSServer(ThreadingHTTPServer):
    """HTTPS server that logs handshake failures (e.g. client rejected our cert)."""
    def handle_error(self, request, client_address):
        import sys
        err = sys.exc_info()[1]
        print(f"[HTTPS] {client_address[0]} error: {type(err).__name__}: {err}")


def start_https_server():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(os.path.join(CERT_DIR, "server_chain.crt"), os.path.join(CERT_DIR, "server.key"))

    def sni_cb(sslobj, server_name, _ctx):
        print(f"[HTTPS] TLS ClientHello SNI={server_name}")
    ctx.sni_callback = sni_cb

    httpd = LoggingTLSServer((HOST_IP, HTTPS_PORT), RoSMockHTTPHandler, bind_and_activate=True)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True, do_handshake_on_connect=True)
    print(f"[*] HTTPS Listener started on {HOST_IP}:{HTTPS_PORT}")
    httpd.serve_forever()


if __name__ == "__main__":
    import functools, builtins
    builtins.print = functools.partial(builtins.print, flush=True)  # unbuffered logs
    threading.Thread(target=start_http_server, daemon=True).start()
    threading.Thread(target=start_https_server, daemon=True).start()
    threading.Thread(target=start_stub_8080, daemon=True).start()
    import time
    while True:
        try:
            asyncio.run(start_tcp_gate())
        except Exception as e:
            import traceback
            print(f"[TCP/UDP GATE CRASH] {e}\n{traceback.format_exc()}")
            time.sleep(1)