import struct, zlib

with open(r"c:\Users\Lufy\Desktop\Server\current_screen.png", "rb") as f:
    data = f.read()

w, h = struct.unpack(">II", data[16:24])
idat = bytearray()
pos = 8
while pos < len(data):
    length = struct.unpack(">I", data[pos:pos+4])[0]
    ctype = data[pos+4:pos+8]
    if ctype == b"IDAT":
        idat.extend(data[pos+8:pos+8+length])
    pos += 8 + length + 4

raw = zlib.decompress(idat)
stride = 1 + w * 4

# Let's search in the rectangle [600, 650] to [1000, 850] for the word "PLAY"
# It has bright cyan/white letters (R > 200, G > 200, B > 200)
# Let's print an ASCII art map of pixels in that region!
step_x = 10
step_y = 6
for y in range(650, 800, step_y):
    row = []
    for x in range(650, 950, step_x):
        off = y * stride + 1 + x * 4
        r, g, b, a = raw[off:off+4]
        # check brightness
        if r > 180 and g > 180 and b > 180:
            row.append("#")
        elif b > 180 and g > 180:
            row.append("c")
        else:
            row.append(".")
    print(f"y={y:3d} " + "".join(row))
