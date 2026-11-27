import os
import glob
from PIL import Image

def build_loading_screens():
    print("Building modern loading screens...")
    out_dir = "scratch/patch_res/loading"
    os.makedirs(out_dir, exist_ok=True)
    
    airdrop_src = "C:/Users/Lufy/.gemini/antigravity/brain/c744c4c4-aaed-4b8b-9e65-5d71627bc1d9/ros_loading_airdrop_1794908732046.jpg"
    squad_src = "C:/Users/Lufy/.gemini/antigravity/brain/c744c4c4-aaed-4b8b-9e65-5d71627bc1d9/ros_loading_tactical_squad_1794908749604.jpg"
    battle_src = "scratch/ros_banner_clean.jpg"
    
    img_airdrop = Image.open(airdrop_src).convert("RGB")
    img_squad = Image.open(squad_src).convert("RGB")
    img_battle = Image.open(battle_src).convert("RGB")
    
    # Define mapping of loading screen targets:
    # 1. 1280x960 full backgrounds (4:3 / tablet / high-res)
    targets_1280x960 = [
        "bg_loading_01", "bg_loading_02", "bg_loading_03", "bg_loading_04",
        "bg_loading_05", "bg_loading_06", "bg_loading_07", "bg_loading_08",
        "bg_loading_oasis", "bg_loading_slums", "bg_loading_irontown", "bg_loading_test",
        "bg_vehicle", "jiangjinsai"
    ]
    
    # 2. 1024x768 backgrounds
    targets_1024x768 = [
        "bg_loading_dts", "loading_0", "loading_2", "loading_3", "loading_4",
        "loading_5", "loading_7", "loading_8", "loading_9", "loading_10",
        "loading_11", "loading_13"
    ]
    
    # 3. 1024x480 widescreen banners
    targets_1024x480 = [
        "loading_1"
    ]
    
    # 4. PC / Nova loadings
    pc_targets = [f"pc_loading_{i}" for i in range(1, 14)]
    nova_targets = [f"huawei_nova_loading_{i}" for i in range(1, 14)]
    
    # Rotating sources for variety
    sources = [img_airdrop, img_squad, img_battle]
    
    def export_asset(name, width, height, src_img):
        # Resize/crop to fill exact target aspect ratio
        sw, sh = src_img.size
        target_ratio = width / height
        src_ratio = sw / sh
        
        if src_ratio > target_ratio:
            # Source is wider: crop sides
            new_w = int(sh * target_ratio)
            offset = (sw - new_w) // 2
            crop_box = (offset, 0, offset + new_w, sh)
        else:
            # Source is taller: crop top/bottom
            new_h = int(sw / target_ratio)
            offset = (sh - new_h) // 2
            crop_box = (0, offset, sw, offset + new_h)
            
        cropped = src_img.crop(crop_box).resize((width, height), Image.LANCZOS)
        
        # Save as .pkm (which is JPEG inside for loading screens), .jpg, and .png
        pkm_path = os.path.join(out_dir, f"{name}.pkm")
        jpg_path = os.path.join(out_dir, f"{name}.jpg")
        png_path = os.path.join(out_dir, f"{name}.png")
        
        cropped.save(pkm_path, "JPEG", quality=95)
        cropped.save(jpg_path, "JPEG", quality=95)
        cropped.save(png_path, "PNG")
        
        # Also provide white alpha .alpha.pkm just in case engine checks it
        alpha_pkm_path = os.path.join(out_dir, f"{name}.alpha.pkm")
        white_alpha = Image.new("L", (width, height), 255)
        white_alpha.convert("RGB").save(alpha_pkm_path, "JPEG", quality=90)
    
    idx = 0
    for name in targets_1280x960:
        src = sources[idx % len(sources)]
        export_asset(name, 1280, 960, src)
        idx += 1
        
    for name in targets_1024x768:
        src = sources[idx % len(sources)]
        export_asset(name, 1024, 768, src)
        idx += 1
        
    for name in targets_1024x480:
        src = sources[idx % len(sources)]
        export_asset(name, 1024, 480, src)
        idx += 1
        
    for name in pc_targets + nova_targets:
        src = sources[idx % len(sources)]
        export_asset(name, 1280, 720, src)
        idx += 1
        
    print(f"Exported all {idx} loading screen variants into {out_dir}!")

if __name__ == "__main__":
    build_loading_screens()
