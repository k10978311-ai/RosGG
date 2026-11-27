"""Decrypt NeoX script.npk (Rules of Survival 1.610637.617289) to marshalled code objects.

    python -I tools/npk_decrypt.py script/script.npk script/out

Pipeline per entry (from redirect.NpkImporter.load_module, read in-game):
    rotor.decrypt(key) -> zlib.decompress -> _reverse_string -> marshal.loads
_reverse_string: XOR the first 128 bytes with 0x9A, then reverse the whole string.

Output: out/<hash>.code (raw marshal of a Python 2.7 code object, no pyc header)
        out/index.json  (hash -> co_filename + strings found, for grep)
"""
import json
import os
import re
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(__file__))
from rotor import Rotor  # noqa: E402

KEY_FILE = os.path.join(os.path.dirname(__file__), "neox_rotor_key.txt")


class FastRotor:
    """Rotor decrypt via precomputed position streams: per stage translate + xor."""

    def __init__(self, key, maxlen):
        r = Rotor(key)
        self.key = key
        n = r.rotors
        self.n = n
        self.d_tables = [bytes(r.d[i]) for i in range(n)]
        streams = [bytearray(maxlen) for _ in range(n)]
        r._init()
        pos, adv = r.pos, r.adv
        for idx in range(maxlen):
            for i in range(n):
                streams[i][idx] = pos[i]
            # inline _advance
            for i in range(n):
                t = pos[i] + adv[i]
                pos[i] = t & 0xFF
                if t >= 256 and i < n - 1:
                    pos[i + 1] = (pos[i + 1] + 1) & 0xFF
        self.streams = [bytes(s) for s in streams]

    def decrypt(self, data):
        L = len(data)
        c = data
        for i in range(self.n - 1, -1, -1):
            c = c.translate(self.d_tables[i])
            x = int.from_bytes(c, "little") ^ int.from_bytes(self.streams[i][:L], "little")
            c = x.to_bytes(L, "little")
        return c

    def encrypt(self, data):
        if not hasattr(self, "e_tables"):
            r = Rotor(self.key)
            self.e_tables = [bytes(r.e[i]) for i in range(self.n)]
        L = len(data)
        if L > len(self.streams[0]):
            raise ValueError("data longer than precomputed rotor stream")
        p = data
        for i in range(self.n):
            x = int.from_bytes(p, "little") ^ int.from_bytes(self.streams[i][:L], "little")
            p = x.to_bytes(L, "little").translate(self.e_tables[i])
        return p


def reverse_string(b):
    b = bytes(x ^ 0x9A for x in b[:128]) + b[128:]
    return b[::-1]


def unreverse_string(b):
    b = b[::-1]
    return bytes(x ^ 0x9A for x in b[:128]) + b[128:]


def read_index(d):
    assert d[:4] == b"NXPK"
    files, _, _, _, io = struct.unpack_from("<IIIII", d, 4)
    return [struct.unpack_from("<IIIIIIHH", d, io + 28 * i) for i in range(files)]


STR_RE = re.compile(rb"[\x20-\x7e]{6,}")


def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    d = open(src, "rb").read()
    entries = read_index(d)
    key = open(KEY_FILE, encoding="latin-1").read()
    maxlen = max(e[2] for e in entries)
    print(f"{len(entries)} entries, max {maxlen} bytes; precomputing rotor streams...")
    fr = FastRotor(key, maxlen)
    index, bad = {}, 0
    for n, e in enumerate(entries):
        sign, off, ln = e[0], e[1], e[2]
        try:
            code = reverse_string(zlib.decompress(fr.decrypt(d[off:off + ln])))
        except Exception as ex:
            bad += 1
            open(os.path.join(out, f"{sign:08x}.raw"), "wb").write(d[off:off + ln])
            index[f"{sign:08x}"] = {"error": str(ex)}
            continue
        open(os.path.join(out, f"{sign:08x}.code"), "wb").write(code)
        strs = [s.decode() for s in STR_RE.findall(code)]
        fname = next((s for s in strs if s.endswith((".py", ".pyx"))), "")
        index[f"{sign:08x}"] = {"file": fname, "size": len(code), "strings": strs}
        if n % 500 == 0:
            print(f"  {n}/{len(entries)}")
    json.dump(index, open(os.path.join(out, "index.json"), "w"), indent=0)
    print(f"done: {len(entries) - bad} ok, {bad} failed -> {out}")


if __name__ == "__main__":
    main()
