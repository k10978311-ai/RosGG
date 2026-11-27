import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def draw_vector_icon(draw, cx, cy, icon_name, color=(220, 240, 255, 240)):
    """Draw crisp minimalist vector icons for game UI dock."""
    if icon_name == "NOTICE":
        # Megaphone / Bell
        draw.polygon([(cx - 10, cy - 3), (cx - 10, cy + 3), (cx - 2, cy + 6), (cx - 2, cy - 6)], outline=color, fill=None, width=2)
        draw.arc([cx - 4, cy - 10, cx + 10, cy + 10], start=-45, end=45, fill=color, width=2)
        draw.line([(cx - 10, cy + 3), (cx - 7, cy + 9)], fill=color, width=2)
    elif icon_name == "REPAIR":
        # Wrench
        draw.line([(cx - 8, cy + 8), (cx + 4, cy - 4)], fill=color, width=3)
        draw.arc([cx + 2, cy - 10, cx + 12, cy], start=60, end=300, fill=color, width=2)
    elif icon_name == "ACCOUNT":
        # User profile
        draw.ellipse([cx - 5, cy - 10, cx + 5, cy], outline=color, width=2)
        draw.arc([cx - 10, cy + 2, cx + 10, cy + 14], start=180, end=360, fill=color, width=2)
    elif icon_name == "LANGUAGE":
        # Globe
        draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=color, width=2)
        draw.ellipse([cx - 4, cy - 9, cx + 4, cy + 9], outline=color, width=1)
        draw.line([(cx - 9, cy), (cx + 9, cy)], fill=color, width=1)
    elif icon_name == "SETTINGS":
        # Gear
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=color, width=2)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=color)
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1 = cx + int(7 * math.cos(rad))
            y1 = cy + int(7 * math.sin(rad))
            x2 = cx + int(10 * math.cos(rad))
            y2 = cy + int(10 * math.sin(rad))
            draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
    elif icon_name == "QUIT":
        # Power / Exit
        draw.arc([cx - 8, cy - 7, cx + 8, cy + 9], start=30, end=150, fill=color, width=2)
        draw.arc([cx - 8, cy - 7, cx + 8, cy + 9], start=210, end=330, fill=color, width=2)
        draw.line([(cx, cy - 9), (cx, cy + 1)], fill=color, width=2)

