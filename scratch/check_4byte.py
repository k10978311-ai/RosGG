from Crypto.Cipher import Blowfish
import struct, socket

# In the last session:
# rest = 04 0b 6a fd 8e 6c 0f 93 21 31 ...
# 4-byte key = rest[1:5] = 0b 6a fd 8e
key4 = bytes.fromhex('0b6afd8e')
key16 = bytes.fromhex('0b6afd8e6c0f93213101e458a932b8a9')

# What our server sent:
# encrypted with key16:
# Block 0 was 198ae280a72afc73
c0 = bytes.fromhex('198ae280a72afc73')

# Client decrypted c0 with key4:
p_client = Blowfish.new(key4, Blowfish.MODE_ECB).decrypt(c0)
print(f"Client decrypted block 0 with 4-byte key: {p_client.hex()}")
ip_str = socket.inet_ntoa(p_client[:4])
port_val = struct.unpack('>H', p_client[4:6])[0]
print(f"IP: {ip_str}, Port: {port_val}")
print(f"Does it match 69.253.255.76:558? {ip_str == '69.253.255.76' and port_val == 558}")
