import os
import sys
import plistlib
import subprocess
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(__file__))
from test_etc1_fast import encode_etc1_fast, make_pkm

logo_source_path = r"C:\Users\Lufy\.gemini\antigravity\brain\c744c4c4-aaed-4b8b-9e65-5d71627bc1d9\ros_game_title_logo_1794976737825.jpg"
bg_source_path = r"C:\Users\Lufy\.gemini\antigravity\brain\c744c4c4-aaed-4b8b-9e65-5d71627bc1d9\ros_lobby_background_1794976721936.jpg"

font_bahnschrift = "C:/Windows/Fonts/bahnschrift.ttf"
if not os.path.exists(font_bahnschrift):
    font_bahnschrift = "C:/Windows/Fonts/arialbd.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def extract_clean_logo():
    print("Extracting clean transparent logo...")
    logo_img = Image.open(logo_source_path).convert("RGB")
    arr = np.array(logo_img, dtype=np.float32)
    max_c = np.max(arr, axis=2)
    alpha = np.clip((max_c - 18) / 35.0, 0.0, 1.0) * 255.0
    scale = np.where(alpha > 0, 255.0 / np.maximum(max_c, 50.0), 1.0)
    scale = np.clip(scale, 1.0, 1.4)[:, :, np.newaxis]
    rgb_clean = np.clip(arr * scale, 0, 255).astype(np.uint8)
    logo_rgba = Image.fromarray(np.dstack([rgb_clean, alpha.astype(np.uint8)]))
    bbox = logo_rgba.getbbox()
    trimmed = logo_rgba.crop(bbox)
    print(f"Trimmed logo size: {trimmed.size}")
    return trimmed

