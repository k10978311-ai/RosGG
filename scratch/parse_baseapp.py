"""Parse login + post-login Mercury UDP packets from gate_capture.bin (local RosGG copy)."""
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import loginapp  # noqa: E402

LOGIN_MAGIC = b"\x01\x00\x00\x84"
LOGIN_SIZE = 145
PROBE_MAGIC = b"\x01\x00\x00\x0b"


def iter_packets(raw: bytes):
    i = 0
    while i < len(raw):
        if raw[i : i + 4] == LOGIN_MAGIC and i + LOGIN_SIZE <= len(raw):
            yield "LOGIN", i, raw[i : i + LOGIN_SIZE]
            i += LOGIN_SIZE
            continue
        if raw[i : i + 4] == PROBE_MAGIC:
            # probes in capture are 37 bytes apart in a repeating pattern
            chunk = raw[i : i + 64]
            end = chunk.find(LOGIN_MAGIC)
            if end < 0:
                end = min(37, len(raw) - i)
            yield "PROBE", i, raw[i : i + end]
            i += end
            continue
        i += 1


def main():
    path = ROOT / "gate_capture.bin"
    if not path.exists():
        raise SystemExit(f"missing {path}")
    raw = path.read_bytes()
    counts = {"LOGIN": 0, "PROBE": 0}
    last_login = None
    for kind, off, pkt in iter_packets(raw):
        counts[kind] += 1
        if kind == "LOGIN":
            last_login = pkt
            print(
                f"LOGIN @{off:6d} seq={pkt[5:7].hex()} req_id={pkt[5:9].hex()} "
                f"footer_field={pkt[7:11].hex()}"
            )
        else:
            print(f"PROBE @{off:6d} {loginapp.parse_mercury_probe(pkt)}")
            print(f"         hex={pkt.hex()}")
    print(f"\nTotals: {counts}")
    if last_login:
        reply, params, bf = loginapp.build_reply(
            last_login, "192.168.100.137", 25000, 24
        )
        print(f"\nLatest login user={params.get('username')!r} bf={bf.hex() if bf else None}")
        print(f"variant=24 reply ({len(reply)}B): {reply.hex()}")


if __name__ == "__main__":
    main()
