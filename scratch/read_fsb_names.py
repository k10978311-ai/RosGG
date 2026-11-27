import zipfile, struct

obb = r"decompile\xapk\patch.1227927.com.netease.chiji.obb"
with zipfile.ZipFile(obb, 'r') as z:
    for name in ["res/sound/sound_g89/music_rukoujiemian.fsb", "res/sound/music/music_chushengdao_rulesofsurvival.fsb"]:
        data = z.read(name)
        magic, ver, num_samples, shdr_size, name_size, data_size, mode = struct.unpack_from("<4sIIIIII", data, 0)
        # In FSB5:
        # Base header is 0x3C (60 bytes)
        # sample_headers: offset 60 to 60 + shdr_size
        # name_table: offset 60 + shdr_size to 60 + shdr_size + name_size
        name_offset = 60 + shdr_size
        name_bytes = data[name_offset:name_offset + name_size]
        print(f"{name} names raw:", name_bytes)
