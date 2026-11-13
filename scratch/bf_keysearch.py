"""
Deep analysis of LogOnParams key structure.

The 'rest' field (after username+password) from multiple sessions:
S1: 04 08 19 6b e2 | 6c 0f 93 21 31 01 e4 58 a9 32 b8 a9 ff cd 3c db 0a 94 f0 63
S3: 04 0b 6a fd 8e | 6c 0f 93 21 31 01 e4 58 a9 32 b8 a9 ff cd 3c db 39 3d c5 77
   (from server log at 14:28)
S4: 04 0b 6a fd 8e | 6c 0f 93 21 31 01 e4 58 a9 32 b8 a9 ff cd 3c db 03 5a 3d 6e
   (from server log at 14:34)

Observations:
- Byte 0: always 0x04 -> likely a type tag for 'blowfish key follows'
- Bytes 1-4 vary per session (0x08196be2, 0x0b6afd8e, etc.)  <- KEY
- Bytes 5..20 are CONSTANT across S3 and S4, slightly differ from S1
  (6c 0f 93 21 31 01 e4 58 a9 32 b8 a9 ff cd 3c db)
- Bytes 21..24 vary again (trailing per-session suffix?)

This strongly suggests:
  - 0x04 is BigWorld's 'BF key descriptor' marker
  - Next byte(s) encode key length OR just the key follows
  - Actually from BigWorld source: LogOnParams::addEncryptionKey uses a fixed-width record
  - The key might be 8 bytes (Blowfish minimum block size)

Let me try all reasonable key sizes at all reasonable offsets.
"""

from Crypto.Cipher import Blowfish
import struct, socket

# Sessions
sessions = {
    'S1': bytes.fromhex('0408196be26c0f93213101e458a932b8a9ffcd3cdb0a94f063'),
    'S3': bytes.fromhex('040b6afd8e6c0f93213101e458a932b8a9ffcd3cdb393dc577'),
    'S4': bytes.fromhex('040b6afd8e6c0f93213101e458a932b8a9ffcd3cdb035a3d6e'),
}

# Target IP for validation
target_ip_bytes = socket.inet_aton('192.168.1.18')   # c0 a8 01 12
target_port     = struct.pack('>H', 25000)             # 61 a8

record   = target_ip_bytes + target_port + b'\x00\x00' + struct.pack('<I', 0x11223344)
padded   = record + b'\x00' * 4

# The actual encrypted record from the LAST packet sent:
enc_record = bytes.fromhex('198ae280a72afc73a823adbc66972b73')

print(f"Target encrypted record: {enc_record.hex()}")
print(f"Want decrypt -> ip=192.168.1.18 port=25000")
print()

# Try every combination of (session, offset, length, mode) to find which
# key+mode combination produces the enc_record from padded
found = []
for sess_name, rest in sessions.items():
    for off in range(0, len(rest) - 3):
        for ln in [4, 8, 16, 20, 24]:
            if off + ln > len(rest):
                continue
            key = rest[off:off+ln]
            if len(key) < 4:
                continue
            for mode_name, mode, iv in [
                ('ECB', Blowfish.MODE_ECB, None),
                ('CBC0', Blowfish.MODE_CBC, b'\x00'*8),
            ]:
                try:
                    if mode == Blowfish.MODE_ECB:
                        cipher = Blowfish.new(key, mode)
                    else:
                        cipher = Blowfish.new(key, mode, iv)
                    ct = cipher.encrypt(padded)
                    if ct == enc_record:
                        print(f"*** MATCH! sess={sess_name} off={off} len={ln} mode={mode_name}")
                        print(f"    key={key.hex()}")
                        found.append((sess_name, off, ln, mode_name, key))
                except Exception:
                    pass

if not found:
    print("No exact match found.")
    print()
    # Try reverse: decrypt enc_record with every candidate and see if ip matches
    print("--- Trying decrypt approach (looking for 192.168.1.18 in result) ---")
    for sess_name, rest in sessions.items():
        for off in range(0, len(rest) - 3):
            for ln in [4, 8, 16, 20, 24]:
                if off + ln > len(rest):
                    continue
                key = rest[off:off+ln]
                if len(key) < 4:
                    continue
                for mode_name, mode, iv in [
                    ('ECB', Blowfish.MODE_ECB, None),
                    ('CBC0', Blowfish.MODE_CBC, b'\x00'*8),
                ]:
                    try:
                        if mode == Blowfish.MODE_ECB:
                            d = Blowfish.new(key, mode)
                        else:
                            d = Blowfish.new(key, mode, iv)
                        pt = d.decrypt(enc_record)
                        if pt[:4] == target_ip_bytes:
                            print(f"*** DECRYPT MATCH! sess={sess_name} off={off} len={ln} mode={mode_name}")
                            print(f"    key={key.hex()}  plain={pt.hex()}")
                    except Exception:
                        pass

print()
print("--- Constant bytes across S3/S4 ---")
s3 = sessions['S3']
s4 = sessions['S4']
for i in range(min(len(s3), len(s4))):
    if s3[i] == s4[i]:
        print(f"  offset {i:2d}: {s3[i]:02x}  (constant)")
    else:
        print(f"  offset {i:2d}: {s3[i]:02x} vs {s4[i]:02x}  <-- VARIES")
