f = open(OUT, "w")
try:
    import maps_utils
    f.write("maps_utils dir: %r\n" % ([a for a in dir(maps_utils) if not a.startswith("__")],))
    # Check maps dict / data
    for attr in ["MAPS", "maps", "MAP_DATA", "mapData", "map_data_dict", "_maps"]:
        f.write("%s: %r\n" % (attr, getattr(maps_utils, attr, "<none>")))
    
    # Inspect getMapData code
    fn = getattr(maps_utils, "getMapData", None)
    if fn:
        co = fn.func_code
        f.write("getMapData names: %r\n" % (co.co_names,))
        f.write("getMapData consts: %r\n" % ([c for c in co.co_consts if not hasattr(c, "co_names")],))
        f.write("getMapData varnames: %r\n" % (co.co_varnames,))
    
    # Inspect getScenePath code
    sfn = getattr(maps_utils, "getScenePath", None)
    if sfn:
        co = sfn.func_code
        f.write("getScenePath names: %r\n" % (co.co_names,))
        f.write("getScenePath consts: %r\n" % ([c for c in co.co_consts if not hasattr(c, "co_names")],))
        f.write("getScenePath varnames: %r\n" % (co.co_varnames,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
