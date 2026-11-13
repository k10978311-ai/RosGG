import capstone

data = open(r"C:\Users\Lufy\Desktop\Server\extract\libclient.so", "rb").read()
cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

for p in range(0x93c500, 0x93c950, 4):
    for i in cs.disasm(data[p:p+4], p):
        for off in ["#0x50", "#0x54", "#0x58", "#0x5c", "#0x60"]:
            if off in i.op_str:
                print(f"0x{p:x}: {i.mnemonic:10s} {i.op_str}")