def create_refactored_ui():
    bg_path = "scratch/ros_banner_clean.jpg"
    if not os.path.exists(bg_path):
        bg_path = "ros_banner_clean.jpg"
    
    base = Image.open(bg_path).convert("RGBA")
    w, h = base.size
    
    if (w, h) != (1920, 1080):
        base = base.resize((1920, 1080), Image.Resampling.LANCZOS)
        w, h = 1920, 1080

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    font_path_title = "C:/Windows/Fonts/bahnschrift.ttf"
    font_path_regular = "C:/Windows/Fonts/segoeui.ttf"
    if not os.path.exists(font_path_title):
        font_path_title = "C:/Windows/Fonts/arialbd.ttf"
    if not os.path.exists(font_path_regular):
        font_path_regular = "C:/Windows/Fonts/arial.ttf"

    def get_font(path, size):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            return ImageFont.load_default()

    f_title = get_font(font_path_title, 68)
    f_subtitle = get_font(font_path_title, 20)
    f_play = get_font(font_path_title, 36)
    f_srv = get_font(font_path_regular, 21)
    f_srv_sub = get_font(font_path_regular, 14)
    f_dock = get_font(font_path_regular, 12)
    f_badge = get_font(font_path_title, 14)

    # 1. Subtle cinematic vignettes
    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    for y in range(150):
        alpha = int(150 * (1.0 - y / 150.0))
        v_draw.line([(0, y), (w, y)], fill=(8, 12, 22, alpha))
    for y in range(h - 240, h):
        progress = (y - (h - 240)) / 240.0
        alpha = int(190 * progress)
        v_draw.line([(0, y), (w, y)], fill=(6, 10, 18, alpha))
    overlay = Image.alpha_composite(overlay, vignette)
    draw = ImageDraw.Draw(overlay)

    # 2. Top Header Bar
    # Top Left: Version Badge
    draw.rounded_rectangle([40, 28, 300, 74], radius=8, fill=(12, 18, 30, 200), outline=(50, 85, 130, 220), width=1)
    draw.text((55, 36), "RULES OF SURVIVAL 2.0", font=f_badge, fill=(255, 255, 255, 255))
    draw.text((55, 53), "BUILD 1.610637 • CLIENT NA-PROD", font=get_font(font_path_regular, 12), fill=(130, 180, 230, 230))

    # Top Right: Server Connection Status
    draw.rounded_rectangle([w - 440, 28, w - 40, 74], radius=8, fill=(12, 18, 30, 200), outline=(50, 85, 130, 220), width=1)
    draw.ellipse([w - 425, 46, w - 413, 58], fill=(46, 213, 115, 255))
    draw.text((w - 400, 36), "MERCURY GATEWAY: CONNECTED", font=f_badge, fill=(245, 250, 255, 255))
    draw.text((w - 400, 53), "PORT: 25000 UDP  |  PING: 12ms  |  STATUS: LOGGED_ON", font=get_font(font_path_regular, 11), fill=(135, 190, 235, 225))

    # 3. Main Center Title Branding
    center_x = w // 2 + 50
    title_text = "RULES OF SURVIVAL"
    sub_text = "BATTLE ROYALE  •  PRIVATE SERVER EDITION"
    
    t_len = draw.textlength(title_text, font=f_title)
    s_len = draw.textlength(sub_text, font=f_subtitle)
    
    t_x = center_x - t_len / 2
    s_x = center_x - s_len / 2

    # Drop shadow & halo for title
    for ox in range(-3, 4):
        for oy in range(-3, 4):
            if ox != 0 or oy != 0:
                draw.text((t_x + ox, 135 + oy), title_text, font=f_title, fill=(5, 10, 20, 140))
    draw.text((t_x, 135), title_text, font=f_title, fill=(255, 255, 255, 255))

    # Subtitle with contrast back-plate
    sub_bg = [s_x - 16, 216, s_x + s_len + 16, 246]
    draw.rounded_rectangle(sub_bg, radius=6, fill=(10, 15, 25, 180), outline=(255, 190, 0, 180), width=1)
    draw.text((s_x, 220), sub_text, font=f_subtitle, fill=(255, 210, 40, 255))

    # 4. Refactored Server Selector Panel
    srv_w = 520
    srv_h = 76
    srv_x1 = center_x - srv_w // 2
    srv_y1 = h - 305
    srv_x2 = srv_x1 + srv_w
    srv_y2 = srv_y1 + srv_h
    
    # Outer cyber glow outline
    draw.rounded_rectangle([srv_x1 - 2, srv_y1 - 2, srv_x2 + 2, srv_y2 + 2], radius=14, outline=(40, 120, 210, 120), width=2)
    draw.rounded_rectangle([srv_x1, srv_y1, srv_x2, srv_y2], radius=12, fill=(15, 24, 38, 220), outline=(65, 135, 225, 240), width=2)
    
    # Pulsing green status dot
    draw.ellipse([srv_x1 + 22, srv_y1 + 28, srv_x1 + 38, srv_y1 + 44], fill=(46, 213, 115, 255))
    draw.ellipse([srv_x1 + 18, srv_y1 + 24, srv_x1 + 42, srv_y1 + 48], outline=(46, 213, 115, 90), width=2)
    
    draw.text((srv_x1 + 54, srv_y1 + 15), "Fast Private-Server [NA / Primary]", font=f_srv, fill=(255, 255, 255, 255))
    draw.text((srv_x1 + 54, srv_y1 + 42), "IP: 192.168.1.18:25000   Latency: 12ms   Load: Normal", font=f_srv_sub, fill=(150, 195, 245, 240))
    # Chevron dropdown button
    draw.rounded_rectangle([srv_x2 - 50, srv_y1 + 18, srv_x2 - 16, srv_y2 - 18], radius=6, fill=(25, 42, 68, 200), outline=(75, 125, 195, 200), width=1)
    draw.polygon([(srv_x2 - 37, srv_y1 + 35), (srv_x2 - 29, srv_y1 + 35), (srv_x2 - 33, srv_y1 + 41)], fill=(200, 230, 255, 255))

    # 5. High-Impact Refactored PLAY Button
    btn_w = 440
    btn_h = 76
    btn_x1 = center_x - btn_w // 2
    btn_y1 = h - 210
    btn_x2 = btn_x1 + btn_w
    btn_y2 = btn_y1 + btn_h

    # Golden cyber glow
    draw.rounded_rectangle([btn_x1 - 8, btn_y1 - 8, btn_x2 + 8, btn_y2 + 8], radius=18, fill=(255, 180, 0, 40))
    # Button main body
    draw.rounded_rectangle([btn_x1, btn_y1, btn_x2, btn_y2], radius=12, fill=(255, 170, 0, 245), outline=(255, 235, 140, 255), width=2)
    # Gloss highlight top half
    draw.rounded_rectangle([btn_x1 + 3, btn_y1 + 3, btn_x2 - 3, btn_y1 + 36], radius=9, fill=(255, 215, 60, 110))
    
    play_txt = "—  P L A Y  —"
    ptw = draw.textlength(play_txt, font=f_play)
    draw.text((center_x - ptw / 2, btn_y1 + 17), play_txt, font=f_play, fill=(20, 15, 5, 255))

    # 6. Right Side Utility Dock
    dock_x = w - 100
    dock_items = ["NOTICE", "REPAIR", "ACCOUNT", "LANGUAGE", "SETTINGS", "QUIT"]
    
    dock_start_y = 160
    dock_h = len(dock_items) * 78 + 20
    draw.rounded_rectangle([dock_x - 18, dock_start_y - 10, dock_x + 68, dock_start_y + dock_h], radius=16, fill=(12, 18, 30, 205), outline=(45, 80, 125, 200), width=1)
    
    for i, label in enumerate(dock_items):
        item_y = dock_start_y + i * 78 + 10
        cx = dock_x + 25
        cy = item_y + 20
        # Button circle
        draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(22, 34, 54, 230), outline=(65, 110, 170, 210), width=1)
        # Vector icon
        draw_vector_icon(draw, cx, cy, label)
        # Label below
        tw = draw.textlength(label, font=f_dock)
        draw.text((cx - tw / 2, item_y + 44), label, font=f_dock, fill=(180, 210, 245, 240))

    # 7. Bottom Ticker / Preservation Notice
    footer_text = "Rules of Survival Preservation Project • Stack: Mercury UDP :25000 / LoginApp / BaseApp • 2026 Edition"
    ftw = draw.textlength(footer_text, font=get_font(font_path_regular, 13))
    draw.text((w // 2 - ftw // 2, h - 42), footer_text, font=get_font(font_path_regular, 13), fill=(160, 195, 230, 210))

    # 8. Bottom-Left Quick Diagnostics Badge
    draw.rounded_rectangle([40, h - 102, 320, h - 42], radius=8, fill=(12, 18, 30, 200), outline=(50, 85, 130, 220), width=1)
    draw.text((55, h - 94), "LOGINAPP & GATE: ACTIVE", font=f_badge, fill=(46, 213, 115, 255))
    draw.text((55, h - 74), "BASEAPP: READY  •  BF SPEC: 1:4  •  HANDSHAKE: OK", font=get_font(font_path_regular, 11), fill=(160, 195, 230, 220))

    # Combine Base + Overlay
    final_img = Image.alpha_composite(base, overlay)
    
    out_refactored_png = "scratch/ros_ui_refactored.png"
    out_refactored_jpg = "scratch/ros_ui_refactored.jpg"
    final_img.convert("RGB").save(out_refactored_png, "PNG", quality=95)
    final_img.convert("RGB").save(out_refactored_jpg, "JPEG", quality=95)
    
    artifact_dir = r"C:\Users\Lufy\.gemini\antigravity\brain\c744c4c4-aaed-4b8b-9e65-5d71627bc1d9"
    final_img.convert("RGB").save(os.path.join(artifact_dir, "ros_ui_refactored.jpg"), "JPEG", quality=95)
    
    print("Refactored UI v2 generated successfully!")

if __name__ == "__main__":
    create_refactored_ui()
