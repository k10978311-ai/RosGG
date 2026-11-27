import struct

with open("extract/libclient.so", "rb") as f:
    data = f.read()

target = 0x942fb4
bs = struct.pack("<Q", target)
idx = 0
while True:
    idx = data.find(bs, idx)
    if idx == -1:
        break
    print(f"Found pointer to 0x942fb4 at 0x{idx:x}")
    idx += 8
