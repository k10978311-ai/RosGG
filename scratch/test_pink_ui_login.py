import os
import sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from test_etc1_fast import encode_etc1_fast, make_pkm

def make_pink_ui_login_en():
    print("Making solid pink ui_login_en to see what changes on screen...")
    # 2048x2048 solid magenta
    pink = Image.new("RGBA", (2048, 2048), (255, 0, 128, 255))
    pink.save("scratch/patch_res/ui_login_en.png", "PNG")
    
    etc_rgb = encode_etc1_fast(pink.convert("RGB"))
    with open("scratch/patch_res/ui_login_en.pkm", "wb") as f:
        f.write(make_pkm(etc_rgb, 2048, 2048))
        
    alpha = pink.split()[3]
    etc_alpha = encode_etc1_fast(Image.merge("RGB", (alpha, alpha, alpha)))
    with open("scratch/patch_res/ui_login_en.alpha.pkm", "wb") as f:
        f.write(make_pkm(etc_alpha, 2048, 2048))
        
    print("Generated solid pink ui_login_en texture!")

if __name__ == "__main__":
    make_pink_ui_login_en()
