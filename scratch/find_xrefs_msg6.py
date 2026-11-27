import sys, os, struct
sys.path.insert(0, 'extract')
from elf import ELF
PATH = 'extract/libclient.so'
e = ELF(PATH); d = e.d
text = e.sec('.text')
tbase, toff, tsize = text['addr'], text['offset'], text['size']
sva = 0x2a283d3

def sx(v, b): return v - (1 << b) if v & (1 << (b-1)) else v
words = struct.unpack_from('<%dI' % (tsize//4), d, toff)
reg_page = {}
xrefs = []
for k, w in enumerate(words):
    va = tbase + k*4
    if (w & 0x9F000000) == 0x90000000:
        rd = w & 0x1F; immlo=(w>>29)&3; immhi=(w>>5)&0x7FFFF
        reg_page[rd] = (va & ~0xFFF) + (sx((immhi<<2)|immlo,21) << 12)
    elif (w & 0xFFC00000) == 0x91000000:
        rd=w&0x1F; rn=(w>>5)&0x1F; imm=(w>>10)&0xFFF; sh=(w>>22)&3
        if sh==1: imm<<=12
        if rn in reg_page and reg_page[rn]+imm == sva:
            xrefs.append(va)
    elif (w & 0x9F000000) == 0x10000000:
        rd=w&0x1F; immlo=(w>>29)&3; immhi=(w>>5)&0x7FFFF
        if va + sx((immhi<<2)|immlo,21) == sva:
            xrefs.append(va)

print('xrefs:', [hex(x) for x in xrefs])
