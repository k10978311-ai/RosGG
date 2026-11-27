import os
import sys
import plistlib
import struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from test_etc1_fast import encode_etc1_fast, make_pkm
import render_perfect_assets

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_path_title = "C:/Windows/Fonts/bahnschrift.ttf"
font_path_bold = "C:/Windows/Fonts/segoeuib.ttf"
if not os.path.exists(font_path_title):
    font_path_title = "C:/Windows/Fonts/arialbd.ttf"
if not os.path.exists(font_path_bold):
    font_path_bold = "C:/Windows/Fonts/arialbd.ttf"

def render_rku_logo(width=378, height=332):
    """
    Render modern 3D beveled metallic logo for RKU-LOGO (378x332).
    Fits the original RKU-LOGO.png frame on login6.plist.
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    f_rules = get_font(font_path_title, 44)
    f_of = get_font(font_path_bold, 17)
    f_survival = get_font(font_path_title, 52)
    f_sub = get_font(font_path_bold, 14)
    f_badge = get_font(font_path_bold, 11)
    
    # 1. Top Cyber Badge
    bw, bh = 260, 24
    bx1 = width // 2 - bw // 2
    by1 = 15
    bx2 = bx1 + bw
    by2 = by1 + bh
    draw.rounded_rectangle([bx1 - 2, by1 - 2, bx2 + 2, by2 + 2], radius=6, fill=(0, 200, 255, 40))
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=5, fill=(12, 22, 38, 245), outline=(0, 210, 255, 230), width=2)
    
    badge_txt = "★   BATTLE ROYALE 2.0   ★"
    tw = draw.textlength(badge_txt, font=f_badge)
    draw.text((width // 2 - tw / 2, by1 + 4), badge_txt, font=f_badge, fill=(0, 235, 255, 255))
    
    # 2. Main Title: "RULES OF"
    rx = width // 2 - 145
    ry = 55
    render_perfect_assets.draw_beveled_text(
        draw, (rx, ry), "RULES", font=f_rules, fill_color=(252, 253, 255, 255),
        bevel_light=(255, 255, 255, 255), bevel_dark=(30, 45, 70, 255),
        shadow_color=(5, 12, 24, 250), shadow_dist=4
    )
    
    # "OF" badge
    of_x = width // 2 + 80
    of_y = 66
    draw.rounded_rectangle([of_x, of_y, of_x + 46, of_y + 30], radius=5, fill=(20, 35, 60, 240), outline=(255, 195, 30, 240), width=2)
    draw.text((of_x + 10, of_y + 5), "OF", font=f_of, fill=(255, 215, 60, 255))
    
    # 3. Main Title: "SURVIVAL"
    sx = width // 2 - 155
    sy = 115
    render_perfect_assets.draw_beveled_text(
        draw, (sx, sy), "SURVIVAL", font=f_survival, fill_color=(255, 255, 255, 255),
        bevel_light=(255, 255, 255, 255), bevel_dark=(35, 45, 65, 255),
        shadow_color=(5, 12, 24, 250), shadow_dist=5
    )
    
    # 4. Tactical Accent Line
    line_y = 188
    draw.line([(width // 2 - 160, line_y), (width // 2 - 40, line_y)], fill=(255, 195, 30, 220), width=2)
    draw.line([(width // 2 + 40, line_y), (width // 2 + 160, line_y)], fill=(255, 195, 30, 220), width=2)
    draw.polygon([(width // 2, line_y - 5), (width // 2 + 6, line_y), (width // 2, line_y + 5), (width // 2 - 6, line_y)], fill=(255, 215, 60, 255))
    
    # 5. Modern Subtitle
    sub_txt = "PRIVATE SERVER EDITION"
    sw = draw.textlength(sub_txt, font=f_sub)
    draw.text((width // 2 - sw / 2 + 2, 202 + 2), sub_txt, font=f_sub, fill=(5, 12, 24, 240))
    draw.text((width // 2 - sw / 2, 202), sub_txt, font=f_sub, fill=(240, 245, 255, 255))
    
    # 6. Sleek lower carbon badge replacing the old Ravelo Komiks Universe logo
    box_w, box_h = 320, 50
    bx1 = width // 2 - box_w // 2
    by1 = 240
    bx2 = bx1 + box_w
    by2 = by1 + box_h
    draw.rounded_rectangle([bx1 - 2, by1 - 2, bx2 + 2, by2 + 2], radius=8, fill=(255, 195, 30, 50))
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill=(16, 26, 42, 240), outline=(255, 195, 30, 230), width=2)
    
    box_txt = "TACTICAL BATTLE ROYALE"
    f_box = get_font(font_path_title, 20)
    tw = draw.textlength(box_txt, font=f_box)
    draw.text((width // 2 - tw / 2, by1 + 12), box_txt, font=f_box, fill=(255, 215, 50, 255))
    
    return img

def patch_login6_with_logo():
    print("Patching login6 atlas with new RKU-LOGO...")
    # Load current login6.png
    login6_path = "scratch/patch_res/login6.png"
    atlas = Image.open(login6_path).convert("RGBA")
    w, h = atlas.size
    
    # RKU-LOGO.png frame: {{1586, 2}, {378, 332}}
    logo = render_rku_logo(378, 332)
    logo.save("scratch/patch_res/rku_logo_modern.png")
    
    # Clear old logo region
    blank = Image.new("RGBA", (378, 332), (0, 0, 0, 0))
    atlas.paste(blank, (1586, 2))
    # Paste new modern logo
    atlas.paste(logo, (1586, 2), logo)
    
    # Save PNG
    atlas.save("scratch/patch_res/login6.png", "PNG")
    print("Saved scratch/patch_res/login6.png")
    
    # Re-encode ETC1 RGB
    print("Encoding login6.pkm (ETC1 RGB)...")
    etc_rgb = encode_etc1_fast(atlas.convert("RGB"))
    pkm_rgb = make_pkm(etc_rgb, w, h)
    with open("scratch/patch_res/login6.pkm", "wb") as f:
        f.write(pkm_rgb)
    print("Saved scratch/patch_res/login6.pkm")
    
    # Re-encode ETC1 Alpha
    print("Encoding login6.alpha.pkm (ETC1 Alpha)...")
    alpha = atlas.split()[3]
    alpha_rgb = Image.merge("RGB", (alpha, alpha, alpha))
    etc_alpha = encode_etc1_fast(alpha_rgb)
    pkm_alpha = make_pkm(etc_alpha, w, h)
    with open("scratch/patch_res/login6.alpha.pkm", "wb") as f:
        f.write(pkm_alpha)
    print("Saved scratch/patch_res/login6.alpha.pkm")

def patch_login_atlas_with_play_and_logo():
    print("Patching login atlas with new PLAY button and clean website bar...")
    login_path = "scratch/login_atlas_decoded.png"
    atlas = Image.open(login_path).convert("RGBA")
    w, h = atlas.size
    
    # 1. Modern PLAY button: {{505, 1}, {838, 159}}
    play_btn = render_perfect_assets.create_modern_play_btn_master()
    blank_play = Image.new("RGBA", (838, 159), (0, 0, 0, 0))
    atlas.paste(blank_play, (505, 1))
    atlas.paste(play_btn, (505, 1), play_btn)
    print("Pasted new PLAY button at (505, 1)")
    
    # 2. Modern Title Logo: txt_logo_zjzc: {{505, 162}, {406, 306}}
    logo_zjzc = render_rku_logo(406, 306)
    blank_logo = Image.new("RGBA", (406, 306), (0, 0, 0, 0))
    atlas.paste(blank_logo, (505, 162))
    atlas.paste(logo_zjzc, (505, 162), logo_zjzc)
    print("Pasted new logo at (505, 162)")
    
    # 3. Transparent website bar: panel_bg_txt01: {{1979, 1}, {689, 56}}, rotated True -> (56, 689) on atlas
    blank_badge = Image.new("RGBA", (56, 689), (0, 0, 0, 0))
    atlas.paste(blank_badge, (1979, 1))
    print("Cleared panel_bg_txt01 at (1979, 1) to transparent")
    
    # Save PNG
    atlas.save("scratch/patch_res/login.png", "PNG")
    print("Saved scratch/patch_res/login.png")
    
    # Encode ETC1 RGB
    print("Encoding login.pkm (ETC1 RGB)...")
    etc_rgb = encode_etc1_fast(atlas.convert("RGB"))
    pkm_rgb = make_pkm(etc_rgb, w, h)
    with open("scratch/patch_res/login.pkm", "wb") as f:
        f.write(pkm_rgb)
    print("Saved scratch/patch_res/login.pkm")
    
    # Encode ETC1 Alpha
    print("Encoding login.alpha.pkm (ETC1 Alpha)...")
    alpha = atlas.split()[3]
    alpha_rgb = Image.merge("RGB", (alpha, alpha, alpha))
    etc_alpha = encode_etc1_fast(alpha_rgb)
    pkm_alpha = make_pkm(etc_alpha, w, h)
    with open("scratch/patch_res/login.alpha.pkm", "wb") as f:
        f.write(pkm_alpha)
    print("Saved scratch/patch_res/login.alpha.pkm")
    
    # Copy plist
    with open("scratch/login_extracted/out_game_ui_login_loginpanel_login.plist", "rb") as f:
        pl_data = f.read()
    with open("scratch/patch_res/login.plist", "wb") as f:
        f.write(pl_data)
    print("Saved scratch/patch_res/login.plist")

if __name__ == "__main__":
    patch_login6_with_logo()
    patch_login_atlas_with_play_and_logo()
    print("All title banner and play button assets successfully built!")
