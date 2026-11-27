"""Parse NeoX-obfuscated Python 2.7 marshal (RoS 1.610637.617289 script.npk entries).

NeoX change vs stock marshal: every string payload ('s', 't', 'u') is XORed with a
descending counter: plain[i] = enc[i] ^ ((len - 1 - i) & 0xFF). Same applies to co_code.
(Bytecode opcodes may additionally be remapped; not needed for string/URL work.)

    python -I tools/neox_marshal.py script/out script/strings   # per-module string dumps
"""
import json
import os
import struct
import sys


def xs(b):
    n = len(b)
    return bytes(c ^ ((n - 1 - i) & 0xFF) for i, c in enumerate(b))


class Code:
    __slots__ = ("argcount", "nlocals", "stacksize", "flags", "code", "consts", "names",
                 "varnames", "freevars", "cellvars", "filename", "name", "firstlineno", "lnotab")

    def walk(self):
        yield self
        for c in self.consts:
            if isinstance(c, Code):
                yield from c.walk()


class Reader:
    def __init__(self, data):
        self.d, self.p, self.refs = data, 0, []
        self.spans = []  # (payload_offset, length, type) of every s/t/u string

    def u8(self):
        v = self.d[self.p]
        self.p += 1
        return v

    def i32(self):
        v = struct.unpack_from("<i", self.d, self.p)[0]
        self.p += 4
        return v

    def raw(self, n):
        v = self.d[self.p:self.p + n]
        self.p += n
        return v

    def obj(self):
        t = chr(self.u8())
        if t == "0":
            return None
        if t == "N":
            return None
        if t in "FT":
            return t == "T"
        if t == "S":
            return StopIteration
        if t == ".":
            return Ellipsis
        if t == "i":
            return self.i32()
        if t == "I":
            return struct.unpack("<q", self.raw(8))[0]
        if t == "l":
            n = self.i32()
            v = 0
            for k in range(abs(n)):
                v |= struct.unpack("<H", self.raw(2))[0] << (15 * k)
            return -v if n < 0 else v
        if t == "f":
            return float(self.raw(self.u8()))
        if t == "g":
            return struct.unpack("<d", self.raw(8))[0]
        if t == "y":
            return complex(*struct.unpack("<dd", self.raw(16)))
        if t == "x":
            a = float(self.raw(self.u8()))
            return complex(a, float(self.raw(self.u8())))
        if t in "st":
            n = self.i32()
            self.spans.append((self.p, n, t))
            s = xs(self.raw(n))
            if t == "t":
                self.refs.append(s)
            return s
        if t == "R":
            return self.refs[self.i32()]
        if t == "u":
            n = self.i32()
            self.spans.append((self.p, n, t))
            return xs(self.raw(n)).decode("utf-8", "replace")
        if t in "([<>":
            n = self.i32()
            items = [self.obj() for _ in range(n)]
            return tuple(items) if t == "(" else items
        if t == "{":
            dct = {}
            while True:
                k = self.obj()
                if k is None and self.d[self.p - 1] == ord("0"):
                    break
                dct[k] = self.obj()
            return dct
        if t == "c":
            c = Code()
            c.argcount, c.nlocals, c.stacksize, c.flags = (self.i32() for _ in range(4))
            c.code = self.obj()
            c.consts, c.names, c.varnames, c.freevars, c.cellvars = (self.obj() for _ in range(5))
            c.filename, c.name = self.obj(), self.obj()
            c.firstlineno = self.i32()
            c.lnotab = self.obj()
            return c
        raise ValueError(f"unknown marshal type {t!r} at {self.p - 1:#x}")


def load(data):
    return Reader(data).obj()


def strings_of(code):
    out = []
    for co in code.walk():
        for c in co.consts:
            if isinstance(c, bytes):
                out.append(("const", co.name.decode("latin-1"), c.decode("latin-1")))
            elif isinstance(c, str):
                out.append(("uconst", co.name.decode("latin-1"), c))
        for n in co.names:
            out.append(("name", co.name.decode("latin-1"), n.decode("latin-1")))
    return out


def main():
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    index, bad = {}, []
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".code"):
            continue
        h = fn[:-5]
        try:
            co = load(open(os.path.join(src, fn), "rb").read())
            fname = co.filename.decode("latin-1")
            strs = strings_of(co)
        except Exception as e:
            bad.append((h, str(e)))
            continue
        index[h] = fname
        with open(os.path.join(dst, h + ".txt"), "w", encoding="utf-8") as f:
            f.write(f"# {fname}\n")
            for kind, where, s in strs:
                f.write(f"{kind}\t{where}\t{s!r}\n")
    json.dump(index, open(os.path.join(dst, "_files.json"), "w"), indent=0, sort_keys=True)
    print(f"{len(index)} modules parsed, {len(bad)} failed")
    for b in bad[:10]:
        print("  fail", b)


if __name__ == "__main__":
    main()
