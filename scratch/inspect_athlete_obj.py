f = open(OUT, "w")
try:
    import BigWorld
    p = BigWorld.player()
    f.write("dir(p): %r\n" % ([a for a in dir(p) if not a.startswith("__")],))
    # Check specific attributes related to hall
    for attr in ["firstLoginToday", "isInHall", "hallScene", "inHall", "_enterHall", "isEnterHall", "cur_map_id", "spaceID"]:
        f.write("%s: %r\n" % (attr, getattr(p, attr, "<none>")))
    
    # Inspect enterHall code
    co = p.enterHall.func_code
    f.write("enterHall co_names: %r\n" % (co.co_names,))
    f.write("enterHall co_varnames: %r\n" % (co.co_varnames,))
    f.write("enterHall co_consts: %r\n" % ([c for c in co.co_consts if not hasattr(c, "co_names")],))
    
    # Check if _realEnterHall exists
    if hasattr(p, "_realEnterHall"):
        rco = p._realEnterHall.func_code
        f.write("_realEnterHall co_names: %r\n" % (rco.co_names,))
        f.write("_realEnterHall co_varnames: %r\n" % (rco.co_varnames,))
        f.write("_realEnterHall co_consts: %r\n" % ([c for c in rco.co_consts if not hasattr(c, "co_names")],))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
