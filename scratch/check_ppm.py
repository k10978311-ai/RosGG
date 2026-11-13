# Read PPM and check brightness in the notification area (y=400..550, x=400..1200)
with open(r"c:\Users\Lufy\Desktop\Server\screen.ppm", "rb") as f:
    header = f.readline()
    dims = f.readline().decode().strip().split()
    w, h = int(dims[0]), int(dims[1])
    maxval = f.readline()
    pixels = f.read()

# Let's count white/bright pixels in y=400..550
bright_count = 0
for y in range(400, 550):
    for x in range(400, 1200):
        off = (y * w + x) * 3
        r, g, b = pixels[off], pixels[off+1], pixels[off+2]
        if r > 200 and g > 200 and b > 200:
            bright_count += 1

print("Bright text pixels in notification area:", bright_count)

# Let's count in PLAY area (y=700..780, x=700..900)
play_bright = 0
for y in range(700, 780):
    for x in range(700, 900):
        off = (y * w + x) * 3
        r, g, b = pixels[off], pixels[off+1], pixels[off+2]
        if r > 180 and g > 180 and b > 180:
            play_bright += 1
print("Bright text pixels in PLAY area:", play_bright)
