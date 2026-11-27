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
font_path_bold = "C:/Windows/Fonts/segoeuib.ttf"
if not os.path.exists(font_path_title):
    font_path_title = "C:/Windows/Fonts/arialbd.ttf"
if not os.path.exists(font_path_regular):
    font_path_regular = "C:/Windows/Fonts/arial.ttf"
if not os.path.exists(font_path_bold):
    font_path_bold = "C:/Windows/Fonts/arialbd.ttf"

def draw_beveled_text(draw, pos, text, font, fill_color, bevel_light=(255, 255, 255, 220), bevel_dark=(20, 30, 45, 240), shadow_color=(5, 10, 20, 240), shadow_dist=4):
    x, y = pos
    # 1. Deep drop shadow
    for r in range(1, shadow_dist + 1):
        for ox in [-r, 0, r]:
            for oy in [r, r + 1]:
                draw.text((x + ox, y + oy), text, font=font, fill=shadow_color)
    # 2. Bevel dark outline (bottom/right)
    draw.text((x + 1, y + 1), text, font=font, fill=bevel_dark)
    draw.text((x + 2, y + 2), text, font=font, fill=bevel_dark)
    # 3. Bevel light highlight (top/left)
    draw.text((x - 1, y - 1), text, font=font, fill=bevel_light)
    # 4. Main text face
    draw.text((x, y), text, font=font, fill=fill_color)

def create_modern_logo_master():
    """Create high-end modern Battle Royale logo (502x317)."""
    w, h = 502, 317
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    f_rules = get_font(font_path_title, 54)
    f_of = get_font(font_path_bold, 20)
    f_survival = get_font(font_path_title, 64)
    f_sub = get_font(font_path_bold, 16)
    f_badge = get_font(font_path_bold, 13)
    
    # --- Top Banner Badge: "PRIVATE SERVER EDITION" ---
    badge_w, badge_h = 320, 30
    bx1 = w // 2 - badge_w // 2
    by1 = 20
    bx2 = bx1 + badge_w
    by2 = by1 + badge_h
    
    # Subtle outer glow for badge
    draw.rounded_rectangle([bx1 - 3, by1 - 3, bx2 + 3, by2 + 3], radius=8, fill=(0, 200, 255, 40))
    # Badge background
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill=(12, 22, 38, 245), outline=(0, 210, 255, 230), width=2)
    
    badge_txt = "★   BATTLE ROYALE 2.0   ★"
    bw = draw.textlength(badge_txt, font=f_badge)
    draw.text((w // 2 - bw / 2, by1 + 6), badge_txt, font=f_badge, fill=(0, 235, 255, 255))
    
    # --- Main Title: RULES OF ---
    rx = w // 2 - 185
    ry = 65
    draw_beveled_text(draw, (rx, ry), "RULES", font=f_rules, fill_color=(250, 252, 255, 255),
                      bevel_light=(255, 255, 255, 255), bevel_dark=(30, 45, 70, 255),
                      shadow_color=(5, 12, 24, 250), shadow_dist=5)
    
    # "OF" hex / capsule badge
    of_x = w // 2 + 100
    of_y = 80
    draw.rounded_rectangle([of_x, of_y, of_x + 55, of_y + 36], radius=6, fill=(20, 35, 60, 240), outline=(255, 195, 30, 240), width=2)
    draw.text((of_x + 13, of_y + 7), "OF", font=f_of, fill=(255, 215, 60, 255))
    
    # --- Main Title: SURVIVAL ---
    sx = w // 2 - 195
    sy = 135
    draw_beveled_text(draw, (sx, sy), "SURVIVAL", font=f_survival, fill_color=(255, 255, 255, 255),
                      bevel_light=(255, 255, 255, 255), bevel_dark=(35, 45, 65, 255),
                      shadow_color=(5, 12, 24, 250), shadow_dist=6)
    
    # --- Tactical Accent Lines ---
    line_y = 222
    # Left wing line
    draw.line([(w // 2 - 210, line_y), (w // 2 - 50, line_y)], fill=(255, 195, 30, 220), width=3)
    draw.line([(w // 2 - 210, line_y - 4), (w // 2 - 140, line_y - 4)], fill=(0, 200, 255, 180), width=1)
    # Right wing line
    draw.line([(w // 2 + 50, line_y), (w // 2 + 210, line_y)], fill=(255, 195, 30, 220), width=3)
    draw.line([(w // 2 + 140, line_y - 4), (w // 2 + 210, line_y - 4)], fill=(0, 200, 255, 180), width=1)
    # Center diamond
    draw.polygon([(w // 2, line_y - 6), (w // 2 + 8, line_y), (w // 2, line_y + 6), (w // 2 - 8, line_y)], fill=(255, 215, 60, 255))
    
    # --- Modern Subtitle ---
    sub_txt = "RULES OF SURVIVAL PRIVATE SERVER"
    sub_w = draw.textlength(sub_txt, font=f_sub)
    draw.text((w // 2 - sub_w / 2 + 2, 238 + 2), sub_txt, font=f_sub, fill=(5, 12, 24, 240))
    draw.text((w // 2 - sub_w / 2, 238), sub_txt, font=f_sub, fill=(240, 245, 255, 255))
    
    # Sleek bottom border
    draw.line([(w // 2 - 90, 272), (w // 2 + 90, 272)], fill=(0, 210, 255, 200), width=2)
    
    return img

def create_modern_play_btn_master():
    """Create high-end modern Start Game / PLAY button (838x159)."""
    w, h = 838, 159
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    f_play = get_font(font_path_title, 76)
    
    # Play text with golden & cyan high-tech styling
    play_txt = "[   —   P L A Y   —   ]"
    tw = draw.textlength(play_txt, font=f_play)
    tx = w // 2 - tw / 2
    ty = h // 2 - 48
    
    # 1. Soft cyber glow layer
    for radius in [14, 10, 6]:
        for ox in range(-radius, radius + 1, 4):
            for oy in range(-radius, radius + 1, 4):
                draw.text((tx + ox, ty + oy), play_txt, font=f_play, fill=(255, 185, 20, 45))
    
    # 2. Deep drop shadow
    for ox, oy in [(-3, 3), (3, 3), (0, 5), (-2, 2), (2, 2), (0, 3)]:
        draw.text((tx + ox, ty + oy), play_txt, font=f_play, fill=(8, 14, 25, 240))
        
    # 3. Metallic bevel highlight
    draw.text((tx - 1, ty - 1), play_txt, font=f_play, fill=(255, 255, 255, 230))
    draw.text((tx + 1, ty + 1), play_txt, font=f_play, fill=(180, 130, 20, 255))
    
    # 4. Main face: radiant warm platinum/gold
    draw.text((tx, ty), play_txt, font=f_play, fill=(255, 252, 240, 255))
    
    return img

if __name__ == "__main__":
    logo = create_modern_logo_master()
    logo.save("scratch/master_modern_logo.png")
    
    play = create_modern_play_btn_master()
    play.save("scratch/master_modern_play.png")
    print("Master modern logo and play button rendered successfully!")
