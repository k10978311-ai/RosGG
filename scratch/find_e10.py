import struct

with open("extract/libclient.so", "rb") as f:
    data = f.read()

# 0xe10 in ARM64 instructions:
# add/sub/ldr/str with imm 0xe10:
# 0xe10 = 3600 decimal.
# In ARM64: imm12 = 0xe10.
# ldr/str unsigned offset: imm12 << 2 or imm12 << 3
# Let's search for instructions with 0xe10.
import capstone
cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

# Let's scan around 0x940000 to 0x960000
start = 0x940000
end = 0x960000
chunk = data[start:end]
for ins in cs.disasm(chunk, start):
    if "0xe10" in ins.op_str:
        print(f"0x{ins.address:x}: {ins.mnemonic} {ins.op_str}")
