"""
Print detailed layout of the last few login requests to confirm request_id extraction.
"""
import struct

with open(r'C:\Users\Lufy\Desktop\Server\gate_capture.bin', 'rb') as f:
    raw = f.read()

LOGIN_MAGIC = b'\x01\x00\x00\x84'
LOGIN_SIZE  = 145

# Find all login request offsets
offsets = []
i = 0
while i < len(raw) - LOGIN_SIZE:
    if raw[i:i+4] == LOGIN_MAGIC:
        offsets.append(i)
        i += LOGIN_SIZE
    else:
        i += 1

print(f"Found {len(offsets)} login requests")
print()
print("Last 5 login requests - byte-by-byte layout:")
for off in offsets[-5:]:
    pkt = raw[off:off+LOGIN_SIZE]
    print(f"\n  Offset {off}:")
    print(f"    [0:4]   magic   = {pkt[0:4].hex()}  (01 00 00 84)")
    print(f"    [4]     unk     = {pkt[4]:02x}        (00)")
    print(f"    [5:7]   seq     = {pkt[5:7].hex()}   = {struct.unpack('<H', pkt[5:7])[0]:#06x}")
    print(f"    [7:11]  bytes78 = {pkt[7:11].hex()}  = {struct.unpack('<I', pkt[7:11])[0]:#010x}")
    print(f"    [11]    msgid   = {pkt[11]:02x}        (expected 2b=43)")
    print(f"    [12:15] pad     = {pkt[12:15].hex()}")
    # data[5:9] = the slice the server uses as request_id
    rid = pkt[5:9]
    rid_u32 = struct.unpack('<I', rid)[0]
    print(f"    [5:9]   req_id (data[5:9]) = {rid.hex()} = {rid_u32} (0x{rid_u32:08x})")
    print(f"    RSA block = {pkt[15:143].hex()[:48]}...")

print()
print("Note: The server sends reply with request_id = data[5:9].")
print("This is bytes [5..9] = {seq(2)} + {bytes7-8(2)} which may overlap.")
print()
print("Checking what field is actually the reply-id (the pending handler key):")
print("  From prior successful test: req_id=data[5:9] caused 'logOnComplete: Logon failed'")
print("  in 0.2s (not 9s timeout), proving the reply handler was matched.")
print("  Conclusion: data[5:9] IS the correct request_id field.")
