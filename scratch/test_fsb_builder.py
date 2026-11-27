import subprocess, struct, os, fsb5

def build_fsb5_mp3(mp3_bytes, sample_count, sample_name="g89_rulesofsurvival", loop=True):
    # Base header: 60 bytes
    # Mode 11 = MPEG
    num_samples = 1
    sample_headers_size = 20
    
    # Name table:
    # 4 bytes offset table (1 offset = 4 bytes)
    # name + \0
    name_bytes = sample_name.encode('ascii') + b'\x00'
    raw_name_tbl = struct.pack('<I', 4) + name_bytes
    # Pad name table so (60 + sample_headers_size + len(name_tbl)) is aligned to 32 bytes
    hdr_and_shdr = 60 + sample_headers_size
    pad_len = (32 - ((hdr_and_shdr + len(raw_name_tbl)) % 32)) % 32
    # But wait, original nameTableSize was 48 bytes.
    # 60 + 20 = 80. 80 + 48 = 128 (aligned to 32).
    # If len(raw_name_tbl) is 4 + 20 = 24. 48 - 24 = 24 padding.
    target_name_size = len(raw_name_tbl) + pad_len
    if (hdr_and_shdr + target_name_size) % 32 != 0:
        target_name_size += 32 - ((hdr_and_shdr + target_name_size) % 32)
    name_tbl = raw_name_tbl + (b'\x00' * (target_name_size - len(raw_name_tbl)))
    name_table_size = len(name_tbl)
    
    data_size = len(mp3_bytes)
    # Pad mp3 data to 32 bytes alignment if needed
    data_pad = (32 - (data_size % 32)) % 32
    mp3_padded = mp3_bytes + (b'\x00' * data_pad)
    data_size = len(mp3_padded)
    
    # Sample header (20 bytes):
    # raw Q bitfields:
    # bit 0: next_chunk = 1 (has LOOP chunk)
    # bit 1..4: frequency index (8 = 44100 Hz)
    # bit 5: channels - 1 (channels=2 -> 1)
    # bit 6..33 (28 bits): dataOffset / 16 = 0
    # bit 34..63 (30 bits): sample_count
    freq_idx = 8 # 44100
    chan_flag = 1 # 2 channels
    raw_q = 1 | (freq_idx << 1) | (chan_flag << 5) | (0 << 6) | ((sample_count & 0x3FFFFFFF) << 34)
    
    # Loop chunk (12 bytes):
    # next_chunk = 0 (1 bit)
    # chunk_size = 8 (24 bits)
    # chunk_type = 3 (7 bits) -> MetadataChunkType.LOOP
    chunk_hdr = 0 | (8 << 1) | (3 << 25)
    loop_start = 0
    loop_end = max(0, sample_count - 1000)
    
    shdr = struct.pack('<QIII', raw_q, chunk_hdr, loop_start, loop_end)
    assert len(shdr) == 20
    
    zero = b'\x00\x00\x02\x00\x00\x00\x00\x00'
    dummy_hash = b'\x18\t\x87\xc9I\xd50\x11/A\x8cJ\x959\xae\x18'
    dummy_tail = b'&\x9a\x14\xb0\x1b\xb9}\xa7'
    
    base_hdr = struct.pack(
        '<4sIIIIII8s16s8s',
        b'FSB5',
        1, # version
        num_samples,
        sample_headers_size,
        name_table_size,
        data_size,
        11, # SoundFormat.MPEG
        zero,
        dummy_hash,
        dummy_tail
    )
    
    return base_hdr + shdr + name_tbl + mp3_padded

# Let's test with the user's downloaded music!
# First re-encode scratch/game_music.mp3 to standard CBR 44100 stereo MP3 without ID3 tags
ffmpeg_path = r"C:\Users\Lufy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
ffprobe_path = r"C:\Users\Lufy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffprobe.exe"

out_cbr = r"scratch\game_music_44k_cbr.mp3"
subprocess.run([
    ffmpeg_path, "-y", "-i", r"scratch\game_music.mp3",
    "-ar", "44100", "-ac", "2", "-b:a", "128k",
    "-write_xing", "0", "-id3v2_version", "0",
    out_cbr
], check=True, capture_output=True)

# Get sample count from ffprobe
res = subprocess.run([
    ffprobe_path, "-v", "error", "-select_streams", "a:0",
    "-show_entries", "stream=duration,nb_samples",
    "-of", "csv=p=0", out_cbr
], capture_output=True, text=True)
print("ffprobe stream info:", res.stdout.strip())

# Or calculate exact samples from duration * 44100
dur_res = subprocess.run([
    ffprobe_path, "-v", "error", "-show_entries", "format=duration",
    "-of", "csv=p=0", out_cbr
], capture_output=True, text=True)
duration = float(dur_res.stdout.strip())
sample_count = int(duration * 44100)
print(f"Duration: {duration}s, sample_count: {sample_count}")

with open(out_cbr, "rb") as f:
    mp3_data = f.read()

fsb_bytes = build_fsb5_mp3(mp3_data, sample_count, "g89_rulesofsurvival")
out_fsb = r"scratch\music_chushengdao_rulesofsurvival.fsb"
with open(out_fsb, "wb") as f:
    f.write(fsb_bytes)

print(f"Wrote {len(fsb_bytes)} bytes to {out_fsb}")

# Now verify with fsb5 library!
parsed = fsb5.load(fsb_bytes)
print("Verification successful!")
print("Header:", parsed.header)
print("Sample:", parsed.samples[0])
