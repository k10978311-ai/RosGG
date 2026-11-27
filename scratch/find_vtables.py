import struct

with open("extract/libclient.so", "rb") as f:
    data = f.read()

for target in (0x942f8c, 0x942f80, 0x942fc8, 0x942fc0):
    bs = struct.pack("<Q", target)
    idx = 0
    while True:
        idx = data.find(bs, idx)
        if idx == -1:
            break
        print(f"Target 0x{target:x} found at 0x{idx:x}")
        idx += 8
