import subprocess

adb = r"C:\LDPlayer\LDPlayer9\adb.exe"
dst = r"C:\Users\Lufy\.gemini\antigravity\brain\1351e113-f720-4968-8d52-364fa84eb18d\emulator_screen_live.png"
with open(dst, "wb") as f:
    subprocess.run([adb, "-s", "emulator-5554", "exec-out", "screencap", "-p"], stdout=f)

print("Saved emulator_screen_live.png")
