import subprocess, time
from PIL import Image

adb = r"C:\LDPlayer\LDPlayer9\adb.exe"

im = Image.open(r"C:\Users\Lufy\.gemini\antigravity\brain\1351e113-f720-4968-8d52-364fa84eb18d\emulator_screen_live.png")
w, h = im.size
print(f"Screen size: {w}x{h}")

# The X button is at ~88.5% width, ~9.5% height
close_x = int(w * 0.887)
close_y = int(h * 0.095)
print(f"Tapping close button at ({close_x}, {close_y})...")

subprocess.run([adb, "-s", "emulator-5554", "shell", f"input tap {close_x} {close_y}"])
time.sleep(2)

dst = r"C:\Users\Lufy\.gemini\antigravity\brain\1351e113-f720-4968-8d52-364fa84eb18d\emulator_title_clean.png"
with open(dst, "wb") as f:
    subprocess.run([adb, "-s", "emulator-5554", "exec-out", "screencap", "-p"], stdout=f)
print(f"Saved {dst}")
