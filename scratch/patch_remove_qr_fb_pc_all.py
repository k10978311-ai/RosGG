import os
import sys
import plistlib
import subprocess
import time
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from test_etc1_fast import encode_etc1_fast, make_pkm


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


def wipe_rect(img, x, y, w, h):
    blank = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    img.paste(blank, (x, y))


def patch_atlases():
    base_dir = os.path.dirname(__file__)
    patch_dir = os.path.join(base_dir, "patch_res")

    # 1. Patch login.png
    print("\n--- 1. Patching login atlas (wiping QR & PC Tips) ---")
    login_png = os.path.join(patch_dir, "login.png")
    atlas_login = Image.open(login_png).convert("RGBA")

    # Wipe img_qrcode: {{989,684},{120,140}}
    wipe_rect(atlas_login, 989, 684, 120, 140)
    print("Cleared img_qrcode (989, 684)")

    # Wipe pc_tips: {{1345,1},{539,242}}
    wipe_rect(atlas_login, 1345, 1, 539, 242)
    print("Cleared pc_tips (1345, 1)")

    # Wipe ecqr fragments and buttons
    wipe_rect(atlas_login, 947, 974, 40, 40)    # img_ecqr_btn_bg
    wipe_rect(atlas_login, 1420, 864, 43, 44)   # img_ecqr_txt_bg
    wipe_rect(atlas_login, 1337, 245, 216, 157) # img_ecqr_suipian_1
    wipe_rect(atlas_login, 1457, 722, 140, 83)  # img_ecqr_suipian_2
    wipe_rect(atlas_login, 1795, 739, 138, 60)  # img_ecqr_suipian_3
    wipe_rect(atlas_login, 1723, 651, 130, 70)  # img_ecqr_suipian_4
    wipe_rect(atlas_login, 1965, 1096, 75, 90)  # tab_qrcode_dwn
    wipe_rect(atlas_login, 1131, 684, 75, 90)   # tab_qrcode_nml
    print("Cleared all QR fragments and tab icons from login atlas")

    save_and_encode_atlas(atlas_login, os.path.join(patch_dir, "login"))

    # 2. Patch ui_login_en.png
    print("\n--- 2. Patching ui_login_en atlas (wiping QR tab icons) ---")
    ui_login_png = os.path.join(patch_dir, "ui_login_en.png")
    atlas_ui_login = Image.open(ui_login_png).convert("RGBA")

    # tab_qrcode_dwn_en_ui_login: {{707,316},{75,90}} rotated -> {90, 75}
    wipe_rect(atlas_ui_login, 707, 316, 90, 75)
    # tab_qrcode_nml_en_ui_login: {{1843,313},{75,90}} rotated -> {90, 75}
    wipe_rect(atlas_ui_login, 1843, 313, 90, 75)
    print("Cleared tab_qrcode_en icons from ui_login_en atlas")

    save_and_encode_atlas(atlas_ui_login, os.path.join(patch_dir, "ui_login_en"))


def deploy_all(serial="emulator-5554"):
    print("\n--- 3. Deploying All Patched Assets & Scripts to Device ---")
    adb = "C:/LDPlayer/LDPlayer9/adb.exe"
    if not os.path.exists(adb):
        adb = "adb"
    remote_base = "/storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na"

    target_res_dirs = [
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
        "scratch/patch_res/login.png",
        "scratch/patch_res/login.pkm",
        "scratch/patch_res/login.alpha.pkm",
        "scratch/patch_res/login.plist",
        "scratch/patch_res/ui_login_en.png",
        "scratch/patch_res/ui_login_en.pkm",
        "scratch/patch_res/ui_login_en.alpha.pkm",
        "scratch/patch_res/ui_login_en.plist",
    ]

    for d in target_res_dirs:
        subprocess.run([adb, "-s", serial, "shell", f"mkdir -p {d}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for f in files_to_push:
            if os.path.exists(f):
                fname = os.path.basename(f)
                subprocess.run([adb, "-s", serial, "push", f, f"{d}/{fname}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Deploy UIFollowonFacebook.nxs
    fb_nxs = "scratch/patch_res/UIFollowonFacebook.nxs"
    if os.path.exists(fb_nxs):
        fb_dirs = [
            f"{remote_base}/res/nxs/ui",
            f"{remote_base}/res/ui",
            f"{remote_base}/Documents/res/nxs/ui",
            f"{remote_base}/Documents/res/ui",
        ]
        for d in fb_dirs:
            subprocess.run([adb, "-s", serial, "shell", f"mkdir -p {d}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run([adb, "-s", serial, "push", fb_nxs, f"{d}/UIFollowonFacebook.nxs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[+] Deployed UIFollowonFacebook.nxs -> {d}")

    print("[+] All assets and script patches deployed successfully!")


def restart_and_capture(serial="emulator-5554"):
    print("\n--- 4. Restarting Game & Verifying Live Display ---")
    adb = "C:/LDPlayer/LDPlayer9/adb.exe"
    if not os.path.exists(adb):
        adb = "adb"
    pkg = "com.netease.chiji"

    subprocess.run([adb, "-s", serial, "shell", f"am force-stop {pkg}"])
    time.sleep(2)
    subprocess.run([adb, "-s", serial, "shell", f"monkey -p {pkg} -c android.intent.category.LAUNCHER 1"], stdout=subprocess.DEVNULL)
    print("Launched Rules of Survival...")

    for wait_s in [5, 8, 12]:
        print(f"Waiting {wait_s}s...")
        time.sleep(wait_s)
        # Dismiss any popup/notice
        subprocess.run([adb, "-s", serial, "shell", "input tap 1536 100"], stdout=subprocess.DEVNULL)
        subprocess.run([adb, "-s", serial, "shell", "input tap 1280 720"], stdout=subprocess.DEVNULL)

    out_img = "scratch/screen_clean_title_live.png"
    with open(out_img, "wb") as f:
        subprocess.run([adb, "-s", serial, "exec-out", "screencap", "-p"], stdout=f)
    print(f"[+] Captured live title screen to {out_img}")


if __name__ == "__main__":
    patch_atlases()
    deploy_all()
    restart_and_capture()
