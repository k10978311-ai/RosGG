import struct

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

# Check pointers at 0x3a00c08, 0x39fe168, 0x39fd708
for va in [0x3a00c08, 0x39fe168, 0x39fd708]:
    ptr = struct.unpack_from("<Q", data, va)[0]
    # find string near ptr
    # in C++ typeinfo, the name string is at ptr + 8 (or ptr is the typeinfo structure)
    name_ptr = struct.unpack_from("<Q", data, ptr + 8)[0]
    name = ""
    if 0 <= name_ptr < len(data):
        end = data.find(b"\x00", name_ptr)
        name = data[name_ptr:end].decode(errors="ignore")
    print(f"VA {hex(va)} -> typeinfo {hex(ptr)} -> name: {name}")
