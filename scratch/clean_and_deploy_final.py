import os
import subprocess
import time
from PIL import Image
from test_etc1_fast import encode_etc1_fast, make_pkm

adb = "C:/LDPlayer/LDPlayer9/adb.exe"
serial = "emulator-5554"
staging = "/data/local/tmp/ros_patch"

print("1. Re-encoding login...")
login = Image.open("scratch/patch_res/login.png").convert("RGBA")
w, h = login.size
etc_rgb = encode_etc1_fast(login.convert("RGB"))
with open("scratch/patch_res/login.pkm", "wb") as f:
    f.write(make_pkm(etc_rgb, w, h))
alpha = login.split()[3]
alpha_rgb = Image.merge("RGB", (alpha, alpha, alpha))
etc_alpha = encode_etc1_fast(alpha_rgb)
with open("scratch/patch_res/login.alpha.pkm", "wb") as f:
    f.write(make_pkm(etc_alpha, w, h))

print("2. Re-encoding ui_login_en...")
ui = Image.open("scratch/patch_res/ui_login_en.png").convert("RGBA")
w, h = ui.size
etc_rgb2 = encode_etc1_fast(ui.convert("RGB"))
with open("scratch/patch_res/ui_login_en.pkm", "wb") as f:
    f.write(make_pkm(etc_rgb2, w, h))
alpha2 = ui.split()[3]
alpha_rgb2 = Image.merge("RGB", (alpha2, alpha2, alpha2))
etc_alpha2 = encode_etc1_fast(alpha_rgb2)
with open("scratch/patch_res/ui_login_en.alpha.pkm", "wb") as f:
    f.write(make_pkm(etc_alpha2, w, h))

print("3. Staging files on device...")
for f in [
    "scratch/patch_res/login.png",
    "scratch/patch_res/login.pkm",
    "scratch/patch_res/login.alpha.pkm",
    "scratch/patch_res/ui_login_en.png",
    "scratch/patch_res/ui_login_en.pkm",
    "scratch/patch_res/ui_login_en.alpha.pkm",
]:
    subprocess.run([adb, "-s", serial, "push", f, f"{staging}/{os.path.basename(f)}"], check=True)

print("4. Copying to target directories...")
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
script_lines = []
for d in dirs_to_target:
    script_lines.append(f"mkdir -p '{d}'")
    script_lines.append(f"cp -f {staging}/* '{d}/'")
full_cmd = " && ".join(script_lines)
subprocess.run([adb, "-s", serial, "shell", full_cmd], check=True)

print("5. Rebooting game...")
subprocess.run([adb, "-s", serial, "shell", "am force-stop com.netease.chiji"])
time.sleep(2)
subprocess.run([adb, "-s", serial, "shell", "monkey -p com.netease.chiji -c android.intent.category.LAUNCHER 1"], stdout=subprocess.DEVNULL)

for ws in [5, 8, 10]:
    time.sleep(ws)
    subprocess.run([adb, "-s", serial, "shell", "input tap 1536 100"], stdout=subprocess.DEVNULL)
    subprocess.run([adb, "-s", serial, "shell", "input tap 1280 720"], stdout=subprocess.DEVNULL)

out_img = "scratch/screen_clean_final.png"
with open(out_img, "wb") as f:
    subprocess.run([adb, "-s", serial, "exec-out", "screencap", "-p"], stdout=f)

import shutil
shutil.copy(out_img, r"C:\Users\Lufy\.gemini\antigravity\brain\c744c4c4-aaed-4b8b-9e65-5d71627bc1d9\screen_clean_final.png")
print("All done, final screenshot saved to screen_clean_final.png!")
