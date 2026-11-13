import capstone

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

start_pc = 0x93c500
length = 0x400

cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
code = data[start_pc : start_pc + length]

for insn in cs.disasm(code, start_pc):
    print(f"0x{insn.address:x}: {insn.mnemonic:10s} {insn.op_str}")
