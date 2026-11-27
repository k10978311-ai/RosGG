import os
import struct
import numpy as np
from PIL import Image
from test_etc1_fast import encode_etc1_fast, make_pkm

def build_login6():
    orig_path = "scratch/login6_original.png"
    banner_path = "scratch/ros_banner_clean.jpg"
    
    orig = Image.open(orig_path).convert("RGBA")
    banner = Image.open(banner_path).convert("RGBA")
    
    # 1. Prepare crops/resizes for the two frames in login6:
    # Frame 'img_login_xiyou.png': frame {{2, 979}, {1580, 960}}
    banner_xiyou = banner.resize((1580, 960), Image.Resampling.LANCZOS)
    
    # Frame 'vx_giant/bg.png': frame {{2, 2}, {1580, 973}}
    banner_giant = banner.resize((1580, 973), Image.Resampling.LANCZOS)
    
    # 2. Composite onto 2048x2048 atlas
    atlas = orig.copy()
    atlas.paste(banner_giant, (2, 2))
    atlas.paste(banner_xiyou, (2, 979))
    
    os.makedirs("scratch/patch_res", exist_ok=True)
    atlas.save("scratch/patch_res/login6.png", "PNG")
    print("Saved scratch/patch_res/login6.png")
    
    # 3. Encode RGB to PKM (ETC1)
    print("Encoding RGB to ETC1 PKM (2048x2048)...")
    rgb_img = atlas.convert("RGB")
    rgb_etc1 = encode_etc1_fast(rgb_img)
    rgb_pkm = make_pkm(rgb_etc1, 2048, 2048)
    with open("scratch/patch_res/login6.pkm", "wb") as f:
        f.write(rgb_pkm)
    print("Saved scratch/patch_res/login6.pkm (size:", len(rgb_pkm), "bytes)")
    
    # 4. Encode Alpha to PKM (ETC1)
    print("Encoding Alpha to ETC1 PKM (2048x2048)...")
    r, g, b, a = atlas.split()
    alpha_rgb = Image.merge("RGB", (a, a, a))
    alpha_etc1 = encode_etc1_fast(alpha_rgb)
    alpha_pkm = make_pkm(alpha_etc1, 2048, 2048)
    with open("scratch/patch_res/login6.alpha.pkm", "wb") as f:
        f.write(alpha_pkm)
    print("Saved scratch/patch_res/login6.alpha.pkm (size:", len(alpha_pkm), "bytes)")
    
    # 5. Copy login6.plist as well
    plist_src = "scratch/login_extracted/out_game_ui_login_loginpanel_login6.plist"
    with open(plist_src, "rb") as f:
        plist_data = f.read()
    with open("scratch/patch_res/login6.plist", "wb") as f:
        f.write(plist_data)
    print("Saved scratch/patch_res/login6.plist")

if __name__ == "__main__":
    build_login6()
