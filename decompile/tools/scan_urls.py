"""Scan an unpacked APK tree for hardcoded API hosts / URLs.

Usage:  python -I scan_urls.py <apk_unzip_dir> <out_json>

Finds http(s) URLs, bare hostnames on NetEase-ish / game domains, and IPv4
literals in every file (dex, so, xml, json, cfg, txt...). Records file, byte
offset and the exact string so patch_hosts.py can do same-length replacement.
"""
import json
import os
import re
import sys
from collections import defaultdict

URL_RE = re.compile(rb"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]{3,200}")
HOST_RE = re.compile(
    rb"(?<![A-Za-z0-9.-])((?:[A-Za-z0-9-]{1,63}\.)+"
    rb"(?:netease\.com|163\.com|126\.net|easebar\.com|nie\.easebar\.com|"
    rb"netease\.im|ntes53\.netease\.com|rulesofsurvivalgame\.com|"
    rb"neteasegames\.com|update\.netease\.com|nie\.netease\.com|"
    rb"easebar\.com|gameyw\.netease\.com|unisdk\.easebar\.com|"
    rb"proxima\.nie\.easebar\.com|appdump\.nosdn\.127\.net|127\.net|"
    rb"ntes\.com|ludashi\.com|nosdn\.127\.net|163yun\.com|netease\.org))"
    rb"(?![A-Za-z0-9-])"
)
IP_RE = re.compile(rb"(?<![0-9.])((?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3})(?::\d{2,5})?(?![0-9.])")

SKIP_IPS = {b"0.0.0.0", b"127.0.0.1", b"255.255.255.255", b"1.0.0.0"}


def scan_file(path):
    try:
        data = open(path, "rb").read()
    except OSError:
        return []
    hits = []
    for m in URL_RE.finditer(data):
        hits.append(("url", m.start(), m.group(0)))
    for m in HOST_RE.finditer(data):
        hits.append(("host", m.start(1), m.group(1)))
    # dex strings are MUTF-8 so plain ascii works; also catch UTF-16LE (resources.arsc)
    if path.endswith(".arsc"):
        try:
            u = data.decode("utf-16-le", "ignore").encode("ascii", "ignore")
            for m in URL_RE.finditer(u):
                hits.append(("url16", -1, m.group(0)))
        except Exception:
            pass
    for m in IP_RE.finditer(data):
        ip = m.group(1)
        if ip in SKIP_IPS or ip.count(b".") != 3:
            continue
        # ignore version-like strings (x.y.z.w with small numbers in .so)
        parts = [int(p) for p in ip.split(b".")]
        if parts[0] < 10:
            continue
        hits.append(("ip", m.start(), m.group(0)))
    return hits


def main():
    root, out = sys.argv[1], sys.argv[2]
    results = []
    by_host = defaultdict(set)
    for dp, _, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, root).replace("\\", "/")
            for kind, off, s in scan_file(p):
                txt = s.decode("latin-1")
                results.append({"file": rel, "kind": kind, "offset": off, "value": txt})
                host = re.sub(r"^https?://", "", txt).split("/")[0].split(":")[0]
                by_host[host].add(rel)
    summary = {h: sorted(f) for h, f in sorted(by_host.items())}
    json.dump({"hits": results, "hosts": summary}, open(out, "w"), indent=1)
    print(f"{len(results)} hits, {len(summary)} unique hosts -> {out}")


if __name__ == "__main__":
    main()
