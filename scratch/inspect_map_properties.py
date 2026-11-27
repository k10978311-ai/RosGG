f = open(OUT, "w")
try:
    import maps_utils
    # Let's inspect getMapData's globals / closures
    fn = maps_utils.getMapData
    f.write("fn: %r\n" % (fn,))
    f.write("closure: %r\n" % ([getattr(c, "cell_contents", None) for c in (fn.func_closure or [])],))
    
    # Check properties in maps_utils
    p = getattr(maps_utils, "properties", None)
    f.write("properties: %r\n" % (p,))
    if p:
        f.write("dir(properties): %r\n" % ([a for a in dir(p) if not a.startswith("__")],))
    
    # Let's see what maps_utils.properties has
    import sys
    for modname in sys.modules:
        if "map" in modname.lower() or "level" in modname.lower():
            f.write("mod: %s\n" % modname)
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
