with open(r"c:\Users\Lufy\Desktop\Server\screen.ppm", "rb") as f:
    header = f.readline()
    dims = f.readline().decode().strip().split()
    w, h = int(dims[0]), int(dims[1])
    maxval = f.readline()
    pixels = f.read()

# Let's inspect rows around y=500..650
step_x = 10
step_y = 8
for y in range(450, 650, step_y):
    row = []
    for x in range(400, 1200, step_x):
        off = (y * w + x) * 3
        r, g, b = pixels[off], pixels[off+1], pixels[off+2]
        if r > 200 and g > 200 and b > 200:
            row.append("#")
        elif r > 150 or g > 150 or b > 150:
            row.append("+")
        else:
            row.append(".")
    print(f"y={y:3d} " + "".join(row))
