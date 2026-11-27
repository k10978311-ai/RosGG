OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete
    real_fn = Athlete.PlayerAthlete.enterHall.func_closure[0].cell_contents
    GameObject = real_fn.func_globals.get('GameObject')
    scene_go = GameObject.Find('Scene')
    ss = scene_go.GetComponent('SceneSystem')
    
    co = ss._preloadLevelResCoro.im_func.func_code
    f.write("_preloadLevelResCoro names: %r\n" % (co.co_names,))
    f.write("_preloadLevelResCoro consts: %r\n" % [c for c in co.co_consts if not hasattr(c, 'co_names')])
    f.write("_preloadLevelResCoro varnames: %r\n" % (co.co_varnames,))

    # Also check if ss is currently running any coroutines
    for cname in ('_preloadLevelResCoro', 'loadHallScene'):
        f.write("isCoroutineRunning(%s): %r\n" % (cname, ss.isCoroutineRunning(cname)))

    # Also check Globals.MAP_ID and PREV_MAP_ID
    import Globals
    f.write("Globals.MAP_ID: %r\n" % getattr(Globals, 'MAP_ID', 'NO_ATTR'))
    f.write("Globals.PREV_MAP_ID: %r\n" % getattr(Globals, 'PREV_MAP_ID', 'NO_ATTR'))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
