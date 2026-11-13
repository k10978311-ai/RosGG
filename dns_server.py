"""Minimal DNS server: answers NetEase/RoS domains with the local PC IP, forwards everything else.

Run on the PC; the emulator's UDP/53 traffic is DNAT'ed here by iptables (see setup_emulator.ps1).
"""
import socket
import struct
import threading
import time

LISTEN = ("0.0.0.0", 53)
LOCAL_IP = "192.168.1.18"
UPSTREAM = ("8.8.8.8", 53)
REDIRECT_SUFFIXES = (
    "easebar.com", "netease.com", "163.com", "126.net", "netease.im",
    "rulesofsurvivalgame.com", "nease.net",
)


def log(msg):
    print(f"{time.strftime('%H:%M:%S')} {msg}", flush=True)


def parse_qname(data, off):
    labels = []
    while True:
        n = data[off]
        off += 1
        if n == 0:
            break
        labels.append(data[off:off + n].decode("ascii", "replace"))
        off += n
    return ".".join(labels).lower(), off


def build_reply(query, qend, qtype, ip):
    tid = query[:2]
    flags = b"\x81\x80"  # standard response, RD+RA, NOERROR
    question = query[12:qend + 4]
    if qtype == 1:  # A
        answer = b"\xc0\x0c" + struct.pack(">HHIH", 1, 1, 30, 4) + socket.inet_aton(ip)
        counts = struct.pack(">HHHH", 1, 1, 0, 0)
    else:  # AAAA / anything else -> empty NOERROR so the client falls back to IPv4
        answer = b""
        counts = struct.pack(">HHHH", 1, 0, 0, 0)
    return tid + flags + counts + question + answer


def forward(sock, data, addr):
    try:
        up = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        up.settimeout(3)
        up.sendto(data, UPSTREAM)
        resp, _ = up.recvfrom(4096)
        sock.sendto(resp, addr)
    except Exception as e:
        log(f"[DNS] upstream error: {e}")
    finally:
        up.close()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(LISTEN)
    log(f"[*] DNS server on {LISTEN[0]}:{LISTEN[1]} -> redirecting {REDIRECT_SUFFIXES} to {LOCAL_IP}")
    while True:
        data, addr = sock.recvfrom(4096)
        try:
            name, off = parse_qname(data, 12)
            qtype = struct.unpack(">H", data[off:off + 2])[0]
        except Exception:
            continue
        if any(name == s or name.endswith("." + s) for s in REDIRECT_SUFFIXES):
            log(f"[DNS] {name} (type {qtype}) -> {LOCAL_IP if qtype == 1 else 'empty'}")
            sock.sendto(build_reply(data, off, qtype, LOCAL_IP), addr)
        else:
            threading.Thread(target=forward, args=(sock, data, addr), daemon=True).start()


if __name__ == "__main__":
    main()
