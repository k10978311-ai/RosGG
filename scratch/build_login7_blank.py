import os
import plistlib
import struct
from PIL import Image

def build_login7_blank():
    print("Building blank login7 patch (to suppress legacy monkey king animations)...")
    w, h = 2048, 2048
    
    # 1. 2048x2048 fully transparent RGBA
    blank = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    blank_png = "scratch/patch_res/login7.png"
    blank.save(blank_png, "PNG")
    print(f"Saved {blank_png}")
    
    # 2. PKM header + empty data
    # ETC1 block of (0,0,0) is all zeros: 8 bytes per 4x4 block
    total_blocks = (w // 4) * (h // 4)
    etc1_data = bytes(total_blocks * 8)
    
    header = struct.pack('>6sHHHHH', b'PKM 10', 0, w, h, w, h)
    pkm = header + etc1_data
    
    with open("scratch/patch_res/login7.pkm", "wb") as f:
        f.write(pkm)
    print(f"Saved scratch/patch_res/login7.pkm ({len(pkm)} bytes)")
    
    with open("scratch/patch_res/login7.alpha.pkm", "wb") as f:
        f.write(pkm)
    print(f"Saved scratch/patch_res/login7.alpha.pkm ({len(pkm)} bytes)")
    
    # 3. Copy plist
    plist_src = "scratch/login_extracted/out_game_ui_login_loginpanel_login7.plist"
    with open(plist_src, "rb") as f:
        pl_data = f.read()
    with open("scratch/patch_res/login7.plist", "wb") as f:
        f.write(pl_data)
    print("Saved scratch/patch_res/login7.plist")

if __name__ == "__main__":
    build_login7_blank()
