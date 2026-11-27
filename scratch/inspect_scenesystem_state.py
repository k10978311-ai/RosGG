OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete
    real_fn = Athlete.PlayerAthlete.enterHall.func_closure[0].cell_contents
    GameObject = real_fn.func_globals.get('GameObject')
    scene_go = GameObject.Find('Scene')
    ss = scene_go.GetComponent('SceneSystem')
    
    f.write("ss._scene: %r\n" % getattr(ss, '_scene', 'NO_ATTR'))
    f.write("ss._scene_stage: %r\n" % getattr(ss, '_scene_stage', 'NO_ATTR'))
    f.write("ss.scene_main: %r\n" % getattr(ss, 'scene_main', 'NO_ATTR'))
    f.write("ss._SceneSystem____loading_callback: %r\n" % getattr(ss, '_SceneSystem____loading_callback', 'NO_ATTR'))
    f.write("ss._preloadLevelResCoro: %r\n" % getattr(ss, '_preloadLevelResCoro', 'NO_ATTR'))
    
    # Check coroutines on scene_go
    f.write("ss.isCoroutineRunning: %r\n" % getattr(ss, 'isCoroutineRunning', 'NO_ATTR'))
    
    # Inspect loadHallScene code!
    lhs = ss.loadHallScene
    f.write("lhs: %r\n" % lhs)
    if hasattr(lhs, 'func_code'):
        co = lhs.func_code
        f.write("lhs names: %r\n" % (co.co_names,))
        f.write("lhs consts: %r\n" % (co.co_consts,))
        f.write("lhs varnames: %r\n" % (co.co_varnames,))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
