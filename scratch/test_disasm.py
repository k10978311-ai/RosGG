import capstone

data = open(r"C:\Users\Lufy\Desktop\Server\extract\libclient.so", "rb").read()
print("len:", len(data))
print("bytes at 0x93e47c:", data[0x93e47c:0x93e47c+16].hex())

cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)
for i in cs.disasm(data[0x93e47c:0x93e47c+0x80], 0x93e47c):
    print(hex(i.address), i.mnemonic, i.op_str)
