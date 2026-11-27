import dts_appearance_utils as dau
import traceback

with open(OUT, "w") as f:
    try:
        sample_ids = [
            120901, 120902, 120903, 120904, 120905, # Weapons
            142080, 142081, 142082, 140105,         # Vehicles
            102568, 102413, 1102319,                # Suits
            1111382, 1111383, 15, 16, 17,           # Wearables
            106500, 106501, 106502,                 # Parachutes
            104932, 104935,                         # Jet wings
            250175, 250153, 250156                  # Head/helmets
        ]
        f.write("=== INSPECTING SEEDED APPEARANCE ITEMS ===\n")
        for iid in sample_ids:
            try:
                name = dau.getDtsAppearanceName(iid) if hasattr(dau, "getDtsAppearanceName") else "N/A"
                desc = dau.getDtsAppearanceDesc(iid) if hasattr(dau, "getDtsAppearanceDesc") else "N/A"
                quality = dau.getDtsAppearanceQuality(iid) if hasattr(dau, "getDtsAppearanceQuality") else "N/A"
                app_type = dau.getDtsAppearanceType(iid) if hasattr(dau, "getDtsAppearanceType") else "N/A"
                icon = dau.getDtsAppearanceIconPath(iid) if hasattr(dau, "getDtsAppearanceIconPath") else "N/A"
                f.write("ID %d: Name=%r, Type=%r, Quality=%r, Icon=%r\n" % (iid, name, app_type, quality, icon))
            except Exception as e:
                f.write("ID %d error: %s\n" % (iid, e))
    except Exception:
        f.write(traceback.format_exc())
