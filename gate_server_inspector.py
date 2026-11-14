"""Standalone NeoX TCP gate packet inspector (read-only capture + framed ack experiments).

Fast Private-Server in server_list_ad.local.txt uses 192.168.x.x:25000 — same port as
BigWorld Mercury UDP login. For a full harness, keep ros_mock_server.py running (it also
logs TCP to tcp_gate_capture.bin). Use this script when you want verbose console hexdumps
without the mock HTTP/DNS/UDP stack.

  set ROS_PC_IP=192.168.100.137
  python gate_server_inspector.py              # listens 0.0.0.0:25000
  python gate_server_inspector.py --port 20001 # legacy Frida/JSON gate

Env:
  GATE_INSPECT_PORT — default 25000
  GATE_SERVER_HELLO — if 1, send server-first hello on connect timeout
  GATE_FRAMED_ACK   — if 1, send 2-byte length + \\x01\\x00 after each client chunk
"""
from __future__ import annotations

import argparse
import asyncio
import os
import struct
import time

HOST = "0.0.0.0"
CAPTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tcp_gate_inspect.bin")


def hexdump(data: bytes, limit: int = 512) -> str:
    chunk = data[:limit]
    hex_str = " ".join(f"{b:02x}" for b in chunk)
    ascii_str = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
    extra = f"\n     ... +{len(data) - limit} bytes" if len(data) > limit else ""
    return f"HEX:   {hex_str}{extra}\nASCII: {ascii_str}"


def dump_headers(data: bytes) -> None:
    if len(data) >= 2:
        len_u16 = struct.unpack_from("<H", data, 0)[0]
        print(f"     [hdr] uint16_le@0 = {len_u16} (pkt len {len(data)})")
    if len(data) >= 4:
        len_u32 = struct.unpack_from("<I", data, 0)[0]
        print(f"     [hdr] uint32_le@0 = {len_u32}")
    if len(data) >= 6:
        print(f"     [hdr] bytes[2:6] = {data[2:6].hex()}")


async def handle_neox_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    peer = writer.get_extra_info("peername")
    local = writer.get_extra_info("sockname")
    port = local[1] if local else 0
    ts = time.strftime("%H:%M:%S")
    print(f"\n[{ts}] [+] TCP gate connection port={port} from {peer}")

    hello_on_timeout = os.environ.get("GATE_SERVER_HELLO", "0") == "1"
    framed_ack = os.environ.get("GATE_FRAMED_ACK", "0") == "1"
    root = os.path.dirname(os.path.abspath(__file__))

    try:
        try:
            data = await asyncio.wait_for(reader.read(4096), timeout=3.0)
        except asyncio.TimeoutError:
            print("[!] Client silent 3s — server must speak first? (set GATE_SERVER_HELLO=1)")
            if hello_on_timeout:
                hello_pkt = struct.pack("<HB", 1, 0x01)
                writer.write(hello_pkt)
                await writer.drain()
                print(f"[<-] server hello: {hello_pkt.hex()}")
            data = await reader.read(4096)

        while data:
            print(f"\n[->] {len(data)} bytes:")
            print(hexdump(data))
            dump_headers(data)
            with open(CAPTURE, "ab") as f:
                f.write(struct.pack("<H", len(data)))
                f.write(data)

            if framed_ack:
                ack_payload = b"\x01\x00"
                reply = struct.pack("<H", len(ack_payload)) + ack_payload
                writer.write(reply)
                await writer.drain()
                print(f"[<-] framed ack ({len(reply)}B): {reply.hex()}")

            data = await reader.read(4096)

    except Exception as e:
        print(f"[-] {e}")
    finally:
        print(f"[*] closed {peer}")
        writer.close()


async def main() -> None:
    ap = argparse.ArgumentParser(description="NeoX TCP gate inspector")
    ap.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("GATE_INSPECT_PORT", "25000")),
        help="TCP listen port (default 25000 = server_list_ad.local.txt)",
    )
    args = ap.parse_args()

    server = await asyncio.start_server(handle_neox_client, HOST, args.port)
    print(f"[*] RoS TCP gate inspector on {HOST}:{args.port}")
    print(f"    PLAY list uses :25000; primary login is usually UDP Mercury on same port.")
    print(f"    Captures append to {CAPTURE}")
    print(f"    GATE_SERVER_HELLO=1 GATE_FRAMED_ACK=1 for ack experiments")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
