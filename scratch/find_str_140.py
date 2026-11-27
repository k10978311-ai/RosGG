import sys, os, struct
sys.path.insert(0, 'extract')
from elf import ELF
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
PATH = 'extract/libclient.so'
e = ELF(PATH); d = e.d
text = e.sec('.text')
tbase, toff, tsize = text['addr'], text['offset'], text['size']
md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)

# STR Xt, [Xn, #0x140]: 0x140 / 8 = 40 = 0x28 -> imm12 = 0x28
# 0xf9000000 | (0x28 << 10) = 0xf900a000
target = 0xF900A000
for k in range(0, tsize, 4):
    w = struct.unpack_from('<I', d, toff + k)[0]
    if (w & 0xFFC00000) == target:
        va = tbase + k
        chunk = d[toff + k - 16 : toff + k + 16]
        print(f'STR at {hex(va)}:')
        for ins in md.disasm(chunk, va - 16):
            mark = ' <---' if ins.address == va else ''
            print(f'  {hex(ins.address)}: {ins.mnemonic} {ins.op_str}{mark}')
