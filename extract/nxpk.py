"""Minimal NXPK (NeoX pack) reader. Extracts entries, decompresses zlib/lz4, and
locates the one containing an RSA public key. Based on the public neox_tools format.

Usage: python nxpk.py <assets.npk> <outdir>
"""
import struct, sys, zlib, os, hashlib

def read(path, outdir):
    d = open(path, "rb").read()
    assert d[:4] == b"NXPK", "not NXPK"
    files, var1, mode, hash_mode, index_off = struct.unpack_from("<IIIII", d, 4)
    print(f"files={files} var1={var1} mode={mode} hash_mode={hash_mode} index_off={hex(index_off)} size={len(d)}")
    os.makedirs(outdir, exist_ok=True)
    entry_size = (len(d) - index_off) // files
    print(f"entry_size={entry_size} (remainder {(len(d)-index_off)%files})")
    pem_hits = []
    for i in range(files):
        base = index_off + i * entry_size
        sign, off, zlen, olen = struct.unpack_from("<IIII", d, base)
        blob = d[off:off+zlen]
        raw = blob
        for name, fn in (("zlib", lambda b: zlib.decompress(b)),):
            try:
                if blob[:2] in (b"\x78\x9c", b"\x78\x01", b"\x78\xda"):
                    raw = zlib.decompress(blob)
                    break
            except Exception:
                pass
        if b"BEGIN" in raw and b"KEY" in raw and len(raw) < 4000:
            pem_hits.append((i, sign, off, zlen, olen, raw))
    print(f"PEM-like entries: {len(pem_hits)}")
    for i, sign, off, zlen, olen, raw in pem_hits:
        fn = os.path.join(outdir, f"key_{i}_{sign:08x}.pem")
        open(fn, "wb").write(raw)
        print(f"  entry {i} sign={sign:08x} off={hex(off)} zlen={zlen} olen={olen} -> {fn}")
        print("   ", raw[:80])
    return pem_hits

if __name__ == "__main__":
    read(sys.argv[1], sys.argv[2])
