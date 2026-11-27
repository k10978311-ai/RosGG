"""Replace hardcoded NetEase API hosts inside the APK with your own server's domain.

Usage:
    python -I tools/patch_hosts.py hosts_map.json xapk/com.netease.chiji.apk patched/ros_patched_unsigned.apk

hosts_map.json:
    {
      "suffix": {"easebar.com": "rospriv.lan", "netease.com": "rospriv.net"},
      "exact":  {"www.rulesofsurvivalgame.com": "..."},     # optional
      "only_hosts": []                                        # optional whitelist of full hosts
    }

Every replacement MUST be byte-for-byte the same length as the original. Native
.so strings and dex string data have fixed sizes, so a longer/shorter host would
corrupt the file. The script refuses unequal lengths.

What gets patched:
  * classes*.dex  -> string data in place, then SHA-1 signature + adler32 checksum
                     recomputed. Aborts a dex if the string_ids sort order breaks
                     (ART verifier rejects unsorted string tables).
  * lib/**/*.so, assets/*, res/raw/*, resources.arsc (UTF-8 and UTF-16LE)
Everything else is copied untouched. META-INF signatures are dropped (re-sign
afterwards with tools/sign_apk.ps1). Stored entries are 4-byte aligned, .so
entries 4096-byte aligned, so no separate zipalign pass is required.
"""
import hashlib
import json
import re
import struct
import sys
import zipfile
import zlib

HOST_CHARS = rb"A-Za-z0-9-"


def build_rules(cfg):
    rules = []  # (compiled regex, old bytes, new bytes)
    for old, new in cfg.get("exact", {}).items():
        rules.append((old.encode(), new.encode(), True))
    for old, new in cfg.get("suffix", {}).items():
        rules.append((old.encode(), new.encode(), False))
    for old, new, _ in rules:
        if len(old) != len(new):
            sys.exit(f"[!] length mismatch: {old!r} ({len(old)}) -> {new!r} ({len(new)}). Must be equal.")
    return rules


def make_regex(old, exact):
    o = re.escape(old)
    if exact:
        return re.compile(rb"(?<![" + HOST_CHARS + rb".])" + o + rb"(?![" + HOST_CHARS + rb"])")
    # suffix: must be preceded by a dot (subdomain) or a non-host char, and end the host
    return re.compile(rb"(?<![" + HOST_CHARS + rb"])" + o + rb"(?![" + HOST_CHARS + rb".]?[A-Za-z0-9])")


def full_host_at(data, start, end):
    s = start
    while s > 0 and (chr(data[s - 1]).isalnum() or data[s - 1] in b".-"):
        s -= 1
    return data[s:end]


def patch_bytes(data, rules, only_hosts, log, label, utf16=False):
    data = bytearray(data)
    count = 0
    for old, new, exact in rules:
        o, n = old, new
        if utf16:
            o, n = old.decode().encode("utf-16-le"), new.decode().encode("utf-16-le")
            rx = re.compile(re.escape(o))
        else:
            rx = make_regex(o, exact)
        for m in list(rx.finditer(bytes(data))):
            if not utf16 and only_hosts:
                h = full_host_at(data, m.start(), m.end()).decode("latin-1")
                if h not in only_hosts:
                    continue
            data[m.start():m.end()] = n
            count += 1
            if not utf16:
                log.append(f"{label}@{m.start():#x}: {full_host_at(data, m.start(), m.end()).decode('latin-1')}")
    return bytes(data), count


# ---------------------------------------------------------------- dex helpers
def uleb(d, p):
    r = s = 0
    while True:
        b = d[p]
        p += 1
        r |= (b & 0x7F) << s
        s += 7
        if b < 0x80:
            return r, p


def dex_strings(d):
    n, off = struct.unpack_from("<II", d, 0x38)
    out = []
    for i in range(n):
        so = struct.unpack_from("<I", d, off + 4 * i)[0]
        _, p = uleb(d, so)
        e = d.index(b"\x00", p)
        out.append(d[p:e])
    return out


