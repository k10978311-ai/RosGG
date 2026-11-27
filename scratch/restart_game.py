import subprocess, time

adb = r"C:\LDPlayer\LDPlayer9\adb.exe"
devices = ["emulator-5554", "R3CM90BCXGJ"]
pkg = "com.netease.chiji"

for dev in devices:
    print(f"[{dev}] Pushing music file...")
    subprocess.run([adb, "-s", dev, "shell", "mkdir -p /storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na/res/sound/music"], capture_output=True)
    subprocess.run([adb, "-s", dev, "push", "scratch/music_chushengdao_rulesofsurvival.fsb", "/storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na/res/sound/music/music_chushengdao_rulesofsurvival.fsb"], capture_output=True)

    print(f"[{dev}] Force stopping {pkg}...")
    subprocess.run([adb, "-s", dev, "shell", f"am force-stop {pkg}"], capture_output=True)

time.sleep(1)

for dev in devices:
    print(f"[{dev}] Starting {pkg}...")
    subprocess.run([adb, "-s", dev, "shell", f"monkey -p {pkg} -c android.intent.category.LAUNCHER 1"], capture_output=True)

print("Game relaunched on both devices. Waiting 10s for splash/load...")
time.sleep(10)

# Capture emulator screenshot to verify
out_png = r"scratch\restarted_game_screen.png"
with open(out_png, "wb") as f:
    subprocess.run([adb, "-s", "emulator-5554", "exec-out", "screencap", "-p"], stdout=f)

print(f"Captured screenshot to {out_png}")
