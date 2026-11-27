import zipfile, struct

obb = r"decompile\xapk\patch.1227927.com.netease.chiji.obb"
with zipfile.ZipFile(obb, 'r') as z:
    data = z.read("res/sound/music/music_chushengdao_rulesofsurvival.fsb")
    # Base header (60 bytes)
    # '4s I I I I I I 8s 16s 8s'
    fields = struct.unpack('<4sIIIIII8s16s8s', data[:60])
    print("Magic:", fields[0])
    print("Version:", fields[1])
    print("numSamples:", fields[2])
    print("sampleHeadersSize:", fields[3])
    print("nameTableSize:", fields[4])
    print("dataSize:", fields[5])
    print("mode:", fields[6])
    print("zero:", fields[7].hex())
    print("hash:", fields[8].hex())
    print("dummy:", fields[9].hex())
    print("Sample header:", data[60:80].hex())
    print("Name table:", data[80:128])
