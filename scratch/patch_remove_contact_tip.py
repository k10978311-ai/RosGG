"""
Patch and remove/customize the 'Please contact us: gamerulesofsurvival@global.netease.com...'
text from client scripts (Account.nxs) and deploy to emulator / phone.
"""

import os
import sys
import zlib
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "decompile", "tools"))
from neox_marshal import Reader, xs
from npk_decrypt import FastRotor, KEY_FILE, reverse_string, unreverse_string


def patch_account_nxs(custom_text=None):
    base_dir = os.path.dirname(__file__)
    src_nxs = os.path.join(base_dir, "..", "decompile", "script", "patched", "nxs", "entities", "Account.nxs")
    if not os.path.exists(src_nxs):
        print(f"Error: {src_nxs} does not exist.")
        return None

    with open(src_nxs, "rb") as f:
        enc = f.read()

    fr = FastRotor(open(KEY_FILE, encoding="latin-1").read(), len(enc) + 65536)
    code = reverse_string(zlib.decompress(fr.decrypt(enc)))
    r = Reader(code)
    top = r.obj()

    buf = bytearray(code)
    replaced = 0
    for off, n, t in r.spans:
        plain = xs(bytes(buf[off:off + n]))
        if b"gamerulesofsurvival" in plain.lower():
            if custom_text is None:
                # Blank out with spaces
                new_str = b" " * len(plain)
            else:
                raw_bytes = custom_text.encode("utf-8")
                # Pad or truncate to exact length
                if len(raw_bytes) < len(plain):
                    new_str = raw_bytes.ljust(len(plain), b" ")
                else:
                    new_str = raw_bytes[:len(plain)]
            buf[off:off + n] = xs(new_str)
            print(f"[*] Replaced at offset {off}:\n    Old: {plain.decode('latin-1')}\n    New: {new_str.decode('latin-1')}")
            replaced += 1

    if replaced == 0:
        print("[!] No matching strings found to replace.")
        return None

    new_code = bytes(buf)
    Reader(new_code).obj()  # verify round-trip
    new_enc = fr.encrypt(zlib.compress(unreverse_string(new_code), 9))

    out_file = os.path.join(base_dir, "Account_patched.nxs")
    with open(out_file, "wb") as f:
        f.write(new_enc)
    print(f"[+] Successfully wrote patched file to {out_file}")
    return out_file


def deploy_to_device(nxs_file, serial="emulator-5554"):
    adb = "C:/LDPlayer/LDPlayer9/adb.exe"
    if not os.path.exists(adb):
        adb = "adb"

    remote_base = "/storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na"
    target_dirs = [
        f"{remote_base}/res/nxs/entities",
        f"{remote_base}/res/entities",
        f"{remote_base}/Documents/res/nxs/entities",
        f"{remote_base}/Documents/res/entities",
    ]

    for d in target_dirs:
        try:
            subprocess.run([adb, "-s", serial, "shell", f"mkdir -p {d}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run([adb, "-s", serial, "push", nxs_file, f"{d}/Account.nxs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[+] Deployed Account.nxs -> {d}/Account.nxs")
        except Exception as e:
            print(f"[-] Failed to push to {d}: {e}")


if __name__ == "__main__":
    custom = sys.argv[1] if len(sys.argv) > 1 else None
    patched = patch_account_nxs(custom)
    if patched:
        deploy_to_device(patched)
