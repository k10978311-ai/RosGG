"""
Check what BaseApp Mercury expects:
- The client decoded address=192.168.1.18 and port=25000
- It then tries to connect a Mercury channel to that address
- 'Unable to connect to BaseApp' means the UDP handshake to :25000 timed out

The client will send a Mercury CREATE_CHANNEL (or similar) packet to 192.168.1.18:25000.
Our :25000 UDP listener just logs and discards. We need to answer the channel creation.

This script monitors the gate_capture.bin for new packets AFTER sending the login reply,
and displays any that arrive on :25000 that aren't login requests.
"""
import struct, socket

with open(r'C:\Users\Lufy\Desktop\Server\gate_capture.bin', 'rb') as f:
    data = f.read()

print(f"gate_capture.bin: {len(data)} bytes total")

# Parse packets - each is a captured datagram. We don't know exact boundaries
# since they're just concatenated. But login requests start with 01 00 00 84.
# Let's look for non-login-request data.

i = 0
pkt_num = 0
while i < len(data):
    # Try to identify packet type
    if i + 2 <= len(data):
        # Check if this is a login request
        if data[i:i+4] == b'\x01\x00\x00\x84':
            # Login request: known size ~145 bytes
            pkt_len = 145 + 2  # + 02 00 trailer
            print(f"[{pkt_num:3d}] @ {i:6d}: LOGIN REQUEST ({pkt_len}B) seq={data[i+5:i+7].hex()}")
            i += pkt_len
        else:
            flags = struct.unpack('<H', data[i:i+2])[0]
            print(f"[{pkt_num:3d}] @ {i:6d}: flags={flags:#06x} data={data[i:i+32].hex()}")
            # Unknown size, advance by minimum
            i += max(4, 1)
        pkt_num += 1
    else:
        break
    if pkt_num > 100:
        print("... (truncated)")
        break
