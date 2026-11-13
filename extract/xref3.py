"""Thorough ARM64 xref finder: catches ADRP+ADD and ADRP+LDR(:lo12:) references to a
target string vaddr, tracking page values per register across the whole .text."""
import struct, sys
from elf import ELF
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN

PATH = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
e = ELF(PATH); d = e.d
text = e.sec(".text"); tbase, toff, tsize = text["addr"], text["offset"], text["size"]

marker = sys.argv[1] if len(sys.argv) > 1 else "publicEncrypt failed"
before = int(sys.argv[2]) if len(sys.argv) > 2 else 40
after  = int(sys.argv[3]) if len(sys.argv) > 3 else 8

si = d.find(marker.encode())
assert si >= 0, "marker not found"
# back up to string start (previous NUL)
st = d.rfind(b"\x00", 0, si) + 1
sva = e.off_to_vaddr(st)
print(f"string starts at off {hex(st)} va {hex(sva)}: {d[st:st+60]!r}")

def sx(v, b): return v - (1 << b) if v & (1 << (b-1)) else v
words = struct.unpack_from("<%dI" % (tsize//4), d, toff)
reg_page = {}
hits = []
for k, w in enumerate(words):
    va = tbase + k*4
    if (w & 0x9F000000) == 0x90000000:  # ADRP
        rd = w & 0x1F; immlo=(w>>29)&3; immhi=(w>>5)&0x7FFFF
        reg_page[rd] = (va & ~0xFFF) + (sx((immhi<<2)|immlo,21) << 12)
    elif (w & 0xFFC00000) == 0x91000000:  # ADD imm (64)
        rd=w&0x1F; rn=(w>>5)&0x1F; imm=(w>>10)&0xFFF; sh=(w>>22)&3
        if sh==1: imm<<=12
        if rn in reg_page and reg_page[rn]+imm == sva:
            hits.append(("ADD", va))
    elif (w & 0x3B000000) == 0x39000000:  # LDR/STR (unsigned imm) incl LDRB
        rn=(w>>5)&0x1F; imm=(w>>10)&0xFFF; size=(w>>30)&3
        scaled = imm << size
        if rn in reg_page and reg_page[rn]+scaled == sva:
            hits.append(("LDR", va))

print(f"xrefs: {[(t, hex(v)) for t,v in hits]}")
md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
for t, x in hits[:2]:
    off = e.vaddr_to_off(x); start = off - before*4
    chunk = d[start: off + after*4]
    print(f"\n==== {t} ref at {hex(x)} ====")
    for ins in md.disasm(chunk, e.off_to_vaddr(start)):
        mark = " <<<" if ins.address == x else ""
        print(f"  {hex(ins.address)}: {ins.mnemonic:8} {ins.op_str}{mark}")
