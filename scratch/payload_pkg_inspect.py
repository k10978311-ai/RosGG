import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        pkg = getattr(p, "dtsAppearancePackage", None)
        f.write("pkg: %r\n" % pkg)
        if pkg:
            raw_items = getattr(pkg, "itemList", "NO_ITEMLIST")
            f.write("itemList type: %s, len: %r\n" % (type(raw_items).__name__, len(raw_items) if hasattr(raw_items, '__len__') else None))
            f.write("itemList repr: %r\n" % raw_items)
            f.write("pkg dir: %r\n" % dir(pkg))
    except Exception:
        f.write(traceback.format_exc())
