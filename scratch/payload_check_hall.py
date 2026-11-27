import sys
import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        f.write("Player: %r (id=%s)\n" % (p, getattr(p, "id", None)))
        f.write("hallScene: %r\n" % getattr(p, "hallScene", None))
        
        # Check packages
        pkg = getattr(p, "dtsAppearancePackage", None)
        if pkg:
            items = getattr(pkg, "itemList", {})
            f.write("Appearance Package skins: %d items\n" % len(items))
            f.write("Skin IDs: %r\n" % sorted(items.keys()))
            
        rep = getattr(p, "dtsRos2RepertoryPackage", None)
        if rep:
            r_items = getattr(rep, "itemList", {})
            f.write("Repertory (Depot) items: %d items\n" % len(r_items))

        # Check SceneSystem
        import SceneSystem
        ss = getattr(SceneSystem, "getInstance", lambda: None)()
        f.write("SceneSystem: %r\n" % ss)
        if ss:
            f.write("  curScene: %r\n" % getattr(ss, "curScene", None))
            f.write("  nextScene: %r\n" % getattr(ss, "nextScene", None))
            f.write("  isLoading: %r\n" % getattr(ss, "isLoading", None))
            f.write("  isSceneLoading: %r\n" % getattr(ss, "isSceneLoading", None))
            
        # Check active coroutines
        import ss as _ss_mod
        f.write("ss module: %r\n" % dir(_ss_mod))
    except Exception:
        f.write(traceback.format_exc())
