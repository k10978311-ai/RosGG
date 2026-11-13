import struct

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

# Let's search for references to 0x2a2766f in the binary.
# In a 64-bit ELF, literal pools or ADRP+ADD might be used.
# Let's search for 8-byte pointers (0x0000000002a2766f or similar)
str_va = 0x2a2766f # offset in file

# Let's check ELF load headers to know the VA
# Usually ELF header at offset 0
e_phoff = struct.unpack_from("<Q", data, 0x20)[0]
e_phnum = struct.unpack_from("<H", data, 0x38)[0]
e_phentsize = struct.unpack_from("<H", data, 0x36)[0]

print(f"phoff: {hex(e_phoff)}, phnum: {e_phnum}, entsize: {e_phentsize}")

loads = []
for i in range(e_phnum):
    ph = data[e_phoff + i * e_phentsize : e_phoff + (i+1) * e_phentsize]
    p_type, p_flags, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align = struct.unpack("<IIQQQQQQ", ph)
    if p_type == 1: # PT_LOAD
        loads.append((p_offset, p_filesz, p_vaddr, p_memsz, p_flags))
        print(f"LOAD: file {hex(p_offset)}..{hex(p_offset+p_filesz)} -> VA {hex(p_vaddr)}..{hex(p_vaddr+p_memsz)} flags={hex(p_flags)}")

# Find which load segment contains 0x2a2766f
for p_off, p_fsz, p_va, p_msz, p_fl in loads:
    if p_off <= str_va < p_off + p_fsz:
        va_of_str = p_va + (str_va - p_off)
        print(f"String offset {hex(str_va)} is at VA {hex(va_of_str)}")
        break
