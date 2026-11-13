"""
Send the last captured login request to our local server to verify the reply
fires with the correct Blowfish encryption. No game client needed.
"""
import socket, struct, time

# Last login packet from capture (request at seq=0xf237, rest of fields per analysis)
# We need the actual packet bytes from gate_capture.bin
import os
cap_path = r'C:\Users\Lufy\Desktop\Server\gate_capture.bin'
if os.path.exists(cap_path) and os.path.getsize(cap_path) >= 145:
    with open(cap_path, 'rb') as f:
        data = f.read()
    # Find last login request
    LOGIN_MAGIC = b'\x01\x00\x00\x84'
    last_pkt = None
    i = 0
    while i < len(data) - 145:
        if data[i:i+4] == LOGIN_MAGIC:
            last_pkt = data[i:i+145]
            i += 145
        else:
            i += 1
    if last_pkt:
        print(f"Last login request: {last_pkt[:20].hex()}... ({len(last_pkt)}B)")
        print(f"  seq={last_pkt[5:7].hex()} req_id={last_pkt[5:9].hex()}")
        
        # Send to our server on :25000
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3.0)
        sock.sendto(last_pkt, ('127.0.0.1', 25000))
        print("Sent login packet to 127.0.0.1:25000, waiting for reply...")
        try:
            reply, addr = sock.recvfrom(4096)
            print(f"Got reply ({len(reply)}B) from {addr}: {reply.hex()}")
            # Parse reply
            flags = struct.unpack('<H', reply[0:2])[0]
            msg_len = struct.unpack('<I', reply[3:7])[0]
            req_id  = struct.unpack('<I', reply[7:11])[0]
            status  = reply[11]
            enc_rec = reply[12:28]
            seq_ft  = struct.unpack('<I', reply[-4:])[0]
            print(f"  flags={flags:#06x} msg_len={msg_len} req_id={req_id:#010x}")
            print(f"  status={status:#04x} enc_record={enc_rec.hex()} seq={seq_ft}")
            print(f"  request_id match: {req_id == struct.unpack('<I', last_pkt[5:9])[0]}")
        except socket.timeout:
            print("Timeout - no reply (is REPLY_VARIANT set?)")
        sock.close()
    else:
        print("No login packets in capture yet")
else:
    print("gate_capture.bin is empty or missing - trigger a login first")
