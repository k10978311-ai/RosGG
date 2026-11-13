from Crypto.Cipher import Blowfish
import struct, socket

def custom_bf_encrypt(key, data):
    # data must be multiple of 8
    assert len(data) % 8 == 0
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    out = bytearray()
    prev_plain = None
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        if prev_plain is not None:
            # XOR block with prev_plain
            xored = bytes(a ^ b for a, b in zip(block, prev_plain))
        else:
            xored = block
        enc_block = cipher.encrypt(xored)
        out.extend(enc_block)
        prev_plain = block
    return bytes(out)

def custom_bf_decrypt(key, data):
    assert len(data) % 8 == 0
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    out = bytearray()
    prev_plain = None
    for i in range(0, len(data), 8):
        enc_block = data[i:i+8]
        dec_block = cipher.decrypt(enc_block)
        if prev_plain is not None:
            plain_block = bytes(a ^ b for a, b in zip(dec_block, prev_plain))
        else:
            plain_block = dec_block
        out.extend(plain_block)
        prev_plain = plain_block
    return bytes(out)

# Test round-trip
key = bytes.fromhex('0b6afd8e6c0f93213101e458a932b8a9')
ip_bytes = socket.inet_aton('192.168.1.18')
port_be = struct.pack('>H', 25000)

# 20 bytes struct:
# 0..3: IP
# 4..5: Port
# 6..15: 10 zero bytes
# 16..19: session key (e.g. 0x11223344)
rec20 = ip_bytes + port_be + b'\x00' * 10 + struct.pack('<I', 0x11223344)
rec24 = rec20 + b'\x00' * 4 # pad to 24 bytes (multiple of 8)

enc = custom_bf_encrypt(key, rec24)
dec = custom_bf_decrypt(key, enc)

print("Original (24B):", rec24.hex())
print("Encrypted (24B):", enc.hex())
print("Decrypted (24B):", dec.hex())
assert dec == rec24

# Check block 0:
dec_ip = socket.inet_ntoa(dec[:4])
dec_port = struct.unpack('>H', dec[4:6])[0]
dec_sk = struct.unpack('<I', dec[16:20])[0]
print(f"Decoded: ip={dec_ip}, port={dec_port}, sessionKey={hex(dec_sk)}")
