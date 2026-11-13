"""Fast ARM64 xref finder: manually decode ADRP+ADD to locate code referencing
message-name strings, then capstone-disasm a small window around each hit."""
import struct, sys
from elf import ELF
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN

PATH = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
e = ELF(PATH); d = e.d
text = e.sec(".text"); tbase, toff, tsize = text["addr"], text["offset"], text["size"]

NAMES = sys.argv[1:] or ["createBasePlayer", "shortEntityMessage", "authenticate",
                         "resetEntities", "baseAppLogin", "setGameTime"]
name_va = {}
for nm in NAMES:
    needle = nm.encode() + b"\x00"; i = 0
    while True:
        i = d.find(needle, i)
        if i < 0: break
        if i == 0 or d[i-1] == 0:
            va = e.off_to_vaddr(i)
            if va: name_va[va] = nm
        i += 1

def sx(v, bits):
    return v - (1 << bits) if v & (1 << (bits-1)) else v

# linear scan: track ADRP page per dest reg; on ADD imm, test target
words = struct.unpack_from("<%dI" % (tsize//4), d, toff)
reg_page = {}
hits = []
for k, w in enumerate(words):
    va = tbase + k*4
    # ADRP: bit31=1, bits[28:24]=0b10000
    if (w & 0x9F000000) == 0x90000000:
        rd = w & 0x1F
        immlo = (w >> 29) & 3
        immhi = (w >> 5) & 0x7FFFF
        imm = sx((immhi << 2) | immlo, 21)
        page = (va & ~0xFFF) + (imm << 12)
        reg_page[rd] = page
    # ADD (imm) 64-bit: bits[31:23]=0b100100010 (sf=1,op=0,S=0,0010001,shift)
    elif (w & 0xFFC00000) == 0x91000000:
        rd = w & 0x1F
        rn = (w >> 5) & 0x1F
        imm12 = (w >> 10) & 0xFFF
        sh = (w >> 22) & 3
        if sh == 1: imm12 <<= 12
        if rn in reg_page:
            target = reg_page[rn] + imm12
            if target in name_va:
                hits.append((name_va[target], va))

print(f"Found {len(hits)} xrefs")
md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
for nm, va in hits[:25]:
    off = e.vaddr_to_off(va)
    start = off - 11*4
    chunk = d[start:off + 14*4]
    print(f"\n=== '{nm}' referenced at {hex(va)} ===")
    for ins in md.disasm(chunk, e.off_to_vaddr(start)):
        mark = " <<<" if ins.address == va else ""
        print(f"  {hex(ins.address)}: {ins.mnemonic:8} {ins.op_str}{mark}")
