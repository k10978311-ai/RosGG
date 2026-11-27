"""Refit LDPlayer's RoS keymap to the 1.610637 in-match HUD (1600x900).

Reads the stock recommend config, moves each key onto the button measured
from an adb screencap, and writes it to vms/customizeConfigs (which LDPlayer
prefers over recommendConfigs). Re-run after changing positions below.
"""
import copy
import json
import os
import shutil

LD = r"C:\LDPlayer\LDPlayer9\vms"
SRC = os.path.join(LD, "recommendConfigs", "RULES OF SURVIVAL.kmp")
DST = os.path.join(LD, "customizeConfigs", "RULES OF SURVIVAL.kmp")
W, H = 1600, 900

# key code -> (x, y) in screen pixels at 1600x900
TAPS = {
    32: (1453, 597),   # Space  jump
    67: (1455, 712),   # C      crouch
    90: (1197, 843),   # Z      prone
    82: (1084, 840),   # R      reload (ammo icon)
    86: (1457, 838),   # V      change angle
    81: (1282, 572),   # Q      action button left of jump
    49: (1315, 105),   # 1      weapon slot 1
    50: (1315, 185),   # 2      weapon slot 2
    51: (1468, 185),   # 3      slot 3
    52: (1468, 253),   # 4      slot 4 (throwable)
    88: (1468, 100),   # X      fist / holster
    155: (1315, 105),  # wheel up   -> slot 1
    154: (1315, 185),  # wheel down -> slot 2
    89: (1360, 313),   # Y      speaker toggle
    84: (1424, 313),   # T      mic toggle
    54: (1288, 313),   # 6      quick chat
    187: (1485, 362),  # =      skateboard / slide button
}
MACROS = {  # key -> single-tap macro target (keeps mouse released)
    9: (400, 843),     # Tab   backpack
    77: (228, 150),    # M     map
    20: (1483, 313),   # Caps  auto-run
}
DROP = {66}            # B: old two-slot macro, no matching button now


def n(x, y):
    return {"x": round(x / W * 10000), "y": round(y / H * 10000)}


def main():
    d = json.load(open(SRC, encoding="utf-8-sig"))
    out = []
    for m in d["keyboardMappings"]:
        m = copy.deepcopy(m)
        cls, data = m["class"], m["data"]
        key = data.get("key")
        if key in DROP:
            continue
        if cls == "ClassKeyboardDisc":            # WASD joystick
            data["origin"] = n(348, 660)
            data["radius"] = 1150
        elif cls == "ClassMouseTrigger":          # left click = fire
            data["point"] = n(1310, 703)
        elif cls == "ClassMouseODisc":            # Alt = free look (eye)
            data["origin"] = n(1160, 313)
        elif cls == "ClassKeyboardCurve" and key in TAPS:
            p = n(*TAPS[key])
            for pt in data["curve"]:
                pt["x"], pt["y"] = p["x"], p["y"]
        elif cls == "ClassKeyboardMacros" and key in MACROS:
            x, y = MACROS[key]
            data["origin"] = n(x, y)
            data["macros"] = f"size {W} {H}\rtouch {x} {y}\rwait 50\rswitch-mouse\r"
        out.append(m)

    have = {m["data"].get("key") for m in out}
    for key in ("81",):  # add Q if the stock map lacked it
        k = int(key)
        if k not in have:
            p = n(*TAPS[k])
            out.append({"class": "ClassKeyboardCurve", "data": {
                "key": k, "secondKey": 0,
                "curve": [dict(p, timing=0), dict(p, timing=60)],
                "extraData": "", "description": "", "moreDescription": "",
                "hintVisible": True, "hintOffset": {"x": 0, "y": 0}}})

    d["keyboardMappings"] = out
    if os.path.exists(DST):
        shutil.copy2(DST, DST + ".bak")
    with open(DST, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print(f"wrote {DST} ({len(out)} mappings)")


if __name__ == "__main__":
    main()
