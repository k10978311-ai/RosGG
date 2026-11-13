with open(r"c:\Users\Lufy\Desktop\Server\screen.ppm", "rb") as f:
    header = f.readline()
    dims = f.readline().decode().strip().split()
    w, h = int(dims[0]), int(dims[1])
    maxval = f.readline()
    pixels = f.read()

# Find buttons by searching for borders / background
# Buttons are usually around y=550..620
for y in range(540, 620, 10):
    for x in range(500, 1100, 50):
        off = (y * w + x) * 3
        r, g, b = pixels[off], pixels[off+1], pixels[off+2]
        print(f"({x}, {y}) = RGB({r}, {g}, {b})")
