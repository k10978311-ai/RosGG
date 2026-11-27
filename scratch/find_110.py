import capstone

with open("extract/libclient.so", "rb") as f:
    data = f.read()

cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
for ins in cs.disasm(data[0x940000:0x960000], 0x940000):
    if "0x110" in ins.op_str and ("str" in ins.mnemonic or "ldr" in ins.mnemonic):
        print(f"0x{ins.address:x}: {ins.mnemonic} {ins.op_str}")
