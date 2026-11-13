import capstone

data = open(r"C:\Users\Lufy\Desktop\Server\extract\libclient.so", "rb").read()
cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

start = 0x93e56c
length = 0x100
for i in cs.disasm(data[start : start + length], start):
    print(f"0x{i.address:x}: {i.mnemonic:10s} {i.op_str}")
