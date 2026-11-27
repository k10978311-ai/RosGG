import subprocess

adb = r"C:\LDPlayer\LDPlayer9\adb.exe"
for dev in ["emulator-5554", "R3CM90BCXGJ"]:
    pid = subprocess.run([adb, "-s", dev, "shell", "pidof com.netease.chiji"], capture_output=True, text=True).stdout.strip()
    focus = subprocess.run([adb, "-s", dev, "shell", "dumpsys window | grep mCurrentFocus"], capture_output=True, text=True).stdout.strip()
    print(f"[{dev}] PID={pid}, Focus={focus}")