def fit_logo(trimmed_logo, w, h, padding=4):
    avail_w = w - padding * 2
    avail_h = h - padding * 2
    tw, th = trimmed_logo.size
    ratio = min(avail_w / tw, avail_h / th)
    nw, nh = int(tw * ratio), int(th * ratio)
    resized = trimmed_logo.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(resized, ((w - nw) // 2, (h - nh) // 2), resized)
    return canvas

def crop_and_resize(img, target_w, target_h):
    target_aspect = target_w / target_h
    src_aspect = img.width / img.height
    if src_aspect > target_aspect:
        crop_w = int(img.height * target_aspect)
        offset_x = (img.width - crop_w) // 2
        cropped = img.crop((offset_x, 0, offset_x + crop_w, img.height))
    else:
        crop_h = int(img.width / target_aspect)
        offset_y = (img.height - crop_h) // 2
        cropped = img.crop((0, offset_y, img.width, offset_y + crop_h))
    return cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

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

def build_all_patches():
    trimmed_logo = extract_clean_logo()
    bg_img = Image.open(bg_source_path).convert("RGBA")
    play_btn = render_play_button(838, 159)
    
    # --- 1. Patch login6 (Lobby Background + RKU Logo) ---
    print("\n--- 1. Patching login6 (Background + RKU Logo) ---")
    login6_atlas = Image.new("RGBA", (2048, 2048), (0, 0, 0, 0))
    
    # vx_giant/bg.png: {{2, 2}, {1580, 973}}
    bg_973 = crop_and_resize(bg_img, 1580, 973)
    login6_atlas.paste(bg_973, (2, 2))
    print("Pasted new lobby background at vx_giant/bg.png (2, 2)")
    
    # img_login_xiyou.png: {{2, 979}, {1580, 960}}
    bg_960 = crop_and_resize(bg_img, 1580, 960)
    login6_atlas.paste(bg_960, (2, 979))
    print("Pasted new lobby background at img_login_xiyou.png (2, 979)")
    
    # RKU-LOGO.png: {{1586, 2}, {378, 332}}
    logo_rku = fit_logo(trimmed_logo, 378, 332)
    login6_atlas.paste(logo_rku, (1586, 2), logo_rku)
    print("Pasted new logo at RKU-LOGO.png (1586, 2)")
    
    save_and_encode_atlas(login6_atlas, "scratch/patch_res/login6")
    
    # --- 2. Patch login (Main Title Logo zjzc_qd, Play Button, txt_logo_zjzc) ---
    print("\n--- 2. Patching login (Main Title Logo + Play Button) ---")
    login_atlas = Image.open("scratch/login_atlas_decoded.png").convert("RGBA")
    
    # zjzc_qd.png: {{1, 1}, {502, 317}} -> THE MAIN TITLE LOGO ON SCREEN!
    logo_main = fit_logo(trimmed_logo, 502, 317, padding=2)
    blank_logo = Image.new("RGBA", (502, 317), (0, 0, 0, 0))
    login_atlas.paste(blank_logo, (1, 1))
    login_atlas.paste(logo_main, (1, 1), logo_main)
    print("Pasted new Title Logo at zjzc_qd.png (1, 1)")
    
    # txt_enter_game.png: {{505, 1}, {838, 159}} -> PLAY Button
    blank_play = Image.new("RGBA", (838, 159), (0, 0, 0, 0))
    login_atlas.paste(blank_play, (505, 1))
    login_atlas.paste(play_btn, (505, 1), play_btn)
    print("Pasted new PLAY button at txt_enter_game.png (505, 1)")
    
    # txt_logo_zjzc.png: {{505, 162}, {406, 306}}
    logo_zjzc = fit_logo(trimmed_logo, 406, 306, padding=4)
    blank_zjzc = Image.new("RGBA", (406, 306), (0, 0, 0, 0))
    login_atlas.paste(blank_zjzc, (505, 162))
    login_atlas.paste(logo_zjzc, (505, 162), logo_zjzc)
    print("Pasted new Logo at txt_logo_zjzc.png (505, 162)")
    
    # panel_bg_txt01: {{1979, 1}, {689, 56}} rotated True -> (56, 689)
    blank_bar = Image.new("RGBA", (56, 689), (0, 0, 0, 0))
    login_atlas.paste(blank_bar, (1979, 1))
    print("Cleared panel_bg_txt01 (1979, 1)")
    
    save_and_encode_atlas(login_atlas, "scratch/patch_res/login")
    
    # --- 3. Patch ui_login_en (Play Button, Rotated Logos, Clean Side Icons) ---
    print("\n--- 3. Patching ui_login_en ---")
    ui_atlas = Image.open("scratch/ui_login_en_original.png").convert("RGBA")
    
    # txt_enter_game_en_ui_login: {{1, 1}, {838, 159}}
    ui_atlas.paste(blank_play, (1, 1))
    ui_atlas.paste(play_btn, (1, 1), play_btn)
    print("Pasted new PLAY button at txt_enter_game_en_ui_login (1, 1)")
    
    # Cocos format 3 rotated: True means upright (502, 317) rotated 270 deg CW gives (317, 502)
    logo_rotated = logo_main.rotate(270, expand=True)
    assert logo_rotated.size == (317, 502)
    
    # img_login_logo_en_ui_login: {{79, 1434}, {502, 317}}, rotated: True
    blank_rot = Image.new("RGBA", (317, 502), (0, 0, 0, 0))
    ui_atlas.paste(blank_rot, (79, 1434))
    ui_atlas.paste(logo_rotated, (79, 1434), logo_rotated)
    print("Pasted new rotated Logo at img_login_logo_en_ui_login (79, 1434)")
    
    # img_login_logo1_en_ui_login: {{398, 396}, {502, 317}}, rotated: True
    ui_atlas.paste(blank_rot, (398, 396))
    ui_atlas.paste(logo_rotated, (398, 396), logo_rotated)
    print("Pasted new rotated Logo at img_login_logo1_en_ui_login (398, 396)")
    
    save_and_encode_atlas(ui_atlas, "scratch/patch_res/ui_login_en")

def deploy_fast():
    print("\n--- 4. Fast Staged Deployment to LDPlayer ---")
    adb = "C:/LDPlayer/LDPlayer9/adb.exe"
    serial = "emulator-5554"
    staging_dir = "/data/local/tmp/ros_patch"
    remote_base = "/storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na"
    
    # Push all updated files once to /data/local/tmp/ros_patch
    subprocess.run([adb, "-s", serial, "shell", f"mkdir -p {staging_dir}"], check=True)
    files = [
        "scratch/patch_res/login6.png",
        "scratch/patch_res/login6.pkm",
        "scratch/patch_res/login6.alpha.pkm",
        "scratch/patch_res/login6.plist",
        "scratch/patch_res/login.png",
        "scratch/patch_res/login.pkm",
        "scratch/patch_res/login.alpha.pkm",
        "scratch/patch_res/login.plist",
        "scratch/patch_res/ui_login_en.png",
        "scratch/patch_res/ui_login_en.pkm",
        "scratch/patch_res/ui_login_en.alpha.pkm",
        "scratch/patch_res/ui_login_en.plist",
        "scratch/patch_res/login7.pkm",
        "scratch/patch_res/login7.alpha.pkm",
        "scratch/patch_res/login7.plist",
    ]
    for f in files:
        if os.path.exists(f):
            subprocess.run([adb, "-s", serial, "push", f, f"{staging_dir}/{os.path.basename(f)}"], check=True)
    print(f"Pushed {len(files)} files to {staging_dir}")
    
    # Use shell script on device to copy instantly to all 36 directories
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
    
    script_lines = []
    for d in dirs_to_target:
        script_lines.append(f"mkdir -p '{d}'")
        script_lines.append(f"cp -f {staging_dir}/* '{d}/'")
    
    full_cmd = " && ".join(script_lines)
    subprocess.run([adb, "-s", serial, "shell", full_cmd], check=True)
    print("Copied to all 36 directories in one rapid on-device execution!")

def reboot_and_capture():
    print("\n--- 5. Rebooting Game & Capturing Live Result ---")
    adb = "C:/LDPlayer/LDPlayer9/adb.exe"
    serial = "emulator-5554"
    pkg = "com.netease.chiji"
    
    subprocess.run([adb, "-s", serial, "shell", f"am force-stop {pkg}"])
    time.sleep(2)
    subprocess.run([adb, "-s", serial, "shell", f"monkey -p {pkg} -c android.intent.category.LAUNCHER 1"], stdout=subprocess.DEVNULL)
    print("Game launched, waiting for title / lobby screen...")
    
    # Wait for loading screen and dismiss notice popups
    for wait_s in [5, 8, 10]:
        time.sleep(wait_s)
        subprocess.run([adb, "-s", serial, "shell", "input tap 1536 100"], stdout=subprocess.DEVNULL)
        subprocess.run([adb, "-s", serial, "shell", "input tap 1280 720"], stdout=subprocess.DEVNULL)
    
    out_img = "scratch/screen_new_lobby_live.png"
    with open(out_img, "wb") as f:
        subprocess.run([adb, "-s", serial, "exec-out", "screencap", "-p"], stdout=f)
    print(f"Captured live screen to {out_img}")

if __name__ == "__main__":
    build_all_patches()
    deploy_fast()
    reboot_and_capture()
