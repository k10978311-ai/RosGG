"""
Raw UDP capture on port 25000 to see EVERYTHING arriving,
including BaseApp channel probes that may not hit our asyncio handler.
Run this in a separate window while triggering PLAY.
"""
import socket, struct, time, sys

print("Listening for ALL UDP on :25000 (raw bind)...")
print("Trigger PLAY now. Press Ctrl+C to stop.\n")

# Bind a raw socket to see all UDP on port 25000
# We'll use a secondary socket (the server already has one, but asyncio may queue-drop)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
except AttributeError:
    pass  # Windows doesn't have SO_REUSEPORT
sock.settimeout(60)
try:
    sock.bind(('0.0.0.0', 25000))
except OSError as e:
    print(f"Can't bind :25000 (server is already there): {e}")
    print("Will use a promiscuous approach instead...")
    sock.close()
    # Try to sniff using raw socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        sock.bind(('192.168.1.18', 0))
        sock.settimeout(60)
        print("Using raw socket (run as admin if no packets appear)")
        raw_mode = True
    except Exception as e2:
        print(f"Raw socket also failed: {e2}")
        sys.exit(1)
    raw_mode = True
else:
    raw_mode = False

start = time.time()
count = 0
try:
    while time.time() - start < 120:
        try:
            data, addr = sock.recvfrom(65535)
            count += 1
            ts = time.strftime('%H:%M:%S')
            if raw_mode:
                # Parse IP+UDP headers
                ip_len = (data[0] & 0xF) * 4
                udp = data[ip_len:]
                src_port = struct.unpack('>H', udp[0:2])[0]
                dst_port = struct.unpack('>H', udp[2:4])[0]
                payload  = udp[8:]
                if dst_port == 25000 or src_port == 25000:
                    print(f"[{ts}] UDP {addr[0]}:{src_port} -> :{dst_port} ({len(payload)}B): {payload.hex()}")
            else:
                is_login = data[:4] == b'\x01\x00\x00\x84'
                label = 'LOGIN' if is_login else '*** NON-LOGIN ***'
                print(f"[{ts}] {label} from {addr} ({len(data)}B): {data.hex()}")
        except socket.timeout:
            print(f"  ... waiting ({count} pkts so far)")
except KeyboardInterrupt:
    pass

print(f"\nTotal: {count} packets")
sock.close()
