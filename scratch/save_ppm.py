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

# Save a PPM file (simple uncompressed format)
with open(r"c:\Users\Lufy\Desktop\Server\screen.ppm", "wb") as f:
    f.write(f"P6\n{w} {h}\n255\n".encode())
    for y in range(h):
        row = bytearray()
        off = y * stride + 1
        for x in range(w):
            r, g, b, a = raw[off + x*4 : off + x*4 + 4]
            row.extend([r, g, b])
        f.write(row)
print("Saved screen.ppm successfully!")
