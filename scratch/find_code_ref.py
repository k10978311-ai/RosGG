import capstone

with open("extract/libclient.so", "rb") as f:
    data = f.read()

cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
# Search in 0x930000 - 0x960000
for ins in cs.disasm(data[0x930000:0x960000], 0x930000):
    if "942fb4" in ins.op_str or "942fc0" in ins.op_str:
        print(f"0x{ins.address:x}: {ins.mnemonic} {ins.op_str}")
