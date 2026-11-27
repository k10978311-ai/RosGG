"""Point the game scripts (script.npk) at your own server: same-length host replacement
inside the obfuscated marshal strings, re-encoded as loose .nxs files.

    python -I tools/patch_scripts.py hosts_map.example.json script/script.npk script/patched

Output:
  script/patched/nxs/<module path>.nxs   re-encrypted modules (rotor+zlib9+reverse, same as npk)
  script/patched/changes.txt             every replaced string, per module
Only modules that contain a matching host are written. Lengths never change, so the
marshal structure (and code object layout) is untouched.
"""
import json
import os
import re
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(__file__))
from neox_marshal import Reader, xs  # noqa: E402
from npk_decrypt import FastRotor, KEY_FILE, read_index, reverse_string, unreverse_string  # noqa: E402

HOST = rb"A-Za-z0-9-"


def rules_from(cfg):
    rules = []
    for kind in ("exact", "suffix"):
        for old, new in cfg.get(kind, {}).items():
            o, n = old.encode(), new.encode()
            if len(o) != len(n):
                sys.exit(f"length mismatch {old} -> {new}")
            rx = re.compile(rb"(?<![" + HOST + rb"])" + re.escape(o) + rb"(?![" + HOST + rb"]|\.[A-Za-z])")
            rules.append((rx, n))
    return rules


def patch_code(code, rules):
    r = Reader(code)
    top = r.obj()
    buf = bytearray(code)
    changes = []
    for off, n, t in r.spans:
        plain = xs(bytes(buf[off:off + n]))
        new = plain
        for rx, rep in rules:
            new = rx.sub(rep, new)
        if new != plain:
            assert len(new) == len(plain)
            buf[off:off + n] = xs(new)
            changes.append((plain, new))
    return bytes(buf), changes, top.filename.decode("latin-1")


def main():
    cfg, npk, out = sys.argv[1:4]
    rules = rules_from(json.load(open(cfg)))
    d = open(npk, "rb").read()
    entries = read_index(d)
    fr = FastRotor(open(KEY_FILE, encoding="latin-1").read(), max(e[2] for e in entries) + 65536)
    os.makedirs(out, exist_ok=True)
    log = open(os.path.join(out, "changes.txt"), "w", encoding="utf-8")
    mods = total = 0
    for e in entries:
        sign, off, ln = e[0], e[1], e[2]
        try:
            code = reverse_string(zlib.decompress(fr.decrypt(d[off:off + ln])))
            new, changes, fname = patch_code(code, rules)
        except Exception:
            continue
        if not changes:
            continue
        # verify: re-parse and re-encode round-trip
        Reader(new).obj()
        enc = fr.encrypt(zlib.compress(unreverse_string(new), 9))
        assert reverse_string(zlib.decompress(fr.decrypt(enc))) == new
        rel = fname.replace("\\", "/")
        rel = rel[:-3] if rel.endswith(".py") else rel
        dst = os.path.join(out, "nxs", rel + ".nxs")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "wb").write(enc)
        log.write(f"## {fname}  (npk hash {sign:08x})\n")
        for a, b in changes:
            log.write(f"   {a.decode('latin-1')[:140]!r}\n-> {b.decode('latin-1')[:140]!r}\n")
        mods += 1
        total += len(changes)
    log.close()
    print(f"{mods} modules patched, {total} strings replaced -> {out}/nxs  (see changes.txt)")


if __name__ == "__main__":
    main()
