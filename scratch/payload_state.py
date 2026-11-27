import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        f.write("player: %r (class=%s, id=%s)\n" % (p, type(p).__name__, getattr(p, "id", None)))
        if p:
            f.write("name: %s\n" % getattr(p, "playerName", None))
            f.write("charType: %s\n" % getattr(p, "baseCharacterType", None))
            f.write("freeYuanbao: %s, payYuanbao: %s\n" % (getattr(p, "freeYuanbao", None), getattr(p, "payYuanbao", None)))
            
            # Appearance Package
            pkg = getattr(p, "dtsAppearancePackage", None)
            f.write("dtsAppearancePackage: %r\n" % (type(pkg).__name__ if pkg else None))
            if pkg:
                raw_items = getattr(pkg, "itemList", {})
                if isinstance(raw_items, dict):
                    items = raw_items.values()
                else:
                    items = list(raw_items)
                f.write("appearance item count: %d\n" % len(items))
                item_ids = [getattr(it, "itemID", None) for it in items[:30]]
                f.write("appearance itemIDs: %r\n" % item_ids)
            
            # Outfits / Wearable / Body
            f.write("showWearable: %r\n" % getattr(p, "dtsShowWearableAppearanceList", None))
            f.write("showBody: %r\n" % getattr(p, "dtsShowBodyAppearanceList", None))

            # Currencies
            curs = getattr(p, "currencyList", None)
            f.write("currencyList: %r\n" % curs)
            
            # Repertory / Depot
            rep = getattr(p, "dtsRos2RepertoryPackage", None)
            f.write("dtsRos2RepertoryPackage: %r\n" % (type(rep).__name__ if rep else None))
            if rep:
                raw_r = getattr(rep, "itemList", {})
                r_items = raw_r.values() if isinstance(raw_r, dict) else list(raw_r)
                f.write("repertory item count: %d\n" % len(r_items))
                
        # UI manager & Scene
        import Globals
        ui_mgr = getattr(Globals, "uiMgr", None)
        if ui_mgr:
            f.write("ui_dict keys: %r\n" % (list(getattr(ui_mgr, "_ui_dict", {}).keys()),))
            visible = [k for k, v in getattr(ui_mgr, "_ui_dict", {}).items() if getattr(v, "visible", False)]
            f.write("visible UIs: %r\n" % (visible,))
            
        import game_scene_mgr
        gsm = getattr(game_scene_mgr, "getInstance", lambda: None)()
        f.write("current scene: %r\n" % (getattr(gsm, "cur_scene_name", None) if gsm else None))
    except Exception:
        f.write(traceback.format_exc())
