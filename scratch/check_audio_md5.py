import subprocess

adb = r"C:\LDPlayer\LDPlayer9\adb.exe"
cmd = [adb, "-s", "emulator-5554", "shell", "ls -l /storage/emulated/0/Android/obb/com.netease.chiji/"]
res = subprocess.run(cmd, capture_output=True)
print("OBB found:\n", res.stdout.decode('utf-8', errors='ignore'))


