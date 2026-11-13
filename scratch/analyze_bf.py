from Crypto.Cipher import Blowfish
import struct, socket

# From the ACTUAL server log - last session's LogOnParams:
# rest=040b6afd8e6c0f93213101e458a932b8a9ffcd3cdb035a3d6e
# bf (what loginapp.py currently extracts with BF_SPEC=2:16) = 0b6afd8e6c0f93213101e458a932b8a9

rest = bytes.fromhex('040b6afd8e6c0f93213101e458a932b8a9ffcd3cdb035a3d6e')
bf_current = rest[2:18]  # what server is currently using (16 bytes, offset 2)
bf_4byte   = rest[1:5]   # 4-byte key (after 0x04 length prefix)

print(f'rest       : {rest.hex()}')
print(f'bf_current : {bf_current.hex()} (16 bytes, offset 2)')
print(f'bf_4byte   : {bf_4byte.hex()} (4 bytes, offset 1)')

# Target: 192.168.1.18:25000
target_ip = socket.inet_aton('192.168.1.18')
port_net  = struct.pack('>H', 25000)
record    = target_ip + port_net + b'\x00\x00' + struct.pack('<I', 0x11223344)
padded    = record + b'\x00' * 4  # pad to 16

print(f'Plaintext  : {record.hex()} ({len(record)} bytes)')
print(f'Padded     : {padded.hex()} ({len(padded)} bytes)')
print()

for name, key, mode_str in [
    ('16-byte ECB (current)', bf_current, 'ecb'),
    ('4-byte ECB', bf_4byte, 'ecb'),
    ('4-byte CBC iv=0', bf_4byte, 'cbc'),
]:
    try:
        if mode_str == 'cbc':
            c = Blowfish.new(key, Blowfish.MODE_CBC, b'\x00'*8)
            d = Blowfish.new(key, Blowfish.MODE_CBC, b'\x00'*8)
        else:
            c = Blowfish.new(key, Blowfish.MODE_ECB)
            d = Blowfish.new(key, Blowfish.MODE_ECB)
        enc = c.encrypt(padded)
        dec = d.decrypt(enc)
        ip_str   = socket.inet_ntoa(dec[:4])
        port_val = struct.unpack('>H', dec[4:6])[0]
        print(f'{name}:')
        print(f'  enc     -> {enc.hex()}')
        print(f'  decrypt -> {dec.hex()}')
        print(f'            ip={ip_str}  port={port_val}')
    except Exception as e:
        print(f'{name}: ERROR {e}')

print()

# The actual packet that was SENT last (from server log):
pkt_hex = '4000ff1500000033f2000001198ae280a72afc73a823adbc66972b7301000000'
pkt = bytes.fromhex(pkt_hex)
print(f'Sent packet : {pkt.hex()}')
flags   = struct.unpack('<H', pkt[0:2])[0]
msg_len = struct.unpack('<I', pkt[3:7])[0]
req_id  = struct.unpack('<I', pkt[7:11])[0]
status  = pkt[11]
rdata   = pkt[12:-4]
seq     = struct.unpack('<I', pkt[-4:])[0]
print(f'  flags      : {flags:#06x}')
print(f'  0xFF       : {pkt[2]:02x}')
print(f'  msg len    : {msg_len}')
print(f'  request_id : {req_id} ({req_id:#010x})')
print(f'  status     : {status:#04x}')
print(f'  enc_record : {rdata.hex()} ({len(rdata)} bytes)')
print(f'  seq footer : {seq}')
print()

# Try to decrypt the enc_record with all candidate keys
for name, key, mode_str in [
    ('16-byte ECB (current)', bf_current, 'ecb'),
    ('4-byte  ECB', bf_4byte, 'ecb'),
    ('4-byte  CBC iv=0', bf_4byte, 'cbc'),
]:
    try:
        if mode_str == 'cbc':
            d = Blowfish.new(key, Blowfish.MODE_CBC, b'\x00'*8)
        else:
            d = Blowfish.new(key, Blowfish.MODE_ECB)
        dec = d.decrypt(rdata)
        ip_str   = socket.inet_ntoa(dec[:4])
        port_val = struct.unpack('>H', dec[4:6])[0]
        print(f'  Decrypt ({name}): {dec.hex()}')
        print(f'    -> ip={ip_str}  port={port_val}')
    except Exception as e:
        print(f'  Decrypt ({name}): ERROR {e}')
