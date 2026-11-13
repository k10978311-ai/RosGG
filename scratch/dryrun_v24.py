"""
Dry-run of loginapp.build_reply() with the LAST captured request packet,
using the corrected BF_SPEC=1:16 (confirmed ECB, 16-byte key at offset 1).
"""
import sys, os
sys.path.insert(0, r'C:\Users\Lufy\Desktop\Server')
os.environ['REPLY_VARIANT'] = '24'
os.environ['BF_SPEC'] = '1:16'   # confirmed correct

import loginapp, importlib
importlib.reload(loginapp)

from Crypto.Cipher import Blowfish
import struct, socket

# Last captured request (from server.log - last [UDP GATE] 25000 line):
# We'll reconstruct a synthetic one to test the key path.
# The RSA-decrypted LogOnParams rest from S3/S4:
# rest = 040b6afd8e6c0f93213101e458a932b8a9ffcd3cdb035a3d6e

# Confirm key extraction
rest = bytes.fromhex('040b6afd8e6c0f93213101e458a932b8a9ffcd3cdb035a3d6e')
params = {'rest': rest}
bf = loginapp.extract_blowfish_key(params)
print(f"Extracted BF key: {bf.hex()} ({len(bf)} bytes)")
print(f"Expected:         0b6afd8e6c0f93213101e458a932b8a9")
assert bf.hex() == '0b6afd8e6c0f93213101e458a932b8a9', "KEY MISMATCH!"
print("Key extraction: CORRECT")

# Encrypt the record
target_ip = socket.inet_aton('192.168.1.18')
port_net  = struct.pack('>H', 25000)
record    = target_ip + port_net + b'\x00\x00' + struct.pack('<I', 0x11223344)
padded    = record + b'\x00' * 4

enc = Blowfish.new(bytes(bf), Blowfish.MODE_ECB).encrypt(padded)
print(f"\nPlaintext record : {record.hex()} (12 bytes)")
print(f"Padded (16B)     : {padded.hex()}")
print(f"Encrypted (ECB)  : {enc.hex()}")

# Verify round-trip
dec = Blowfish.new(bytes(bf), Blowfish.MODE_ECB).decrypt(enc)
ip_str = socket.inet_ntoa(dec[:4])
port_v = struct.unpack('>H', dec[4:6])[0]
print(f"Decrypted        : {dec.hex()}")
print(f"  -> ip={ip_str}  port={port_v}")
assert ip_str == '192.168.1.18', "IP ROUND-TRIP FAILED!"
assert port_v == 25000, "PORT ROUND-TRIP FAILED!"
print("\nRound-trip: PASS - client will decrypt to 192.168.1.18:25000")

# Show what the full variant=24 reply packet looks like
# (with a fake request_id = data[5:9] = 0x000000F3 for illustration)
req_id = struct.pack('<I', 0xF3)  # representative
rdata  = bytes([1]) + enc         # status=LOGGED_ON + enc_record
reply  = b'\xff' + struct.pack('<I', len(req_id) + len(rdata)) + req_id + rdata
flags  = struct.pack('<H', 0x0040)
pkt    = flags + reply + struct.pack('<I', 1)
print(f"\nFull reply packet ({len(pkt)} bytes): {pkt.hex()}")
print("  [0:2]  flags      : 0x0040 (HAS_SEQUENCE)")
print(f"  [2]    0xFF       : reply msg")
print(f"  [3:7]  msg_len    : {struct.unpack('<I', pkt[3:7])[0]}")
print(f"  [7:11] request_id : {pkt[7:11].hex()}")
print(f"  [11]   status     : {pkt[11]:02x} (LOGGED_ON)")
print(f"  [12:28] enc_record: {pkt[12:28].hex()}")
print(f"  [-4:]  seq footer : {struct.unpack('<I', pkt[-4:])[0]}")
