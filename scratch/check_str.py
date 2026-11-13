so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

for va in [0x2a4701e, 0x2a46eb6]:
    end = data.find(b"\x00", va)
    print(f"VA {hex(va)}: {data[va:end]}")
