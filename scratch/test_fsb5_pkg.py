import fsb5, zipfile

obb = r"decompile\xapk\patch.1227927.com.netease.chiji.obb"
with zipfile.ZipFile(obb, 'r') as z:
    for name in [
        "res/sound/music/music_chushengdao_rulesofsurvival.fsb",
        "res/sound/sound_g89/music_rukoujiemian.fsb",
        "res/sound/sound_g89/music_zhujiemian.fsb"
    ]:
        data = z.read(name)
        f = fsb5.load(data)
        print(f"=== {name} ===")
        print(f"header: {f.header}, num_samples: {len(f.samples)}")
        for s in f.samples:
            print(f"  sample: name={s.name}, frequency={s.frequency}, channels={s.channels}, samples={s.samples}, data_size={len(s.data)}")

