import os
import sys
import plistlib
import struct
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from test_etc1_fast import encode_etc1_fast, make_pkm
import render_perfect_assets

def build_ui_login_en():
    base_dir = os.path.dirname(__file__)
    print("Building ui_login_en patch...")
    orig_path = os.path.join(base_dir, "ui_login_en_original.png")
    atlas = Image.open(orig_path).convert("RGBA")
    w, h = atlas.size
    print(f"Loaded original ui_login_en atlas: {w}x{h}")
    
    # 1. Generate modern logo and play button
    logo = render_perfect_assets.create_modern_logo_master()
    play = render_perfect_assets.create_modern_play_btn_master()
    
    # 2. Rotate logo 270 deg clockwise (90 deg CCW) for Cocos rotated format
    # Logo size is 502x317 -> rotated is 317x502
    logo_rotated = logo.rotate(270, expand=True)
    assert logo_rotated.size == (317, 502), f"Expected (317, 502), got {logo_rotated.size}"
    assert play.size == (838, 159), f"Expected (838, 159), got {play.size}"
    
    # 3. Clear target regions first (transparent)
    # img_login_logo_en_ui_login: (79, 1434, 79+317, 1434+502)
    blank_logo = Image.new("RGBA", (317, 502), (0, 0, 0, 0))
    atlas.paste(blank_logo, (79, 1434))
    atlas.paste(logo_rotated, (79, 1434), logo_rotated)
    
    # img_login_logo1_en_ui_login: (398, 396, 398+317, 396+502)
    atlas.paste(blank_logo, (398, 396))
    atlas.paste(logo_rotated, (398, 396), logo_rotated)
    
    # txt_enter_game_en_ui_login: (1, 1, 1+838, 1+159)
    blank_play = Image.new("RGBA", (838, 159), (0, 0, 0, 0))
    atlas.paste(blank_play, (1, 1))
    atlas.paste(play, (1, 1), play)
    
    patch_dir = os.path.join(base_dir, "patch_res")
    os.makedirs(patch_dir, exist_ok=True)
    
    # 4. Save PNG
    png_out = os.path.join(patch_dir, "ui_login_en.png")
    atlas.save(png_out, "PNG")
    print(f"Saved {png_out}")
    
    # 5. Encode RGB PKM
    rgb_img = atlas.convert("RGB")
    print("Encoding ui_login_en.pkm (ETC1 RGB)...")
    etc_rgb = encode_etc1_fast(rgb_img)
    pkm_rgb = make_pkm(etc_rgb, w, h)
    pkm_out = os.path.join(patch_dir, "ui_login_en.pkm")
    with open(pkm_out, "wb") as f:
        f.write(pkm_rgb)
    print(f"Saved {pkm_out} ({len(pkm_rgb)} bytes)")
    
    # 6. Encode Alpha PKM
    alpha = atlas.split()[3]
    alpha_rgb = Image.merge("RGB", (alpha, alpha, alpha))
    print("Encoding ui_login_en.alpha.pkm (ETC1 Alpha)...")
    etc_alpha = encode_etc1_fast(alpha_rgb)
    pkm_alpha = make_pkm(etc_alpha, w, h)
    alpha_pkm_out = os.path.join(patch_dir, "ui_login_en.alpha.pkm")
    with open(alpha_pkm_out, "wb") as f:
        f.write(pkm_alpha)
    print(f"Saved {alpha_pkm_out} ({len(pkm_alpha)} bytes)")
    
    # 7. Copy plist
    plist_in = os.path.join(base_dir, "ui_login_en.plist")
    plist_out = os.path.join(patch_dir, "ui_login_en.plist")
    with open(plist_in, "rb") as f:
        plist_data = f.read()
    with open(plist_out, "wb") as f:
        f.write(plist_data)
    print(f"Saved {plist_out}")

if __name__ == "__main__":
    build_ui_login_en()
