from PIL import Image
im = Image.open('scratch/after_skip.png')
# search for white pixels of SKIP around x: 950..1200, y: 10..70
print('image size:', im.size)
hits = []
for y in range(0, 100):
    for x in range(950, 1200):
        r, g, b, a = im.getpixel((x, y))
        if r > 240 and g > 240 and b > 240:
            hits.append((x, y))
if hits:
    min_x = min(x for x, y in hits)
    max_x = max(x for x, y in hits)
    min_y = min(y for x, y in hits)
    max_y = max(y for x, y in hits)
    print(f'SKIP bbox: x=({min_x}, {max_x}), y=({min_y}, {max_y}), center=({(min_x+max_x)//2}, {(min_y+max_y)//2})')
else:
    print('no white pixels found')
