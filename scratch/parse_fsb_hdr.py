import zipfile, struct

obb = r"decompile\xapk\patch.1227927.com.netease.chiji.obb"
with zipfile.ZipFile(obb, 'r') as z:
    for name in ["res/sound/sound_g89/music_rukoujiemian.fsb", "res/sound/music/music_chushengdao_rulesofsurvival.fsb"]:
        data = z.read(name)
        magic, ver, num_samples, shdr_size, name_size, data_size, mode = struct.unpack_from("<4sIIIIII", data, 0)
        mode_names = {11: "MPEG", 15: "VORBIS", 7: "IMAADPCM", 16: "FADPCM"}
        print(f"{name}: samples={num_samples}, mode={mode} ({mode_names.get(mode, 'Other')}), data_size={data_size}")
