import struct

with open("extract/libclient.so", "rb") as f:
    data = f.read()

# In 64-bit ELF, Elf64_Rela is:
# r_offset (8), r_info (8), r_addend (8)
# R_AARCH64_RELATIVE = 1027 (0x403)
# When r_info == 0x403, r_addend is the target address!
target = 0x942fb4
for i in range(0, 0x500000, 24):
    r_offset, r_info, r_addend = struct.unpack_from("<QQq", data, i)
    if (r_info & 0xffffffff) == 1027 and r_addend == target:
        print(f"Relocation for 0x{target:x} at r_offset = 0x{r_offset:x}")
