import os, sys, socket, struct
sys.path.insert(0, r'C:\Users\Lufy\Desktop\Server')
import loginapp, importlib
importlib.reload(loginapp)

rest = bytes.fromhex('040b6afd8e6c0f93213101e458a932b8a9ffcd3cdb80ecfd3d')
bf = loginapp.extract_blowfish_key({'rest': rest})
print('bf:', bf.hex(), 'len:', len(bf))

data = open(r'C:\Users\Lufy\Desktop\Server\gate_capture.bin', 'rb').read()[-145:]
pkt, params, bf_res = loginapp.build_reply(data, '192.168.1.18', 25000, 24)
print('Reply len:', len(pkt))
print('Reply hex:', pkt.hex())
print('bf_res:', bf_res.hex(), 'len:', len(bf_res))

# Test decrypt with 4-byte key
from scratch.test_custom_bf import custom_bf_decrypt
enc_rec = pkt[12:-4]
dec = custom_bf_decrypt(bf_res, enc_rec)
print('Decrypted:', dec.hex())
dec_ip = socket.inet_ntoa(dec[:4])
dec_port = struct.unpack('>H', dec[4:6])[0]
print(f'IP={dec_ip}, Port={dec_port}')
assert dec_ip == '192.168.1.18'
assert dec_port == 25000
print('VERIFIED!')
