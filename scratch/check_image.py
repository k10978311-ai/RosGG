from PIL import Image

im = Image.open(r"c:\Users\Lufy\Desktop\Server\current_screen.png")
print("Size:", im.size)

# Sample some pixel colors around the center to see if dialog is up
# Dialog background in center is dark/semi-transparent
# Play button around (800, 730) has white/light-blue text
center_pixel = im.getpixel((800, 450))
play_pixel = im.getpixel((800, 730))
print("Center (800, 450):", center_pixel)
print("Play (800, 730):", play_pixel)
