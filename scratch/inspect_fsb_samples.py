import zipfile, struct

obb = r"decompile\xapk\patch.1227927.com.netease.chiji.obb"
with zipfile.ZipFile(obb, 'r') as z:
    for name in ["res/sound/sound_g89/music_rukoujiemian.fsb", "res/sound/music/music_chushengdao_rulesofsurvival.fsb"]:
        data = z.read(name)
        magic, ver, num_samples, shdr_size, name_size, data_size, mode = struct.unpack_from("<4sIIIIII", data, 0)
        print(f"=== {name} ===")
        print(f"ver={ver}, num_samples={num_samples}, shdr_size={shdr_size}, name_size={name_size}, data_size={data_size}, mode={mode}")
        # sample headers start at offset 0x3C (60) or 0x40 depending on flags
        # In FSB5 standard header is 0x3C or 0x40
        # Let's inspect raw header bytes
        hdr_bytes = data[:0x40]
        print("Header hex:", hdr_bytes.hex())
