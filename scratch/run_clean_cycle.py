import subprocess, time, os, re

ADB = r"C:\LDPlayer\LDPlayer9\adb.exe"
if not os.path.exists(ADB):
    ADB = r"E:\LDPlayer\LDPlayer9\adb.exe"

def adb(cmd):
    return subprocess.check_output(f'"{ADB}" -s emulator-5554 {cmd}', shell=True, text=True, errors="replace")

def adb_raw(cmd):
    return subprocess.check_output(f'"{ADB}" -s emulator-5554 {cmd}', shell=True)

def count_notice():
    cnt = 0
    for fn in ["server.stdout.log", "server.log"]:
        if os.path.exists(fn):
            try:
                cnt += open(fn, "r", errors="ignore").read().count("notice_pc_hw.txt")
            except:
                pass
    return cnt

before = count_notice()
print(f"[*] Starting cycle. Notice count before = {before}")

print("[1] Stopping app and frida-server...")
adb("shell am force-stop com.netease.chiji")
try:
    adb("shell pkill -9 frida-server")
except:
    pass
time.sleep(2)

print("[2] Launching app...")
adb("shell monkey -p com.netease.chiji -c android.intent.category.LAUNCHER 1")

print("[3] Waiting for notice_pc_hw.txt fetch from client...")
for i in range(40):
    time.sleep(3)
    curr = count_notice()
    if curr > before:
        print(f"[+] Notice fetched after {(i+1)*3}s!")
        break
else:
    print("[!] Notice not detected within 120s, continuing anyway...")

print("[4] Waiting 20s for title screen...")
time.sleep(20)

print("[5] Starting frida-server...")
try:
    adb("shell /data/local/tmp/frida-server -D &")
except:
    pass
time.sleep(3)

print("[6] Dismissing Events popup...")
adb("shell input tap 1538 89")
time.sleep(2)
adb("shell input tap 1535 105")
time.sleep(2)

print("[7] Running login_scene_switch.py via Frida...")
F = "/storage/emulated/0/Android/data/com.netease.chiji/files"
adb(f"push frida/payloads/login_scene_switch.py {F}/py_payload.py")
out = subprocess.run([r".venv\Scripts\python.exe", "run_frida.py", "frida/neox_py_eval.js", "--attach", "--realm", "emulated", "--once"], capture_output=True, text=True)
print("Frida out:", out.stdout.strip())
if out.stderr:
    print("Frida err:", out.stderr.strip()[:200])

try:
    print("Payload log:", adb(f"shell cat {F}/py_out.log").strip())
except:
    pass

print("[8] Settling 5s...")
time.sleep(5)

print("[9] Tapping PLAY (800, 640)...")
adb("shell input tap 800 640")
time.sleep(1)
adb("shell input tap 790 660")

print("[10] Waiting 30s for hall.scn to load...")
time.sleep(30)

print("[11] Dismissing possible startup dialogs (Supreme Supply / Profile)...")
adb("shell input tap 98 40")    # Supreme supply back
time.sleep(2)
adb("shell input tap 1265 138") # Profile close
time.sleep(2)
adb("shell input tap 98 40")    # In case another back is needed
time.sleep(2)

print("[12] Capturing screenshot...")
adb("shell screencap -p /sdcard/s.png")
adb_raw("pull /sdcard/s.png emulator_screen_now.png")
print("[+] Screenshot saved to emulator_screen_now.png")
