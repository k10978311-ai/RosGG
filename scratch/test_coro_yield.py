f = open(OUT, "w")
try:
    import Athlete, const
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem")
    
    # Let's inspect what _preloadLevelResCoro creates
    coro = ss._preloadLevelResCoro(const.HALL_MAP_ID, None)
    f.write("coro: %r\n" % (coro,))
    f.write("dir(coro): %r\n" % ([a for a in dir(coro) if not a.startswith("__")],))
    f.write("gi_frame: %r\n" % (getattr(coro, "gi_frame", None),))
    f.write("gi_code: %r\n" % (getattr(coro, "gi_code", None),))
    if hasattr(coro, "gi_code"):
        co = coro.gi_code
        f.write("gi_code.co_names: %r\n" % (co.co_names,))
        f.write("gi_code.co_varnames: %r\n" % (co.co_varnames,))
        f.write("gi_code.co_consts: %r\n" % ([c for c in co.co_consts if not hasattr(c, "co_names")],))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
