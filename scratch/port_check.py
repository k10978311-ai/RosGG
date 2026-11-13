"""
Check port byte-order interpretation.

Our record: ip(4 net-order) + port(2 net-order=big-endian) + salt(2) + sessionKey(4)

If client reads port as LITTLE-endian:
  port = 25000 = 0x61A8
  bytes: 61 A8 -> as little-endian = 0xA861 = 43105

Let's verify what port the client would actually connect to.
"""
import struct, socket

ip = socket.inet_aton('192.168.1.18')
print(f"IP bytes: {ip.hex()} = {socket.inet_ntoa(ip)}")

port = 25000
port_be = struct.pack('>H', port)  # network/big-endian
port_le = struct.pack('<H', port)  # little-endian

print(f"\nPort {port}:")
print(f"  Big-endian bytes:    {port_be.hex()} -> if read as LE = {struct.unpack('<H', port_be)[0]}")
print(f"  Little-endian bytes: {port_le.hex()} -> if read as BE = {struct.unpack('>H', port_le)[0]}")

# Our current record
record = ip + port_be + b'\x00\x00' + struct.pack('<I', 0x11223344)
print(f"\nCurrent record (12B): {record.hex()}")
print(f"  Bytes 4-5 (port): {record[4:6].hex()}")
print(f"  If client reads port as BE: {struct.unpack('>H', record[4:6])[0]}")  # = 25000 ✓
print(f"  If client reads port as LE: {struct.unpack('<H', record[4:6])[0]}")  # = 43105

# What if the port needs to be stored differently?
# BigWorld source: Mercury::Address stores port in network (big-endian) order
# BinaryIStream >> reads fields as-is from the wire (network byte order)
# So our port_be = struct.pack('>H', 25000) should be correct

# The salt field: in Mercury::Address, salt=0 is a valid initial salt
# When client connects to BaseApp, it uses this Address struct directly
# to open a Mercury channel

# Let's also check: what if 'port' in Mercury::Address is stored as little-endian?
# (Some BigWorld implementations store port in host byte order on the wire)
print()
print("If Mercury stores port in HOST order (little-endian on Android ARM):")
port_host = struct.pack('<H', port)  # little-endian
record_le = ip + port_host + b'\x00\x00' + struct.pack('<I', 0x11223344)
print(f"  Record: {record_le.hex()}")
print(f"  Port bytes: {port_host.hex()} -> client reads as LE = {port}")

# BF encrypt both variants to see what ciphertext they produce
from Crypto.Cipher import Blowfish
key = bytes.fromhex('0b6afd8e6c0f93213101e458a932b8a9')

padded_be = record + b'\x00\x00\x00\x00'
padded_le = record_le + b'\x00\x00\x00\x00'

enc_be = Blowfish.new(key, Blowfish.MODE_ECB).encrypt(padded_be)
enc_le = Blowfish.new(key, Blowfish.MODE_ECB).encrypt(padded_le)

print(f"\nBF-ECB encrypted:")
print(f"  port=BE (61a8): {enc_be.hex()}")
print(f"  port=LE (a861): {enc_le.hex()}")

# Our server currently sends enc_be = 198ae280a72afc73a823adbc66972b73
# If the client reads this and gets port 25000 -> tries to connect to :25000
# If client reads this and gets port 43105 -> tries to connect to :43105
print()
print(f"Our sent ciphertext: 198ae280a72afc73a823adbc66972b73")
print(f"Matches port=BE: {enc_be.hex() == '198ae280a72afc73a823adbc66972b73'}")
print(f"Matches port=LE: {enc_le.hex() == '198ae280a72afc73a823adbc66972b73'}")
