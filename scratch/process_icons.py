import os
import sys
from PIL import Image, ImageDraw, ImageFilter


def create_squircle_mask(size, radius_ratio=0.22):
    w, h = size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    r = int(min(w, h) * radius_ratio)
    draw.rounded_rectangle([0, 0, w, h], radius=r, fill=255)
    return mask


def create_circular_mask(size):
    w, h = size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([0, 0, w, h], fill=255)
    return mask


def make_preview_card(icon_img, label="Rules of Survival"):
    # Generate 320x320 dark preview card showing app icon on dark home screen
    card = Image.new("RGBA", (320, 320), (18, 20, 26, 255))
    
    # Resize icon to 160x160 with squircle
    icon_resized = icon_img.resize((160, 160), Image.Resampling.LANCZOS).convert("RGBA")
    mask = create_squircle_mask((160, 160), 0.22)
    
    # Soft drop shadow
    shadow = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([10, 14, 170, 174], radius=35, fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    card.paste(shadow, (70, 42), shadow)
    
    # Paste squircle icon
    card.paste(icon_resized, (80, 50), mask)
    
    return card


def export_android_icon_set(src_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    img = Image.open(src_path).convert("RGBA")
    
    # Android mipmap dimensions
    sizes = {
        "mipmap-xxxhdpi": 192,
        "mipmap-xxhdpi": 144,
        "mipmap-xhdpi": 96,
        "mipmap-hdpi": 72,
        "mipmap-mdpi": 48,
        "store-512": 512,
    }
    
    exported = {}
    for folder, dim in sizes.items():
        resized = img.resize((dim, dim), Image.Resampling.LANCZOS)
        out_path = os.path.join(out_dir, f"ic_launcher_{dim}x{dim}.png")
        resized.save(out_path, "PNG")
        exported[folder] = out_path
        
    return exported


if __name__ == "__main__":
    if len(sys.argv) > 1:
        export_android_icon_set(sys.argv[1], "scratch/generated_icons")
