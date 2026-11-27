"""Rewrite the .lan test hosts inside an apktool-decoded tree to a real domain (same length, byte level).

  python -I rewrite_hosts.py <decoded_dir> [domain=vokdev.com]

Rules (all same length, so they are safe in .so / assets / smali alike):
  <label>.easebar.lan  -> <label>e.vokdev.com      (".easebar.lan" 12 -> "e.vokdev.com" 12)
  <label>.netease.lan  -> <label>n.vokdev.com
  www.rulesofsurvivalgame.lan -> wwwrulesofsurviv.vokdev.com   (27 chars)
Every result is a subdomain of the domain, so one wildcard DNS record (*.vokdev.com) serves them all.
"""
import os, re, sys

root = sys.argv[1]
dom = sys.argv[2] if len(sys.argv) > 2 else "vokdev.com"
HC = rb"A-Za-z0-9-"


def rule(old, new):
    assert len(old) == len(new), (old, new)
    return re.compile(rb"(?<=[" + HC + rb"])" + re.escape(old) + rb"(?![" + HC + rb"])"), new


# the domain must be exactly 10 chars ("vokdev.com") for the 12-char rule to fit
suffix = "." + dom
pad_e = "e" + suffix
pad_n = "n" + suffix
rules = [
    rule(b".easebar.lan", pad_e.encode()),
    rule(b".netease.lan", pad_n.encode()),
]
www_old = b"www.rulesofsurvivalgame.lan"
www_new = ("w" * 3 + "rulesofsurviv").encode()[: len(www_old) - len(suffix)] + suffix.encode()
rules.append((re.compile(re.escape(www_old)), www_new))
assert len(www_new) == len(www_old), (www_new, len(www_new))

total = 0
bare = {}
for dp, dn, fn in os.walk(root):
    if os.sep + "original" in dp + os.sep and dp.startswith(os.path.join(root, "original")):
        continue
    for f in fn:
        p = os.path.join(dp, f)
        try:
            d = open(p, "rb").read()
        except OSError:
            continue
        if b".lan" not in d:
            continue
        o = d
        for rx, new in rules:
            d = rx.sub(new, d)
        for m in re.finditer(rb"(?<![A-Za-z0-9.-])(?:easebar|netease|rulesofsurvivalgame)\.lan", d):
            bare[os.path.relpath(p, root)] = bare.get(os.path.relpath(p, root), 0) + 1
        if d != o:
            open(p, "wb").write(d)
            n = sum(len(rx.findall(o)) for rx, _ in rules)
            total += n
            print(f"[+] {os.path.relpath(p, root)}: {n}")
print(f"[=] {total} host rewrites")
if bare:
    print("[!] bare (no subdomain) hosts left unpatched:")
    for k, v in sorted(bare.items()):
        print("   ", k, v)
