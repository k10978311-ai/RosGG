import zipfile

obb = r"decompile\xapk\patch.1227927.com.netease.chiji.obb"
with zipfile.ZipFile(obb, 'r') as z:
    for name in ["res/sound/sound_g89/music_rukoujiemian.fsb", "res/sound/music/music_chushengdao_rulesofsurvival.fsb"]:
        data = z.read(name)
        print(f"{name}: len={len(data)}, magic={data[:8]}")
