import struct

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

# Search for "ServerConnection::logOnBegin" string
idx = data.find(b"ServerConnection::logOnBegin")
print("logOnBegin string at:", hex(idx) if idx != -1 else "not found")

# Search all BL instructions to 0x98cd30
for pc in range(0, 0x2a00000, 4):
    insn = struct.unpack_from("<I", data, pc)[0]
    if (insn & 0xFC000000) == 0x94000000:
        imm = insn & 0x03FFFFFF
        if imm & (1 << 25):
            imm -= (1 << 26)
        target = pc + imm * 4
        if target == 0x98cd30:
            print(f"BL to 0x98cd30 from {hex(pc)}")
