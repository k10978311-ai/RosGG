import capstone

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

fn = 0x98d948
code = data[fn : fn + 0x180]
for insn in cs.disasm(code, fn):
    print(f"0x{insn.address:x}: {insn.mnemonic:10s} {insn.op_str}")
