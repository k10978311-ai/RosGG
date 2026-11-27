f = open(OUT, "w")
try:
    import BigWorld, Globals
    from libclaudia.Classes.Application import Application as app
    p = BigWorld.player()
    f.write("player: %r\n" % (p,))
    if p:
        for attr in ['hallScene', 'hallSceneReady', 'is_in_hall', 'isInHall', 'm_bEnterHall', 'm_isEnterHall']:
            f.write("p.%s: %r\n" % (attr, getattr(p, attr, '<no>')))
    
    # Check GameObject "Scene"
    import GameObject
    scene_go = GameObject.Find("Scene")
    f.write("Scene GameObject: %r\n" % (scene_go,))
    if scene_go:
        ss = scene_go.GetComponent("SceneSystem")
        f.write("SceneSystem: %r\n" % (ss,))
        if ss:
            for attr in dir(ss):
                if not attr.startswith('__'):
                    try:
                        v = getattr(ss, attr)
                        if not callable(v):
                            f.write("  ss.%s = %r\n" % (attr, v))
                    except Exception as e:
                        pass

    # Check uiMgr for all open UIs
    uiMgr = getattr(Globals, "uiMgr", None)
    if uiMgr:
        f.write("uiMgr: %r\n" % (uiMgr,))
        for attr in dir(uiMgr):
            if 'ui' in attr.lower():
                try:
                    f.write("uiMgr.%s = %r\n" % (attr, getattr(uiMgr, attr)))
                except:
                    pass
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
