"""Shared ELF helpers for libclient.so static analysis."""
import struct

class ELF:
    def __init__(self, path):
        self.d = open(path, "rb").read()
        d = self.d
        assert d[:4] == b"\x7fELF" and d[4] == 2, "need ELF64"
        self.e_shoff = struct.unpack_from("<Q", d, 0x28)[0]
        self.e_shentsize = struct.unpack_from("<H", d, 0x3a)[0]
        self.e_shnum = struct.unpack_from("<H", d, 0x3c)[0]
        self.e_shstrndx = struct.unpack_from("<H", d, 0x3e)[0]
        self.secs = []
        for i in range(self.e_shnum):
            off = self.e_shoff + i*self.e_shentsize
            name, stype, flags, addr, offset, size, link, info, align, entsize = \
                struct.unpack_from("<IIQQQQIIQQ", d, off)
            self.secs.append(dict(name=name, type=stype, flags=flags, addr=addr,
                                  offset=offset, size=size, link=link, entsize=entsize))
        sh = self.secs[self.e_shstrndx]["offset"]
        for s in self.secs:
            end = d.index(b"\x00", sh+s["name"])
            s["sname"] = d[sh+s["name"]:end].decode()

    def sec(self, name):
        for s in self.secs:
            if s["sname"] == name:
                return s
        return None

    def vaddr_to_off(self, va):
        for s in self.secs:
            if s["type"] != 8 and s["addr"] <= va < s["addr"]+s["size"] and s["addr"] != 0:
                return s["offset"] + (va - s["addr"])
        return None

    def off_to_vaddr(self, off):
        for s in self.secs:
            if s["offset"] <= off < s["offset"]+s["size"] and s["addr"] != 0 and s["type"] != 8:
                return s["addr"] + (off - s["offset"])
        return None
