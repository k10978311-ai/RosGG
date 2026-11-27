"""Hide the hall "ROS2.0 IS COMING" banner (UIMain bottom-right panel_new_playmode_activty).

    python -I tools/patch_hide_ros2_banner.py script/script.npk script/patched

UIMain.onInitMainActivityEnter (NeoX-remapped opcodes, decoded by hand):
    modePanel.setVisible(False)
    if ros2_common.isInRos2CashExchangeActiviy(): actCfg = client_utils.getEnableMainActivityCfg()
    else:                                         actCfg = legacyProperties.getMainActivityEnterData(2)
    if actCfg is None:                            # offset 100: 5d 05 00 = LOAD_FAST actCfg
        modePanel.setVisible(False); return
    ... loads textures, binds ROS2 mode button, modePanel.setVisible(True)
Patch: offset 100 LOAD_FAST actCfg -> LOAD_CONST None (65 00 00), so the panel stays hidden.
Same length, so the marshal layout is untouched. Output: <out>/nxs/ui/UIMain.nxs (loose override).
Undo: delete ui/UIMain.nxs from the device's loose script dir.
"""
import os
import sys
import zlib

sys.path.insert(0, os.path.dirname(__file__))
from neox_marshal import Reader, xs  # noqa: E402
from npk_decrypt import FastRotor, KEY_FILE, read_index, reverse_string, unreverse_string  # noqa: E402

UIMAIN_SIGN = 0x45840296
FUNC = b"onInitMainActivityEnter"
OFF, OLD, NEW = 100, bytes.fromhex("5d0500"), bytes.fromhex("650000")


def main():
    npk, out = sys.argv[1:3]
    d = open(npk, "rb").read()
    entries = read_index(d)
    e = next(x for x in entries if x[0] == UIMAIN_SIGN)
    fr = FastRotor(open(KEY_FILE, encoding="latin-1").read(), max(x[2] for x in entries) + 65536)
    code = reverse_string(zlib.decompress(fr.decrypt(d[e[1]:e[1] + e[2]])))

    r = Reader(code)
    top = r.obj()
    assert top.filename.replace(b"\\", b"/").endswith(b"ui/UIMain.py"), top.filename
    fn = [c for c in top.walk() if c.name == FUNC]
    assert len(fn) == 1, len(fn)
    co = fn[0].code
    assert co[OFF:OFF + 3] == OLD, co[OFF:OFF + 3].hex()
    assert fn[0].varnames[5] == b"actCfg" and fn[0].consts[0] is None
    spans = [(o, n) for o, n, t in r.spans if n == len(co) and xs(code[o:o + n]) == co]
    assert len(spans) == 1, spans
    o, n = spans[0]
    new_co = co[:OFF] + NEW + co[OFF + 3:]
    buf = bytearray(code)
    buf[o:o + n] = xs(new_co)
    new = bytes(buf)

    chk = [c for c in Reader(new).obj().walk() if c.name == FUNC][0]
    assert chk.code == new_co
    enc = fr.encrypt(zlib.compress(unreverse_string(new), 9))
    assert reverse_string(zlib.decompress(fr.decrypt(enc))) == new
    dst = os.path.join(out, "nxs", "ui", "UIMain.nxs")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "wb").write(enc)
    print("wrote", dst)


if __name__ == "__main__":
    main()
