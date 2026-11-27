import sys, os, struct
sys.path.insert(0, 'extract')
from elf import ELF
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
PATH = 'extract/libclient.so'
e = ELF(PATH); d = e.d
text = e.sec('.text')
tbase, toff, tsize = text['addr'], text['offset'], text['size']
md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)

# Search for LDR/STR ..., [..., #0xf98]
# In ARM64, LDR/STR 64-bit with imm #0xf98: imm12 = 0xf98/8 = 0x1f3 = 499
for k in range(0, tsize, 4):
    w = struct.unpack_from('<I', d, toff + k)[0]
    # 0xf9400000 | (imm12 << 10) -> LDR Xt, [Xn, #imm12*8]
    # 0xf9000000 | (imm12 << 10) -> STR Xt, [Xn, #imm12*8]
    if (w & 0xFFC00000) in (0xF9400000, 0xF9000000):
        imm12 = (w >> 10) & 0xFFF
        if imm12 * 8 == 0xf98:
            va = tbase + k
            print('hit at', hex(va))
