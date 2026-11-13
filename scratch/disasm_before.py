import capstone

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

start = 0x93c400
length = 0x180
code = data[start : start + length]
for insn in cs.disasm(code, start):
    print(f"0x{insn.address:x}: {insn.mnemonic:10s} {insn.op_str}")
