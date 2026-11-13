import struct

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

def va_to_file(va):
    # Segment 1: 0..0x38a4f40 -> VA 0..0x38a4f40
    if va < 0x38a4f40:
        return va
    # Segment 2: file 0x38a5138 -> VA 0x38b5138
    if 0x38b5138 <= va < 0x4f553f0:
        return va - 0x38b5138 + 0x38a5138
    return va

for va in [0x3a00c08, 0x39fe168, 0x39fd708]:
    f_off = va_to_file(va)
    ptr = struct.unpack_from("<Q", data, f_off)[0]
    name_ptr_f = va_to_file(ptr + 8)
    name_ptr = struct.unpack_from("<Q", data, name_ptr_f)[0]
    name_f = va_to_file(name_ptr)
    end = data.find(b"\x00", name_f)
    print(f"VA {hex(va)} (file {hex(f_off)}) -> {hex(ptr)} -> name: {data[name_f:end]}")
