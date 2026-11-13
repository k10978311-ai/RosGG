"""Find the code that loads a given error string and disassemble the surrounding
function, so we can read the packet/message header parsing logic."""
import struct, sys
from elf import ELF
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN

import os
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libclient.so")
e = ELF(PATH); d = e.d
text = e.sec(".text"); tbase, toff, tsize = text["addr"], text["offset"], text["size"]

marker = sys.argv[1] if len(sys.argv) > 1 else "Got corrupted message header"
before = int(sys.argv[2]) if len(sys.argv) > 2 else 70
after = int(sys.argv[3]) if len(sys.argv) > 3 else 10

# locate string vaddr
si = d.find(marker.encode())
assert si >= 0, "string not found"
sva = e.off_to_vaddr(si)
print(f"string '{marker}' at va {hex(sva)}")

# find ADRP+ADD referencing sva (fast manual scan)
def sx(v, b): return v - (1 << b) if v & (1 << (b-1)) else v
words = struct.unpack_from("<%dI" % (tsize//4), d, toff)
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
    elif (w & 0x9F000000) == 0x10000000:  # ADR
        rd=w&0x1F; immlo=(w>>29)&3; immhi=(w>>5)&0x7FFFF
        if va + sx((immhi<<2)|immlo,21) == sva:
            xrefs.append(va)

print(f"xrefs: {[hex(x) for x in xrefs]}")
md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
for x in xrefs[:3]:
    off = e.vaddr_to_off(x)
    start = off - before*4
    chunk = d[start: off + after*4]
    print(f"\n==== around {hex(x)} ====")
    for ins in md.disasm(chunk, e.off_to_vaddr(start)):
        mark = " <<< (loads string)" if ins.address == x else ""
        print(f"  {hex(ins.address)}: {ins.mnemonic:8} {ins.op_str}{mark}")
