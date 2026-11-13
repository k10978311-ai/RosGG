"""
Properly parse gate_capture.bin as a stream of UDP datagrams.
Since each captured datagram is written with f.write(data) and they're contiguous,
we need to identify packet boundaries by finding login-request magic bytes.

Login request format:
  01 00 00 84 | 00 | seq(2) | 01 00 00 00 | 2b | 00 00 00 | <128B RSA> | 02 00
  = 4 + 1 + 2 + 4 + 1 + 3 + 128 + 2 = 145 bytes

After the login reply is sent, the client sends BaseApp Mercury packets.
These are the ones we care about for understanding the next protocol step.
"""
import struct, socket

with open(r'C:\Users\Lufy\Desktop\Server\gate_capture.bin', 'rb') as f:
    raw = f.read()

LOGIN_MAGIC = b'\x01\x00\x00\x84'
LOGIN_SIZE  = 145

pkts = []
i = 0
while i < len(raw):
    # Check for login request
    if raw[i:i+4] == LOGIN_MAGIC and i + LOGIN_SIZE <= len(raw):
        seq    = struct.unpack('<H', raw[i+5:i+7])[0]
        req_id = struct.unpack('<I', raw[i+7:i+11])[0]
        msgid  = raw[i+11]
        pkts.append(('LOGIN', i, LOGIN_SIZE, {
            'seq': seq, 'req_id': req_id, 'msgid': f'{msgid:02x}'
        }))
        i += LOGIN_SIZE
        continue

    # Try to parse as Mercury packet: flags(2) + ...
    if i + 6 <= len(raw):
        flags = struct.unpack('<H', raw[i:i+2])[0]
        # Heuristic: valid Mercury flags have few bits set (< 0x100)
        # and the first byte of body after flags could be 0xFF (reply) or a small msgid
        if flags < 0x0100 or flags == 0x0040 or flags == 0x0058 or flags == 0x0000:
            # Try to figure out size from message content
            body_start = i + 2
            if body_start < len(raw) and raw[body_start] == 0xFF:
                # REPLY message: [0xFF][len:u32]...
                if body_start + 5 <= len(raw):
                    msg_len = struct.unpack('<I', raw[body_start+1:body_start+5])[0]
                    total   = 2 + 1 + 4 + msg_len + (4 if flags & 0x40 else 0)
                    if total < 512 and i + total <= len(raw):
                        pkts.append(('REPLY', i, total, {'flags': flags, 'msg_len': msg_len}))
                        i += total
                        continue
    # Unknown: advance 1 byte
    i += 1

print(f"Total captured: {len(raw)} bytes")
print(f"Parsed {len(pkts)} packets:\n")

for pkt_type, offset, size, info in pkts:
    chunk = raw[offset:offset+size]
    if pkt_type == 'LOGIN':
        print(f"  LOGIN  @ {offset:6d} ({size:3d}B) seq={info['seq']:#06x} req_id={info['req_id']:#010x} msgid={info['msgid']}")
    else:
        print(f"  REPLY  @ {offset:6d} ({size:3d}B) flags={info['flags']:#06x} msg_len={info['msg_len']}")
        print(f"           hex={chunk.hex()}")

print()
# Also scan for any packets NOT matching login that have reasonable Mercury flags
print("--- Raw scan for non-login Mercury-looking packets ---")
i = 0
while i < len(raw) - 6:
    if raw[i:i+4] == LOGIN_MAGIC:
        i += LOGIN_SIZE
        continue
    flags = struct.unpack('<H', raw[i:i+2])[0]
    # Look for packets with plausible Mercury flags and NOT inside login RSA garbage
    if flags in (0x0000, 0x0001, 0x0008, 0x0040, 0x0048, 0x0050, 0x0058, 0x00C0, 0x00D8):
        # Double-check: next byte should be a reasonable message id
        b = raw[i+2]
        if b < 0x80 or b == 0xFF:
            snippet = raw[i:i+32].hex()
            print(f"  @ {i:6d} flags={flags:#06x} next_byte={b:#04x}: {snippet}")
    i += 1
