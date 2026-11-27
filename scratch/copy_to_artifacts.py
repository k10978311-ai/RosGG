import shutil, os

art_dir = r"C:\Users\Lufy\.gemini\antigravity\brain\1351e113-f720-4968-8d52-364fa84eb18d"
files = [
    ("scratch/game_music.mp3", "game_music.mp3"),
    ("scratch/game_music.ogg", "game_music.ogg"),
    ("scratch/game_music.wav", "game_music.wav"),
    ("scratch/music_chushengdao_rulesofsurvival.fsb", "music_chushengdao_rulesofsurvival.fsb"),
]

for src, dst_name in files:
    dst = os.path.join(art_dir, dst_name)
    shutil.copy2(src, dst)
    print(f"Copied {src} -> {dst} ({os.path.getsize(dst)} bytes)")