def mutf8_key(b):
    # ART orders string_ids by UTF-16 code units. MUTF-8: NUL is C0 80, supplementary
    # chars are CESU-8 surrogate pairs -> surrogatepass gives us the raw code units.
    s = b.replace(b"\xc0\x80", b"\x00").decode("utf-8", "surrogatepass")
    return s.encode("utf-16-be", "surrogatepass")


def fix_dex(d):
    d = bytearray(d)
    d[12:32] = hashlib.sha1(bytes(d[32:])).digest()
    d[8:12] = struct.pack("<I", zlib.adler32(bytes(d[12:])) & 0xFFFFFFFF)
    return bytes(d)


def patch_dex(name, data, rules, only_hosts, log):
    new, c = patch_bytes(data, rules, only_hosts, log, name)
    if not c:
        return data, 0
    old_strs, strs = dex_strings(data), dex_strings(new)
    changed = [i for i, (a, b) in enumerate(zip(old_strs, strs)) if a != b]
    bad = []
    for i in changed:
        for j in (i - 1, i + 1):
            if 0 <= j < len(strs):
                lo, hi = (j, i) if j < i else (i, j)
                if mutf8_key(strs[lo]) >= mutf8_key(strs[hi]):
                    bad.append(hi)
    if bad:
        i = bad[0]
        print(f"[!] {name}: string order broken ({strs[i-1][:60]!r} >= {strs[i][:60]!r}); "
              f"dex left UNPATCHED - use apktool/smali route for this one")
        return data, 0
    return fix_dex(new), c


# ---------------------------------------------------------------- repack
def write_aligned(zin, zout, infos_data):
    for info, data in infos_data:
        zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        zi.external_attr = info.external_attr
        zi.compress_type = info.compress_type
        if zi.compress_type == zipfile.ZIP_STORED:
            align = 4096 if info.filename.endswith(".so") else 4
            hdr = 30 + len(info.filename.encode())
            pos = zout.fp.tell()
            pad = (-(pos + hdr)) % align
            if pad and pad < 4:
                pad += align
            # 0xD935 = Android zipalign extra-field id
            zi.extra = struct.pack("<HH", 0xD935, pad - 4) + b"\x00" * (pad - 4) if pad else b""
        zout.writestr(zi, data)


def main():
    cfg_path, src, dst = sys.argv[1:4]
    cfg = json.load(open(cfg_path))
    rules = build_rules(cfg)
    only = set(cfg.get("only_hosts", []))
    log, total = [], 0
    zin = zipfile.ZipFile(src)
    out_items = []
    for info in zin.infolist():
        n = info.filename
        if n.startswith("META-INF/") and n.upper().endswith((".SF", ".RSA", ".DSA", ".EC", "MANIFEST.MF")):
            continue
        data = zin.read(n)
        c = 0
        if re.fullmatch(r"classes\d*\.dex", n):
            data, c = patch_dex(n, data, rules, only, log)
        elif n.endswith(".so") or n.startswith(("assets/", "res/raw/")) or n.endswith((".properties", ".json", ".xml", ".cfg", ".txt")):
            if n.startswith("res/") and n.endswith(".xml") and not n.startswith("res/raw/"):
                pass  # binary AXML: strings are UTF-16 in a pool, handled via arsc rule below if needed
            else:
                data, c = patch_bytes(data, rules, only, log, n)
        elif n == "resources.arsc":
            data, c8 = patch_bytes(data, rules, only, log, n)
            data, c16 = patch_bytes(data, rules, only, log, n, utf16=True)
            c = c8 + c16
        if c:
            print(f"[+] {n}: {c} replacement(s)")
        total += c
        out_items.append((info, data))
    with zipfile.ZipFile(dst, "w") as zout:
        write_aligned(zin, zout, out_items)
    open(dst + ".patchlog.txt", "w").write("\n".join(log))
    print(f"[=] {total} replacements -> {dst}  (details: {dst}.patchlog.txt)")
    print("[=] Unsigned. Next: tools/sign_apk.ps1")


if __name__ == "__main__":
    main()
