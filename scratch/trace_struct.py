import capstone

data = open(r"C:\Users\Lufy\Desktop\Server\extract\libclient.so", "rb").read()
cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

# In LoginHandler (x19), struct is at x19 + 0x50 (x23)
# Let's check instructions between 0x93c598 and 0x93c900 accessing x19, x23, or offsets from 0x50
for p in range(0x93c598, 0x93c900, 4):
    for i in cs.disasm(data[p:p+4], p):
        # check if accesses x19 or x23
        if "0x50" in i.op_str or "0x54" in i.op_str or "0x58" in i.op_str or "0x5c" in i.op_str or "0x60" in i.op_str or "x23" in i.op_str:
            print(f"0x{p:x}: {i.mnemonic:10s} {i.op_str}")
