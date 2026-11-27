import os
import sys
import zipfile
import io
import subprocess
import time
from PIL import Image, ImageDraw

def main():
    print("=== Rules of Survival — Game Icon Reinstall Pipeline ===")
    
    icon_src = r"C:\Users\Lufy\.gemini\antigravity\brain\c744c4c4-aaed-4b8b-9e65-5d71627bc1d9\ros2_app_icon_1794981634681.jpg"
    base_apk = r"decompile\patched\signed\ros_patched_unsigned-aligned-debugSigned.apk"
    if not os.path.exists(base_apk):
        base_apk = r"decompile\patched\ros_patched_unsigned.apk"
    
    print(f"Loading master app icon: {icon_src}")
    master_icon = Image.open(icon_src).convert("RGBA")
    
    # Save a copy in scratch for reference
    master_icon.save("scratch/ros2_master_app_icon.png")
    
    def make_round(img):
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, img.width, img.height), fill=255)
        res = img.copy()
        res.putalpha(mask)
        return res

    print("Generating Android icon assets across all densities...")
    icon_replacements = {}
    sizes = {
        "ldpi": 36,
        "mdpi": 48,
        "hdpi": 72,
        "xhdpi": 96,
        "xxhdpi": 144,
        "xxxhdpi": 192,
    }

    for density, sz in sizes.items():
        sq = master_icon.resize((sz, sz), Image.Resampling.LANCZOS)
        buf_sq = io.BytesIO()
        sq.save(buf_sq, "PNG")
        sq_bytes = buf_sq.getvalue()
        
        rnd = make_round(sq)
        buf_rnd = io.BytesIO()
        rnd.save(buf_rnd, "PNG")
        rnd_bytes = buf_rnd.getvalue()
        
        icon_replacements[f"res/drawable-{density}/ic_launcher.png"] = sq_bytes
        icon_replacements[f"res/mipmap-{density}/ic_launcher.png"] = sq_bytes
        icon_replacements[f"res/mipmap-{density}/ic_launcher_round.png"] = rnd_bytes

    bg_sizes = {
        "ldpi": 81,
        "mdpi": 108,
        "hdpi": 162,
        "xhdpi": 216,
        "xxhdpi": 324,
        "xxxhdpi": 432,
    }
    for density, sz in bg_sizes.items():
        bg = master_icon.resize((sz, sz), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        bg.save(buf, "PNG")
        icon_replacements[f"res/drawable-{density}/ic_launcher_background.png"] = buf.getvalue()

    # Also root drawable
    icon_replacements["res/drawable/ic_launcher.png"] = icon_replacements["res/drawable-xxhdpi/ic_launcher.png"]

    print(f"Generated {len(icon_replacements)} icon replacements.")

    # 2. Rebuild unsigned APK
    os.makedirs("scratch", exist_ok=True)
    out_unsigned = r"scratch\ros_new_icon_unsigned.apk"
    print(f"Rebuilding APK with new icon -> {out_unsigned}...")
    
    exclude_prefixes = ("META-INF/",)
    exclude_exact = {
        "res/mipmap-anydpi-v26/ic_launcher.xml",
        "res/mipmap-anydpi-v26/ic_launcher_round.xml",
    }
    
    with zipfile.ZipFile(base_apk, "r") as zin:
        with zipfile.ZipFile(out_unsigned, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                name = item.filename
                if any(name.startswith(p) for p in exclude_prefixes):
                    continue
                if name in exclude_exact:
                    continue
                if name in icon_replacements:
                    continue
                data = zin.read(name)
                zout.writestr(item, data)
                
            for path_in_apk, data in icon_replacements.items():
                zout.writestr(path_in_apk, data)
                
    print(f"Successfully constructed unsigned APK ({os.path.getsize(out_unsigned)} bytes)")

    # 3. Sign APK with uber-apk-signer
    java = r"decompile\tools\jdk\bin\java.exe"
    signer = r"decompile\tools\uber-apk-signer.jar"
    out_signed_dir = r"scratch\signed_apk"
    os.makedirs(out_signed_dir, exist_ok=True)
    
    print(f"Signing APK via uber-apk-signer...")
    sign_cmd = [
        java, "-jar", signer,
        "-a", out_unsigned,
        "-o", out_signed_dir,
        "--allowResign"
    ]
    res = subprocess.run(sign_cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(res.stderr)
        raise RuntimeError("APK signing failed!")

    signed_apk = os.path.join(out_signed_dir, "ros_new_icon_unsigned-aligned-debugSigned.apk")
    if not os.path.exists(signed_apk):
        # find newest apk in out_signed_dir
        apks = [os.path.join(out_signed_dir, f) for f in os.listdir(out_signed_dir) if f.endswith(".apk")]
        signed_apk = max(apks, key=os.path.getmtime)
        
    print(f"Signed APK ready: {signed_apk} ({os.path.getsize(signed_apk)} bytes)")

    # 4. Install onto LDPlayer
    adb = r"C:\LDPlayer\LDPlayer9\adb.exe"
    serial = "emulator-5554"
    remote_apk = "/data/local/tmp/ros_new_icon.apk"
    
    print(f"Pushing APK to LDPlayer ({serial})...")
    subprocess.run([adb, "-s", serial, "push", signed_apk, remote_apk], check=True)
    
    print("Installing APK on LDPlayer (preserving data and OBB)...")
    out = subprocess.run([adb, "-s", serial, "shell", f"pm install -r '{remote_apk}'"], capture_output=True, text=True)
    print(out.stdout)
    if "Success" not in out.stdout:
        print("Standard pm install had warning, trying adb install -r directly...")
        out2 = subprocess.run([adb, "-s", serial, "install", "-r", signed_apk], capture_output=True, text=True)
        print(out2.stdout)

    # 5. Refresh launcher icon cache
    print("Refreshing LDPlayer launcher...")
    subprocess.run([adb, "-s", serial, "shell", "am force-stop com.ldmnq.launcher3"])
    time.sleep(2)
    subprocess.run([adb, "-s", serial, "shell", "input keyevent KEYCODE_HOME"])
    time.sleep(3)

    # 6. Capture live LDPlayer home screen
    out_screen = "scratch/screen_launcher_new_icon.png"
    print(f"Capturing launcher home screen to {out_screen}...")
    with open(out_screen, "wb") as f:
        subprocess.run([adb, "-s", serial, "exec-out", "screencap", "-p"], stdout=f)
        
    import shutil
    shutil.copy(out_screen, r"C:\Users\Lufy\.gemini\antigravity\brain\c744c4c4-aaed-4b8b-9e65-5d71627bc1d9\screen_launcher_new_icon.png")
    print("Saved screen_launcher_new_icon.png to artifacts!")
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
