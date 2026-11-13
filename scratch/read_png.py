import struct, zlib

# Read PNG using pure python
with open(r"c:\Users\Lufy\Desktop\Server\current_screen.png", "rb") as f:
    data = f.read()

# Parse PNG header
w, h = struct.unpack(">II", data[16:24])
print(f"PNG image: {w}x{h}")

# Find IDAT chunks
idat = bytearray()
pos = 8
while pos < len(data):
    length = struct.unpack(">I", data[pos:pos+4])[0]
    ctype = data[pos+4:pos+8]
    if ctype == b"IDAT":
        idat.extend(data[pos+8:pos+8+length])
    pos += 8 + length + 4

raw = zlib.decompress(idat)
# Each row has 1 filter byte + w*4 bytes (RGBA)
stride = 1 + w * 4
print("Decompressed bytes:", len(raw), "expected:", stride * h)

def get_pixel(x, y):
    offset = y * stride + 1 + x * 4
    return tuple(raw[offset:offset+4])

print("Center (800, 450):", get_pixel(800, 450))
print("Point (800, 500):", get_pixel(800, 500))
print("Point (800, 700):", get_pixel(800, 700))
print("Point (800, 740):", get_pixel(800, 740))

# Search vertically along x=800 for brightness or buttons
samples = []
for y in range(0, h, 20):
    samples.append((y, get_pixel(800, y)))

for y, p in samples[20:]:
    print(f"y={y:3d}: RGBA={p}")
