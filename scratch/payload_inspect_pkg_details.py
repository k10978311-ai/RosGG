import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        pkg = p.dtsAppearancePackage
        f.write("pkg: %r\n" % pkg)
        f.write("pkg.__dict__: %r\n" % getattr(pkg, "__dict__", None))
        f.write("itemsList: %r\n" % getattr(pkg, "itemsList", "NO_ITEMS_LIST"))
        f.write("itemList: %r\n" % getattr(pkg, "itemList", "NO_ITEM_LIST"))
        f.write("layoutInfo: %r\n" % getattr(pkg, "layoutInfo", "NO_LAYOUT"))
        f.write("_packageCapacity: %r\n" % getattr(pkg, "_packageCapacity", "NO_CAP"))
        f.write("packageCapacity: %r\n" % getattr(pkg, "packageCapacity", "NO_PCAP"))
    except Exception:
        f.write(traceback.format_exc())
