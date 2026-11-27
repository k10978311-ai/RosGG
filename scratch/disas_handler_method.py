import os, sys, struct
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
PATH = "extract/libclient.so"
d = open(PATH, "rb").read()
# ELF load address is 0
md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
addr = 0x91e960
chunk = d[addr:addr+240]
for ins in md.disasm(chunk, addr):
    print(f"0x{ins.address:06x}: {ins.mnemonic} {ins.op_str}")
