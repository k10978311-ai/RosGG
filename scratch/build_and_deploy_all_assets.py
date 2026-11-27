import os
import sys
import plistlib
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(__file__))
from test_etc1_fast import encode_etc1_fast, make_pkm

font_bahnschrift = "C:/Windows/Fonts/bahnschrift.ttf"
font_segoeuib = "C:/Windows/Fonts/segoeuib.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def render_logo(w=502, h=317):
    scale = 3
    sw, sh = w * scale, h * scale
    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    
    f_badge = get_font(font_segoeuib, 13 * scale)
    f_rules = get_font(font_bahnschrift, 64 * scale)
    f_of = get_font(font_segoeuib, 20 * scale)
    f_survival = get_font(font_bahnschrift, 74 * scale)
    f_sub = get_font(font_segoeuib, 17 * scale)
    
    # 1. Top Cyber Badge: — PRIVATE SERVER 2.0 —
    badge_w, badge_h = 310 * scale, 32 * scale
    bx1 = sw // 2 - badge_w // 2
    by1 = 20 * scale
    bx2 = bx1 + badge_w
    by2 = by1 + badge_h
    
    # Glow
    glow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.rounded_rectangle([bx1 - 3*scale, by1 - 3*scale, bx2 + 3*scale, by2 + 3*scale], radius=7*scale, fill=(0, 210, 255, 130))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=5*scale))
    img.paste(glow, (0, 0), glow)
    
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=6*scale, fill=(12, 22, 38, 250), outline=(0, 210, 255, 240), width=2*scale)
    btxt = "—   PRIVATE SERVER 2.0   —"
    bw = draw.textlength(btxt, font=f_badge)
    draw.text((sw // 2 - bw / 2, by1 + 6*scale), btxt, font=f_badge, fill=(0, 235, 255, 255))
    
    # 2. 'RULES' and 'OF'
    rules_w = draw.textlength("RULES", font=f_rules)
    of_box_w = 54 * scale
    gap = 16 * scale
    total_top_w = rules_w + gap + of_box_w
    
    rx = sw // 2 - total_top_w // 2
    ry = 64 * scale
    
    # Shadow for RULES
    s_img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(s_img)
    s_draw.text((rx + 4*scale, ry + 6*scale), "RULES", font=f_rules, fill=(5, 10, 20, 240))
    s_img = s_img.filter(ImageFilter.GaussianBlur(radius=3*scale))
    img.paste(s_img, (0, 0), s_img)
    
    draw = ImageDraw.Draw(img)
    draw.text((rx - 1*scale, ry - 1*scale), "RULES", font=f_rules, fill=(255, 255, 255, 240))
    draw.text((rx + 2*scale, ry + 2*scale), "RULES", font=f_rules, fill=(40, 55, 80, 255))
    draw.text((rx, ry), "RULES", font=f_rules, fill=(252, 253, 255, 255))
    
    # 'OF' Badge
    of_x = rx + rules_w + gap
    of_y = ry + 16 * scale
    of_h = 36 * scale
    draw.rounded_rectangle([of_x, of_y, of_x + of_box_w, of_y + of_h], radius=6*scale, fill=(20, 32, 54, 245), outline=(255, 205, 45, 240), width=2*scale)
    of_tw = draw.textlength("OF", font=f_of)
    draw.text((of_x + of_box_w // 2 - of_tw / 2, of_y + 6*scale), "OF", font=f_of, fill=(255, 215, 60, 255))
    
    # 3. 'SURVIVAL' (Centered)
    surv_w = draw.textlength("SURVIVAL", font=f_survival)
    sx = sw // 2 - surv_w // 2
    sy = 142 * scale
    
    s_img2 = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    s_draw2 = ImageDraw.Draw(s_img2)
    s_draw2.text((sx + 5*scale, sy + 7*scale), "SURVIVAL", font=f_survival, fill=(5, 10, 20, 240))
    s_img2 = s_img2.filter(ImageFilter.GaussianBlur(radius=4*scale))
    img.paste(s_img2, (0, 0), s_img2)
    
    draw = ImageDraw.Draw(img)
    draw.text((sx - 1*scale, sy - 1*scale), "SURVIVAL", font=f_survival, fill=(255, 255, 255, 240))
    draw.text((sx + 3*scale, sy + 3*scale), "SURVIVAL", font=f_survival, fill=(40, 55, 80, 255))
    draw.text((sx, sy), "SURVIVAL", font=f_survival, fill=(252, 253, 255, 255))
    
    # 4. Gold Divider Line + Accents
    line_y = 236 * scale
    line_len = 160 * scale
    draw.line([(sw // 2 - line_len - 15*scale, line_y), (sw // 2 - 25*scale, line_y)], fill=(255, 205, 45, 240), width=3*scale)
    draw.line([(sw // 2 + 25*scale, line_y), (sw // 2 + line_len + 15*scale, line_y)], fill=(255, 205, 45, 240), width=3*scale)
    # Diamond
    draw.polygon([
        (sw // 2, line_y - 8*scale),
        (sw // 2 + 10*scale, line_y),
        (sw // 2, line_y + 8*scale),
        (sw // 2 - 10*scale, line_y)
    ], fill=(255, 215, 55, 255))
    
    # 5. Subtitle: 'BATTLE ROYALE GAME'
    sub_txt = "BATTLE ROYALE GAME"
    sub_w = draw.textlength(sub_txt, font=f_sub)
    draw.text((sw // 2 - sub_w // 2 + 1*scale, 254*scale + 1*scale), sub_txt, font=f_sub, fill=(5, 12, 25, 240))
    draw.text((sw // 2 - sub_w // 2, 254*scale), sub_txt, font=f_sub, fill=(245, 248, 255, 255))
    
    final_logo = img.resize((w, h), Image.Resampling.LANCZOS)
    return final_logo

def render_play_button(w=838, h=159):
    scale = 2
    sw, sh = w * scale, h * scale
    img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    
    f_play = get_font(font_bahnschrift, 78 * scale)
    txt = "[   —   P L A Y   —   ]"
    
    # Golden glow
    glow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    tw = gdraw.textlength(txt, font=f_play)
    tx = sw // 2 - tw / 2
    ty = sh // 2 - 50 * scale
    gdraw.text((tx, ty), txt, font=f_play, fill=(255, 200, 40, 220))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=8*scale))
    img.paste(glow, (0, 0), glow)
    
    # Deep drop shadow
    s_img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(s_img)
    sdraw.text((tx + 4*scale, ty + 6*scale), txt, font=f_play, fill=(5, 10, 20, 250))
    s_img = s_img.filter(ImageFilter.GaussianBlur(radius=4*scale))
    img.paste(s_img, (0, 0), s_img)
    
    draw = ImageDraw.Draw(img)
    # Bevel highlight
    draw.text((tx - 1*scale, ty - 1*scale), txt, font=f_play, fill=(255, 255, 255, 240))
    draw.text((tx + 2*scale, ty + 2*scale), txt, font=f_play, fill=(180, 130, 20, 255))
    draw.text((tx, ty), txt, font=f_play, fill=(255, 252, 242, 255))
    
    final_play = img.resize((w, h), Image.Resampling.LANCZOS)
    return final_play

def save_and_encode_atlas(atlas, out_prefix):
    w, h = atlas.size
    png_path = f"{out_prefix}.png"
    atlas.save(png_path, "PNG")
    print(f"Saved {png_path}")
    
    # RGB PKM
    print(f"Encoding {out_prefix}.pkm (RGB)...")
    etc_rgb = encode_etc1_fast(atlas.convert("RGB"))
    with open(f"{out_prefix}.pkm", "wb") as f:
        f.write(make_pkm(etc_rgb, w, h))
        
    # Alpha PKM
    print(f"Encoding {out_prefix}.alpha.pkm (Alpha)...")
    alpha = atlas.split()[3]
    alpha_rgb = Image.merge("RGB", (alpha, alpha, alpha))
    etc_alpha = encode_etc1_fast(alpha_rgb)
    with open(f"{out_prefix}.alpha.pkm", "wb") as f:
        f.write(make_pkm(etc_alpha, w, h))
    print(f"Done encoding {out_prefix}")

def build_login_patch():
    print("\n--- 1. Building Login Atlas Patch (login.*) ---")
    base_atlas = Image.open("scratch/login_atlas_decoded.png").convert("RGBA")
    
    logo_main = render_logo(502, 317)
    play_btn = render_play_button(838, 159)
    logo_zjzc = render_logo(406, 306)
    
    # 1. zjzc_qd.png: {{1, 1}, {502, 317}} -> THE MAIN TITLE BANNER!
    blank_logo = Image.new("RGBA", (502, 317), (0, 0, 0, 0))
    base_atlas.paste(blank_logo, (1, 1))
    base_atlas.paste(logo_main, (1, 1), logo_main)
    print("Pasted new Title Logo at zjzc_qd.png (1, 1)")
    
    # 2. txt_enter_game.png: {{505, 1}, {838, 159}} -> PLAY button!
    blank_play = Image.new("RGBA", (838, 159), (0, 0, 0, 0))
    base_atlas.paste(blank_play, (505, 1))
    base_atlas.paste(play_btn, (505, 1), play_btn)
    print("Pasted new PLAY button at txt_enter_game.png (505, 1)")
    
    # 3. txt_logo_zjzc.png: {{505, 162}, {406, 306}}
    blank_zjzc = Image.new("RGBA", (406, 306), (0, 0, 0, 0))
    base_atlas.paste(blank_zjzc, (505, 162))
    base_atlas.paste(logo_zjzc, (505, 162), logo_zjzc)
    print("Pasted new Logo at txt_logo_zjzc.png (505, 162)")
    
    # 4. panel_bg_txt01: {{1979, 1}, {689, 56}} rotated True -> (56, 689) -> Clear to transparent
    blank_bar = Image.new("RGBA", (56, 689), (0, 0, 0, 0))
    base_atlas.paste(blank_bar, (1979, 1))
    print("Cleared panel_bg_txt01 (1979, 1)")
    
    save_and_encode_atlas(base_atlas, "scratch/patch_res/login")
    
    # Copy plist
    with open("scratch/login_extracted/out_game_ui_login_loginpanel_login.plist", "rb") as f:
        pl_data = f.read()
    with open("scratch/patch_res/login.plist", "wb") as f:
        f.write(pl_data)

def build_ui_login_en_patch():
    print("\n--- 2. Building UI Login EN Atlas Patch (ui_login_en.*) ---")
    base_atlas = Image.open("scratch/ui_login_en_original.png").convert("RGBA")
    
    logo_main = render_logo(502, 317)
    play_btn = render_play_button(838, 159)
    
    # txt_enter_game_en_ui_login: {{1, 1}, {838, 159}}, rotated: False
    blank_play = Image.new("RGBA", (838, 159), (0, 0, 0, 0))
    base_atlas.paste(blank_play, (1, 1))
    base_atlas.paste(play_btn, (1, 1), play_btn)
    print("Pasted new PLAY button at txt_enter_game_en_ui_login (1, 1)")
    
    # Cocos format 3 rotated: True means upright (502, 317) rotated 270 deg CW gives (317, 502)
    logo_rotated = logo_main.rotate(270, expand=True)
    assert logo_rotated.size == (317, 502)
    
    # img_login_logo_en_ui_login: {{79, 1434}, {502, 317}}, rotated: True
    blank_logo_rot = Image.new("RGBA", (317, 502), (0, 0, 0, 0))
    base_atlas.paste(blank_logo_rot, (79, 1434))
    base_atlas.paste(logo_rotated, (79, 1434), logo_rotated)
    print("Pasted new rotated Logo at img_login_logo_en_ui_login (79, 1434)")
    
    # img_login_logo1_en_ui_login: {{398, 396}, {502, 317}}, rotated: True
    base_atlas.paste(blank_logo_rot, (398, 396))
    base_atlas.paste(logo_rotated, (398, 396), logo_rotated)
    print("Pasted new rotated Logo at img_login_logo1_en_ui_login (398, 396)")
    
    save_and_encode_atlas(base_atlas, "scratch/patch_res/ui_login_en")
    
    with open("scratch/ui_login_en.plist", "rb") as f:
        pl_data = f.read()
    with open("scratch/patch_res/ui_login_en.plist", "wb") as f:
        f.write(pl_data)

def build_login6_patch():
    print("\n--- 3. Building Login6 Atlas Patch (login6.*) ---")
    base_atlas = Image.open("scratch/patch_res/login6.png").convert("RGBA")
    w, h = base_atlas.size
    
    # RKU-LOGO.png: {{1586, 2}, {378, 332}}
    logo_rku = render_logo(378, 332)
    blank_rku = Image.new("RGBA", (378, 332), (0, 0, 0, 0))
    base_atlas.paste(blank_rku, (1586, 2))
    base_atlas.paste(logo_rku, (1586, 2), logo_rku)
    print("Pasted new Logo at RKU-LOGO.png (1586, 2)")
    
    save_and_encode_atlas(base_atlas, "scratch/patch_res/login6")

def deploy_all_to_device():
    print("\n--- 4. Deploying All Patched Assets to LDPlayer ---")
    adb = "C:/LDPlayer/LDPlayer9/adb.exe"
    serial = "emulator-5554"
    remote_base = "/storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na"
    
    dirs_to_target = [
        f"{remote_base}/res",
        f"{remote_base}/res/LoginPanel",
        f"{remote_base}/res/loginpanel",
        f"{remote_base}/res/ui",
        f"{remote_base}/res/ui/LoginPanel",
        f"{remote_base}/res/ui/loginpanel",
        f"{remote_base}/res/out_game",
        f"{remote_base}/res/out_game/ui_login",
        f"{remote_base}/res/out_game/ui_login/loginpanel",
        f"{remote_base}/res/out_game/ui_login/LoginPanel",
        f"{remote_base}/res/ui/out_game/ui_login",
        f"{remote_base}/res/ui/out_game/ui_login/loginpanel",
        f"{remote_base}/res/ui/out_game/ui_login/LoginPanel",
        f"{remote_base}/res/_international/en",
        f"{remote_base}/res/_international/en/ui",
        f"{remote_base}/res/_international/en/ui/out_game/ui_login",
        f"{remote_base}/res/_international/en/ui/out_game/ui_login/loginpanel",
        f"{remote_base}/res/_international/en/ui/out_game/ui_login/LoginPanel",
        
        f"{remote_base}/Documents/res",
        f"{remote_base}/Documents/res/LoginPanel",
        f"{remote_base}/Documents/res/loginpanel",
        f"{remote_base}/Documents/res/ui",
        f"{remote_base}/Documents/res/ui/LoginPanel",
        f"{remote_base}/Documents/res/ui/loginpanel",
        f"{remote_base}/Documents/res/out_game",
        f"{remote_base}/Documents/res/out_game/ui_login",
        f"{remote_base}/Documents/res/out_game/ui_login/loginpanel",
        f"{remote_base}/Documents/res/out_game/ui_login/LoginPanel",
        f"{remote_base}/Documents/res/ui/out_game/ui_login",
        f"{remote_base}/Documents/res/ui/out_game/ui_login/loginpanel",
        f"{remote_base}/Documents/res/ui/out_game/ui_login/LoginPanel",
        f"{remote_base}/Documents/res/_international/en",
        f"{remote_base}/Documents/res/_international/en/ui",
        f"{remote_base}/Documents/res/_international/en/ui/out_game/ui_login",
        f"{remote_base}/Documents/res/_international/en/ui/out_game/ui_login/loginpanel",
        f"{remote_base}/Documents/res/_international/en/ui/out_game/ui_login/LoginPanel",
    ]
    
    files_to_push = [
        # login.* (Title Banner zjzc_qd, Play button, Logo zjzc)
        "scratch/patch_res/login.png",
        "scratch/patch_res/login.pkm",
        "scratch/patch_res/login.alpha.pkm",
        "scratch/patch_res/login.plist",
        # ui_login_en.* (Play button, Logo rotated, clean icons)
        "scratch/patch_res/ui_login_en.png",
        "scratch/patch_res/ui_login_en.pkm",
        "scratch/patch_res/ui_login_en.alpha.pkm",
        "scratch/patch_res/ui_login_en.plist",
        # login6.* (Tactical wallpaper, RKU Logo)
        "scratch/patch_res/login6.png",
        "scratch/patch_res/login6.pkm",
        "scratch/patch_res/login6.alpha.pkm",
        "scratch/patch_res/login6.plist",
        # login7.* (Blank transparent monster suppressor)
        "scratch/patch_res/login7.pkm",
        "scratch/patch_res/login7.alpha.pkm",
        "scratch/patch_res/login7.plist",
    ]
    
    for d in dirs_to_target:
        subprocess.run([adb, "-s", serial, "shell", f"mkdir -p {d}"], check=True)
        for f in files_to_push:
            if os.path.exists(f):
                fname = os.path.basename(f)
                subprocess.run([adb, "-s", serial, "push", f, f"{d}/{fname}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Pushed all files to {d}")
        
    print("Omnipresent deployment completed successfully!")

def reboot_and_verify():
    print("\n--- 5. Rebooting Game & Capturing Live Screen ---")
    adb = "C:/LDPlayer/LDPlayer9/adb.exe"
    serial = "emulator-5554"
    pkg = "com.netease.chiji"
    
    # Force stop
    subprocess.run([adb, "-s", serial, "shell", f"am force-stop {pkg}"])
    time.sleep(2)
    # Launch
    subprocess.run([adb, "-s", serial, "shell", f"monkey -p {pkg} -c android.intent.category.LAUNCHER 1"], stdout=subprocess.DEVNULL)
    print("Launched Rules of Survival...")
    
    # Wait for loading screen and initial check
    for wait_s in [5, 8, 12]:
        print(f"Waiting {wait_s}s...")
        time.sleep(wait_s)
        # Dismiss any popup/notice
        subprocess.run([adb, "-s", serial, "shell", "input tap 1536 100"], stdout=subprocess.DEVNULL)
        subprocess.run([adb, "-s", serial, "shell", "input tap 1280 720"], stdout=subprocess.DEVNULL)
    
    # Final capture
    out_img = "scratch/screen_all_complete_live.png"
    with open(out_img, "wb") as f:
        subprocess.run([adb, "-s", serial, "exec-out", "screencap", "-p"], stdout=f)
    print(f"Captured live screen to {out_img}")

if __name__ == "__main__":
    build_login_patch()
    build_ui_login_en_patch()
    build_login6_patch()
    deploy_all_to_device()
    reboot_and_verify()
