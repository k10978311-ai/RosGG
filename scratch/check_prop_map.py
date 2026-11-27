f = open(OUT, "w")
try:
    import maps_utils, const
    prop = getattr(maps_utils, "properties", None)
    f.write("maps_utils.properties: %r\n" % (prop,))
    if prop:
        fn = getattr(prop, "getMapData", None)
        f.write("properties.getMapData: %r\n" % (fn,))
        if fn:
            f.write("getMapData(20): %r\n" % (fn(20),))
            f.write("getMapData(const.HALL_MAP_ID): %r\n" % (fn(const.HALL_MAP_ID),))
            md = fn(const.HALL_MAP_ID)
            if md:
                f.write("md attributes: %r\n" % ([a for a in dir(md) if not a.startswith("__")],))
                f.write("md.RESOURCE_PATH: %r\n" % (getattr(md, "RESOURCE_PATH", None),))
                f.write("md.SCENE_NAME: %r\n" % (getattr(md, "SCENE_NAME", None),))
                f.write("getScenePath(md): %r\n" % (maps_utils.getScenePath(md),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
