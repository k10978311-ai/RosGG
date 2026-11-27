import zipfile

for obb in [
    r"decompile\xapk\main.1227927.com.netease.chiji.obb",
    r"decompile\xapk\patch.1227927.com.netease.chiji.obb"
]:
    try:
        with zipfile.ZipFile(obb, 'r') as z:
            names = [n for n in z.namelist() if any(ext in n.lower() for ext in ['.mp3', '.ogg', '.wav', 'sound', 'bgm'])]
            print(f"{obb}: found {len(names)} matching files")
            for n in names[:25]:
                print("  ", n)
    except Exception as e:
        print(f"Error {obb}: {e}")

