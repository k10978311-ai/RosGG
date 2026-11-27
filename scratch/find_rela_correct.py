import struct

with open("extract/libclient.so", "rb") as f:
    f.seek(0x31bac8)
    n = 0x46a688 // 24
    for i in range(n):
        r_offset, r_info, r_addend = struct.unpack('<QQq', f.read(24))
        if r_addend in (0x942fb4, 0x942fc0, 0x942f8c, 0x942f80):
            print(f"Target 0x{r_addend:x} at r_offset = 0x{r_offset:x}")
