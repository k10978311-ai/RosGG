"""Find ARM64 code xrefs (ADRP+ADD) to given string vaddrs in libclient.so, and
disassemble a window around each to reveal the msgid immediate passed alongside.

BigWorld registers messages like:
    INTERFACE_ELEMENT(name, lengthStyle, lengthParam)  -> builds InterfaceElement
The name string is loaded via ADRP/ADD; the msgid and length style are nearby
MOV/MOVZ immediates or struct stores.
"""
import struct, sys
from elf import ELF
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN

PATH = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
e = ELF(PATH)
d = e.d
text = e.sec(".text")
tbase, toff, tsize = text["addr"], text["offset"], text["size"]
code = d[toff:toff+tsize]

NAMES = sys.argv[1:] or ["createBasePlayer", "shortEntityMessage", "authenticate",
                         "resetEntities", "setGameTime", "baseAppLogin"]
# resolve name vaddrs
name_va = {}
for nm in NAMES:
    needle = nm.encode() + b"\x00"
    i = 0
    while True:
        i = d.find(needle, i)
        if i < 0: break
        if i == 0 or d[i-1] == 0:
            va = e.off_to_vaddr(i)
            if va: name_va[va] = nm
        i += 1

md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
md.detail = True

# First pass: compute ADRP page per instruction position, then ADD -> target address.
# We track per-register the last ADRP page value.
hits = []  # (nm, va_of_add, xref_list_window)
n = len(code)//4
# Decode whole .text once into a list for context windows
insns = list(md.disasm(code, tbase))
# index by address
addr_idx = {ins.address: k for k, ins in enumerate(insns)}

reg_page = {}
for k, ins in enumerate(insns):
    m = ins.mnemonic
    if m == "adrp":
        # operands: Xd, #imm (page addr)
        try:
            rd = ins.operands[0].reg
            page = ins.operands[1].imm
            reg_page[rd] = page
        except Exception:
            pass
    elif m == "add":
        ops = ins.operands
        if len(ops) == 3 and ops[1].type == 1 and ops[2].type == 2:  # reg = reg + imm
            base_reg = ops[1].reg
            if base_reg in reg_page:
                target = reg_page[base_reg] + ops[2].imm
                if target in name_va:
                    hits.append((name_va[target], ins.address, k))

print(f"Found {len(hits)} string xrefs\n")
for nm, va, k in hits[:40]:
    print(f"=== xref to '{nm}' at {hex(va)} ===")
    lo = max(0, k-6); hi = min(len(insns), k+10)
    for ins in insns[lo:hi]:
        mark = "  <<" if ins.address == va else ""
        print(f"  {hex(ins.address)}: {ins.mnemonic:8} {ins.op_str}{mark}")
    print()
