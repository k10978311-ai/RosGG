import zipfile, struct

obb = r"decompile\xapk\patch.1227927.com.netease.chiji.obb"
with zipfile.ZipFile(obb, 'r') as z:
    data = z.read("res/sound/music/music_chushengdao_rulesofsurvival.fsb")
    # Base header: 60 bytes
    magic, ver, num_samples, shdr_size, name_size, data_size, mode = struct.unpack_from("<4sIIIIII", data, 0)
    print(f"Header: ver={ver}, num_samples={num_samples}, shdr_size={shdr_size}, name_size={name_size}, data_size={data_size}, mode={mode}")
    shdr = data[60:60+shdr_size]
    print(f"Sample header ({len(shdr)} bytes):", shdr.hex())
    name_tbl = data[60+shdr_size:60+shdr_size+name_size]
    print(f"Name table ({len(name_tbl)} bytes):", name_tbl)
    raw_audio_start = 60 + shdr_size + name_size
    # Align to 32 bytes if needed:
    print(f"raw_audio_start={raw_audio_start}, hex at start:", data[raw_audio_start:raw_audio_start+32].hex())
    print("ASCII start:", data[raw_audio_start:raw_audio_start+32])
