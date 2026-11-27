import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        if p:
            # Check appearance item attributes
            pkg = getattr(p, "dtsAppearancePackage", None)
            if pkg:
                raw_items = getattr(pkg, "itemList", {})
                first_k = list(raw_items.keys())[0] if raw_items else None
                first_v = raw_items[first_k] if first_k else None
                f.write("item sample key: %r, val: %r, dir: %r\n" % (first_k, first_v, dir(first_v) if first_v else None))
                if first_v:
                    f.write("val dict: %r\n" % getattr(first_v, "__dict__", {}))
                    for attr in ["itemID", "itemId", "item_id", "id", "item_uuid", "uuid", "number", "count", "info"]:
                        if hasattr(first_v, attr):
                            f.write("  attr %s = %r\n" % (attr, getattr(first_v, attr)))

            # Check currencies
            curs = getattr(p, "currencyList", [])
            for i, c in enumerate(curs):
                f.write("cur[%d]: dir=%r\n" % (i, dir(c)))
                for attr in ["id", "type", "count", "val", "currencyType", "currencyValue"]:
                    if hasattr(c, attr):
                        f.write("  cur[%d] %s = %r\n" % (i, attr, getattr(c, attr)))

        # Check scene
        import neoX
        f.write("neoX: %r\n" % dir(neoX))
        import SceneSystem
        ss = getattr(SceneSystem, "getInstance", lambda: None)()
        f.write("SceneSystem: %r, curScene: %r\n" % (ss, getattr(ss, "curScene", None) if ss else None))
        
        import MapSystem
        ms = getattr(MapSystem, "getInstance", lambda: None)()
        f.write("MapSystem: curMapID=%r\n" % (getattr(ms, "curMapID", None) if ms else None))

        import logic
        f.write("logic: %r\n" % dir(logic))
    except Exception:
        f.write(traceback.format_exc())
