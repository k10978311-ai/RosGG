import subprocess, time

adb = r"C:\LDPlayer\LDPlayer9\adb.exe"
print("Waiting 10s for title screen...")
time.sleep(10)

for dev, name in [("emulator-5554", "emulator_title.png"), ("R3CM90BCXGJ", "phone_title.png")]:
    path = f"C:\\Users\\Lufy\\.gemini\\antigravity\\brain\\1351e113-f720-4968-8d52-364fa84eb18d\\{name}"
    with open(path, "wb") as f:
        subprocess.run([adb, "-s", dev, "exec-out", "screencap", "-p"], stdout=f)
    print(f"Captured {name}")
