import struct

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

def va_to_file(va):
    if va < 0x38a4f40:
        return va
    if 0x38b5138 <= va < 0x4f553f0:
        return va - 0x38b5138 + 0x38a5138
    return va

# Vtable was at 0x38bf800
vtable_va = 0x38bf800
f_off = va_to_file(vtable_va)
# Typeinfo ptr is at vtable - 8
tinfo_ptr = struct.unpack_from("<Q", data, f_off - 8)[0]
tinfo_f = va_to_file(tinfo_ptr)
name_ptr = struct.unpack_from("<Q", data, tinfo_f + 8)[0]
name_f = va_to_file(name_ptr)
end = data.find(b"\x00", name_f)
print(f"Vtable {hex(vtable_va)} is class: {data[name_f:end]}")
