import fsb5, zipfile

obb = r"decompile\xapk\patch.1227927.com.netease.chiji.obb"
with zipfile.ZipFile(obb, 'r') as z:
    data = z.read("res/sound/music/music_chushengdao_rulesofsurvival.fsb")
    f = fsb5.load(data)
    s = f.samples[0]
    print("Metadata chunks:", s.metadata)
    print("Samples:", s.samples)
    print("Channels:", s.channels)
    print("Frequency:", s.frequency)
    print("Data offset:", s.dataOffset)
