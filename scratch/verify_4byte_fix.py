from Crypto.Cipher import Blowfish
import struct, socket

key4 = bytes.fromhex('0b6afd8e')
ip_bytes = socket.inet_aton('192.168.1.18')
port_be = struct.pack('>H', 25000)

rec20 = ip_bytes + port_be + b'\x00' * 10 + struct.pack('<I', 0x11223344)
rec24 = rec20 + b'\x00' * 4

# Encrypt with custom_bf_encrypt
import sys
sys.path.insert(0, r"C:\Users\Lufy\Desktop\Server")
from scratch.test_custom_bf import custom_bf_encrypt, custom_bf_decrypt

enc = custom_bf_encrypt(key4, rec24)
dec = custom_bf_decrypt(key4, enc)

print("Original :", rec24.hex())
print("Encrypted:", enc.hex())
print("Decrypted:", dec.hex())

dec_ip = socket.inet_ntoa(dec[:4])
dec_port = struct.unpack('>H', dec[4:6])[0]
print(f"Decoded fields: IP={dec_ip}, Port={dec_port}")
assert dec_ip == '192.168.1.18'
assert dec_port == 25000
print("CONFIRMED: Client will decode 192.168.1.18:25000!")
