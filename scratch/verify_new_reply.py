import socket, struct, os, sys
sys.path.insert(0, r"C:\Users\Lufy\Desktop\Server")
import loginapp

cap_path = r'C:\Users\Lufy\Desktop\Server\gate_capture.bin'
with open(cap_path, 'rb') as f:
    data = f.read()

# get last 145-byte packet
last_pkt = data[-145:]
print("Last packet magic:", last_pkt[:4].hex())

reply, params, bf = loginapp.build_reply(last_pkt, "192.168.1.18", 25000, 24)
print(f"Built reply ({len(reply)} bytes):")
print(reply.hex())

# Let's inspect fields of reply:
flags = struct.unpack('<H', reply[:2])[0]
msg_type = reply[2]
msg_len = struct.unpack('<I', reply[3:7])[0]
req_id = struct.unpack('<I', reply[7:11])[0]
status = reply[11]
enc_data = reply[12:-4]
footer = struct.unpack('<I', reply[-4:])[0]

print(f"flags: {hex(flags)}")
print(f"msg_type: {hex(msg_type)}")
print(f"msg_len: {msg_len}")
print(f"req_id: {hex(req_id)}")
print(f"status: {status}")
print(f"enc_data ({len(enc_data)} bytes): {enc_data.hex()}")
print(f"footer: {footer}")

# Decrypt enc_data using custom_bf_decrypt
from scratch.test_custom_bf import custom_bf_decrypt
dec = custom_bf_decrypt(bytes(bf), enc_data)
print(f"Decrypted ({len(dec)} bytes): {dec.hex()}")
dec_ip = socket.inet_ntoa(dec[:4])
dec_port = struct.unpack('>H', dec[4:6])[0]
dec_sk = struct.unpack('<I', dec[16:20])[0]
print(f"Decoded fields: IP={dec_ip}, Port={dec_port}, sessionKey={hex(dec_sk)}")
assert dec_ip == "192.168.1.18"
assert dec_port == 25000
print("ALL CHECKS PASSED!")
