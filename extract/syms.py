"""List ELF dynsym/symtab entries matching keywords, with file offsets, for libclient.so."""
import struct, sys

import os
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libclient.so")
d = open(path, "rb").read()
assert d[:4] == b"\x7fELF"
is64 = d[4] == 2
le = "<"
e_shoff = struct.unpack_from(le+"Q", d, 0x28)[0]
e_shentsize = struct.unpack_from(le+"H", d, 0x3a)[0]
e_shnum = struct.unpack_from(le+"H", d, 0x3c)[0]
e_shstrndx = struct.unpack_from(le+"H", d, 0x3e)[0]

sections = []
for i in range(e_shnum):
    off = e_shoff + i*e_shentsize
    name, stype, flags, addr, offset, size, link, info, align, entsize = struct.unpack_from(le+"IIQQQQIIQQ", d, off)
    sections.append(dict(name=name, type=stype, addr=addr, offset=offset, size=size, link=link, entsize=entsize))

shstr_off = sections[e_shstrndx]["offset"]
def secname(n):
    end = d.index(b"\x00", shstr_off+n)
    return d[shstr_off+n:end].decode()
for s in sections:
    s["sname"] = secname(s["name"])

kw = [k.encode() for k in (sys.argv[1:] or ["onLoginReply","LogOnParams","login","Challenge","EncryptionFilter","PacketFilter"])]
for s in sections:
    if s["sname"] in (".dynsym", ".symtab"):
        strtab = sections[s["link"]]
        symcount = s["size"]//s["entsize"]
        for i in range(symcount):
            base = s["offset"] + i*s["entsize"]
            st_name, st_info, st_other, st_shndx, st_value, st_size = struct.unpack_from(le+"IBBHQQ", d, base)
            if st_name == 0 or st_value == 0:
                continue
            end = d.index(b"\x00", strtab["offset"]+st_name)
            nm = d[strtab["offset"]+st_name:end]
            if any(k in nm for k in kw):
                # map vaddr -> file offset via containing section
                foff = None
                for sec in sections:
                    if sec["addr"] <= st_value < sec["addr"]+sec["size"] and sec["type"]==1:
                        foff = sec["offset"] + (st_value - sec["addr"]); break
                print(f"{s['sname']} vaddr={hex(st_value)} size={st_size} foff={hex(foff) if foff else '?'} {nm.decode(errors='replace')[:90]}")
