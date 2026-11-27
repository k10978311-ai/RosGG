import capstone

with open("extract/libclient.so", "rb") as f:
    f.seek(0x94c10c)
    code = f.read(128)

cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
for ins in cs.disasm(code, 0x94c10c):
    print(f"0x{ins.address:x}: {ins.mnemonic} {ins.op_str}")
