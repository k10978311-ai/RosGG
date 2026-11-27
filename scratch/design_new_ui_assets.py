import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

font_path_title = "C:/Windows/Fonts/bahnschrift.ttf"
font_path_regular = "C:/Windows/Fonts/segoeui.ttf"
if not os.path.exists(font_path_title):
    font_path_title = "C:/Windows/Fonts/arialbd.ttf"
if not os.path.exists(font_path_regular):
    font_path_regular = "C:/Windows/Fonts/arial.ttf"

def create_modern_logo():
    """Create modern high-res title logo (502x317) with transparent background."""
    w, h = 502, 317
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    f_rules = get_font(font_path_title, 56)
    f_of = get_font(font_path_title, 24)
    f_survival = get_font(font_path_title, 64)
    f_sub = get_font(font_path_title, 18)
    
    # 1. Main Title: "RULES OF SURVIVAL"
    # "RULES"
    # Drop shadow
    for ox, oy in [(-3, 3), (3, 3), (0, 4), (-2, 2), (2, 2)]:
        draw.text((w // 2 - 190 + ox, 60 + oy), "RULES", font=f_rules, fill=(5, 10, 20, 200))
    draw.text((w // 2 - 190, 60), "RULES", font=f_rules, fill=(255, 255, 255, 255))
    
    # "OF" badge
    draw.rounded_rectangle([w // 2 + 105, 78, w // 2 + 160, 116], radius=6, fill=(20, 30, 48, 220), outline=(70, 130, 210, 240), width=1)
    draw.text((w // 2 + 118, 83), "OF", font=f_of, fill=(180, 220, 255, 255))
    
    # "SURVIVAL"
    for ox, oy in [(-3, 3), (3, 3), (0, 4), (-2, 2), (2, 2)]:
        draw.text((w // 2 - 200 + ox, 130 + oy), "SURVIVAL", font=f_survival, fill=(5, 10, 20, 200))
    draw.text((w // 2 - 200, 130), "SURVIVAL", font=f_survival, fill=(255, 255, 255, 255))
    
    # 2. Modern Subtitle Banner (Replacing old www.rulesofsurvivalgame.com)
    # Golden Cyber Capsule
    badge_x1 = w // 2 - 210
    badge_y1 = 225
    badge_x2 = w // 2 + 210
    badge_y2 = 265
    
    draw.rounded_rectangle([badge_x1 - 2, badge_y1 - 2, badge_x2 + 2, badge_y2 + 2], radius=8, fill=(255, 180, 0, 40))
    draw.rounded_rectangle([badge_x1, badge_y1, badge_x2, badge_y2], radius=6, fill=(15, 22, 35, 230), outline=(255, 195, 20, 255), width=2)
    
    sub_text = "PRIVATE SERVER  •  BATTLE ROYALE 2.0"
    st_len = draw.textlength(sub_text, font=f_sub)
    draw.text((w // 2 - st_len / 2, badge_y1 + 8), sub_text, font=f_sub, fill=(255, 210, 40, 255))
    
    # Sleek bottom accent line
    draw.line([(w // 2 - 120, 280), (w // 2 + 120, 280)], fill=(70, 140, 225, 200), width=2)
    
    return img

def create_modern_play_btn():
    """Create modern glowing Start Game / PLAY button (838x159)."""
    w, h = 838, 159
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    f_play = get_font(font_path_title, 72)
    
    # Play text with golden / electric cyber styling
    play_txt = "—   P L A Y   —"
    tw = draw.textlength(play_txt, font=f_play)
    tx = w // 2 - tw / 2
    ty = h // 2 - 45
    
    # Deep outer drop glow
    for radius in [12, 8, 4]:
        for ox in range(-radius, radius + 1, 3):
            for oy in range(-radius, radius + 1, 3):
                draw.text((tx + ox, ty + oy), play_txt, font=f_play, fill=(255, 170, 0, 50))
    
    # Crisp drop shadow
    for ox, oy in [(-3, 3), (3, 3), (0, 4), (-2, 2), (2, 2)]:
        draw.text((tx + ox, ty + oy), play_txt, font=f_play, fill=(10, 15, 25, 230))
        
    # Main golden/white face
    draw.text((tx, ty), play_txt, font=f_play, fill=(255, 250, 230, 255))
    
    return img

if __name__ == "__main__":
    logo = create_modern_logo()
    logo.save("scratch/test_modern_logo.png")
    
    play = create_modern_play_btn()
    play.save("scratch/test_modern_play.png")
    print("Generated modern logo and play button preview!")
