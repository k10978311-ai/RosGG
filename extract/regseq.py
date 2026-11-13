"""Walk the message-registration function(s) and list each registered message in order
(= msgid assignment order), with name + lengthStyle + lengthParam.

Pattern per registration:
    adrp xR, page ; add xR, xR, #off      -> name string (resolved)
    mov  w2, #style
    mov  w3, #param
    ... mov x0, iface ...
    bl   0x98f654 / 0x98f5dc               -> assigns next id
"""
import struct, sys
from elf import ELF
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN

PATH = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
e = ELF(PATH); d = e.d
text = e.sec(".text"); tbase, toff, tsize = text["addr"], text["offset"], text["size"]

# region to scan: the registration function body (args: start_va end_va)
start_va = int(sys.argv[1], 0) if len(sys.argv) > 1 else 0x8116a0
end_va   = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0x812600
REG_TARGETS = {0x98f654, 0x98f5dc}

md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
off = e.vaddr_to_off(start_va)
chunk = d[off: e.vaddr_to_off(end_va)]
insns = list(md.disasm(chunk, start_va))

def imm(s):
    s = s.strip()
    return int(s, 0) if s.startswith("#") is False and s.startswith("0x") else int(s.lstrip("#"), 0)

def rdstr(va):
    o = e.vaddr_to_off(va)
    if o is None: return None
    end = d.index(b"\x00", o)
    s = d[o:end]
    return s.decode("ascii", "replace") if len(s) < 60 else None

reg_page = {}
cur_name = None
w2 = w3 = None
idx = 0
print(f"{'seq':>3} {'name':26} {'style':9} param")
for ins in insns:
    m, ops = ins.mnemonic, ins.op_str
    p = [x.strip() for x in ops.split(",")]
    try:
        if m == "adrp" and len(p) == 2:
            reg_page[p[0]] = int(p[1].lstrip("#"), 0)
        elif m == "add" and len(p) == 3 and p[2].startswith("#"):
            if p[1] in reg_page:
                tgt = reg_page[p[1]] + int(p[2].lstrip("#"), 0)
                s = rdstr(tgt)
                if s and s[:1].isalpha() and all(32 <= ord(c) < 127 for c in s):
                    cur_name = s
        elif m == "mov" and len(p) == 2 and p[1].startswith("#"):
            v = int(p[1].lstrip("#"), 0)
            if p[0] == "w2": w2 = v
            elif p[0] == "w3": w3 = v
        elif m == "bl" and len(p) == 1:
            tgt = int(p[0].lstrip("#"), 0)
            if tgt in REG_TARGETS and cur_name:
                style = {0:"FIXED",1:"VARIABLE",2:"CALLBACK"}.get(w2, str(w2))
                print(f"{idx:3} {cur_name:26} {style:9} {w3}")
                idx += 1
                cur_name = None; w2 = w3 = None
    except Exception:
        pass
print(f"\nTotal registered: {idx}")
