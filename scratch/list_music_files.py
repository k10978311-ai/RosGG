import zipfile

obb = r"decompile\xapk\patch.1227927.com.netease.chiji.obb"
with zipfile.ZipFile(obb, 'r') as z:
    names = [n for n in z.namelist() if 'music' in n.lower() or 'login' in n.lower()]
    for n in names:
        print(n)
