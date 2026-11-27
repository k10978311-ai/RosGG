import zipfile

obb = r"decompile\xapk\patch.1227927.com.netease.chiji.obb"
with zipfile.ZipFile(obb, 'r') as z:
    data = z.read("res/sound/music/music_chushengdao_rulesofsurvival.fsb")
    mp3_data = data[128:]
    with open("scratch/chushengdao_extracted.mp3", "wb") as f:
        f.write(mp3_data)
    print(f"Extracted {len(mp3_data)} bytes to scratch/chushengdao_extracted.mp3")
