import capstone

data = open(r"C:\Users\Lufy\Desktop\Server\extract\libclient.so", "rb").read()
cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

# In 0x93c79c: bl #0x985cfc
# Let's inspect 0x985cfc again!
# Earlier disasm of 0x985cfc:
# 0x985cfc: str w1, [x0]
# 0x985d00: stur x2, [x0, #4]
# 0x985d04: stur x3, [x0, #0xc]
# 0x985d08: strh w4, [x0, #0x14]
# 0x985d0c: ret
for i in cs.disasm(data[0x985cfc : 0x985cfc + 0x20], 0x985cfc):
    print(f"0x{i.address:x}: {i.mnemonic:10s} {i.op_str}")

# Also check 0x985ce4:
print("--- 0x985ce4 ---")
for i in cs.disasm(data[0x985ce4 : 0x985ce4 + 0x20], 0x985ce4):
    print(f"0x{i.address:x}: {i.mnemonic:10s} {i.op_str}")
