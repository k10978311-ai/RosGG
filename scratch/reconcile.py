"""
Reconcile: why did the previous server.log show ip=0.0.0.0 if the ciphertext 
198ae280... is exactly what the correct key produces?

The last packet sent was:
  4000ff1500000033f2000001198ae280a72afc73a823adbc66972b7301000000

enc_record = 198ae280a72afc73a823adbc66972b73

With bf_current (offset 2:16) = 6afd8e6c0f93213101e458a932b8a9ff:
  - this was used to ENCRYPT and produced 198ae280...?

Let's check: encrypt with offset-2 key, see if it matches enc_record
"""
from Crypto.Cipher import Blowfish
import struct, socket

rest = bytes.fromhex('040b6afd8e6c0f93213101e458a932b8a9ffcd3cdb035a3d6e')
bf_off1 = rest[1:17]   # 0b6afd8e6c0f93213101e458a932b8a9  <- CORRECT
bf_off2 = rest[2:18]   # 6afd8e6c0f93213101e458a932b8a9ff  <- was being used

target_ip = socket.inet_aton('192.168.1.18')
port_net  = struct.pack('>H', 25000)
record    = target_ip + port_net + b'\x00\x00' + struct.pack('<I', 0x11223344)
padded    = record + b'\x00' * 4
enc_record = bytes.fromhex('198ae280a72afc73a823adbc66972b73')

for name, key in [('off=1 (correct)', bf_off1), ('off=2 (was used)', bf_off2)]:
    enc = Blowfish.new(key, Blowfish.MODE_ECB).encrypt(padded)
    dec = Blowfish.new(key, Blowfish.MODE_ECB).decrypt(enc_record)
    print(f"{name}: key={key.hex()}")
    print(f"  encrypt(padded)   = {enc.hex()}")
    print(f"  match enc_record? {enc == enc_record}")
    print(f"  decrypt(sent)     = {dec.hex()}")
    try:
        ip_str = socket.inet_ntoa(dec[:4])
        port_v = struct.unpack('>H', dec[4:6])[0]
        print(f"  -> ip={ip_str}  port={port_v}")
    except:
        pass
    print()

print("Conclusion:")
print("  If off=1 matches -> previous encryption was CORRECT, client had a different issue")
print("  If off=2 matches -> code was always wrong, but somehow produced same bytes (coincidence)")
