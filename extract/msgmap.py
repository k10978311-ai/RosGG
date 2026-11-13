"""Find BigWorld InterfaceElement structs by locating pointers to message-name strings,
then dump surrounding bytes to recover msgid + length style.

InterfaceElement (BigWorld) roughly:
    const char* name;      // 8 bytes, pointer to the name string
    MessageID id;          // 1 byte
    int8 lengthStyle;      // FIXED=0 / VARIABLE / CALLBACK ...
    int  lengthParam;      // fixed length, or #bytes of the length field
    ...
We locate `name` pointers and print the bytes right after them.
"""
import struct, sys
from elf import ELF

PATH = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
e = ELF(PATH)
d = e.d

NAMES = sys.argv[1:] or [
    "createBasePlayer", "createCellPlayer", "shortEntityMessage", "entityMessage",
    "authenticate", "login", "resourceVersionTag", "resetEntities", "setGameTime",
    "baseAppLogin", "loginApp",
]

# 1) find each name string's vaddr
name_va = {}
for nm in NAMES:
    needle = nm.encode() + b"\x00"
    i = 0
    while True:
        i = d.find(needle, i)
        if i < 0:
            break
        # prefer a string that starts cleanly (preceded by \x00)
        if i == 0 or d[i-1] == 0:
            va = e.off_to_vaddr(i)
            if va:
                name_va.setdefault(nm, []).append((i, va))
        i += 1

# 2) scan pointer-sized words across data sections for those vaddrs
targets = {va: nm for nm, lst in name_va.items() for (off, va) in lst}
print("Target name vaddrs:")
for nm, lst in name_va.items():
    print(f"  {nm}: " + ", ".join(hex(va) for _, va in lst))

datasecs = [s for s in e.secs if s["sname"] in (".data.rel.ro", ".data", ".rodata", ".rela.dyn")]
print("\nScanning", [s["sname"] for s in datasecs], "for pointers to those strings...\n")

found = []
for s in e.secs:
    if s["type"] == 8 or s["addr"] == 0:
        continue
    base, off, size = s["addr"], s["offset"], s["size"]
    for p in range(0, size - 8, 8):
        val = struct.unpack_from("<Q", d, off + p)[0]
        if val in targets:
            struct_va = base + p
            after = d[off+p+8: off+p+8+16]
            print(f"[{s['sname']}] ptr@{hex(struct_va)} -> {targets[val]:20s} "
                  f"id=0x{after[0]:02x}({after[0]}) lenStyle={after[1]} "
                  f"next8={after[:8].hex()} +8={after[8:16].hex()}")
            found.append((targets[val], struct_va, after))

# Also check .rela.dyn relocations (PIE: pointers are relocated at load time)
rela = e.sec(".rela.dyn")
if rela and not found:
    print("\nNo inline pointers found; checking .rela.dyn relocations (PIE)...")
    cnt = rela["size"]//24
    for i in range(cnt):
        r_offset, r_info, r_addend = struct.unpack_from("<QQq", d, rela["offset"]+i*24)
        if r_addend in targets:
            # the relocation writes `name` ptr at r_offset; struct starts there
            fo = e.vaddr_to_off(r_offset)
            after = d[fo+8: fo+8+16] if fo else b""
            print(f"[rela] struct@{hex(r_offset)} -> {targets[r_addend]:20s} "
                  f"id=0x{after[0]:02x}({after[0]}) lenStyle={after[1]} "
                  f"bytes={after.hex()}")
            found.append((targets[r_addend], r_offset, after))

print(f"\nTotal InterfaceElement candidates: {len(found)}")
