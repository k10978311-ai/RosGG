import os
import subprocess

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

files = [
    "scratch/patch_res/ui_login_en.png",
    "scratch/patch_res/ui_login_en.pkm",
    "scratch/patch_res/ui_login_en.alpha.pkm",
    "scratch/patch_res/ui_login_en.plist",
]

for d in dirs_to_target:
    subprocess.run([adb, "-s", serial, "shell", f"mkdir -p {d}"], check=True)
    for f in files:
        fname = os.path.basename(f)
        subprocess.run([adb, "-s", serial, "push", f, f"{d}/{fname}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Pushed ui_login_en.* to {d}")

print("All ui_login_en targets pushed successfully!")
