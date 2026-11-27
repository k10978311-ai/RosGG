f = open(OUT, "w")
try:
    import BigWorld, Globals, Athlete
    p = BigWorld.player()
    f.write("BigWorld.player(): %r\n" % (p,))
    if p:
        f.write("p.mapID: %r\n" % getattr(p, 'mapID', '<none>'))
        f.write("p.loginScene: %r\n" % getattr(p, 'loginScene', '<none>'))
        if hasattr(p, 'loginScene'):
            ls = p.loginScene
            for attr in dir(ls):
                if not attr.startswith('__'):
                    try:
                        f.write("  ls.%s: %r\n" % (attr, getattr(ls, attr)))
                    except:
                        pass
        f.write("p.m_bEnterHall: %r\n" % getattr(p, 'm_bEnterHall', '<none>'))
        f.write("p.m_isEnterHall: %r\n" % getattr(p, 'm_isEnterHall', '<none>'))
        f.write("p.isInHall: %r\n" % getattr(p, 'isInHall', '<none>'))
        f.write("p.baseNickname: %r\n" % getattr(p, 'baseNickname', '<none>'))
    
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem") if scene else None
    f.write("Scene: %r\n" % (scene,))
    f.write("SceneSystem: %r\n" % (ss,))
    if ss:
        for attr in dir(ss):
            if not attr.startswith('__') and not callable(getattr(ss, attr)):
                try:
                    f.write("  ss.%s: %r\n" % (attr, getattr(ss, attr)))
                except:
                    pass
        for cname in ["_preloadLevelResCoro", "loadHallScene", "DoLoadNeoxScene", "waitForTerrainReady"]:
            try:
                f.write("isCoroRunning(%s): %r\n" % (cname, ss.isCoroutineRunning(cname)))
            except:
                pass

    uiMgr = Globals.uiMgr
    all_ui = getattr(uiMgr, '____all_ui__', getattr(uiMgr, '_UIMgr____all_ui__', {}))
    f.write("all_ui keys: %r\n" % (list(all_ui.keys()),))
    loading = all_ui.get('UILoading')
    if loading:
        for attr in dir(loading):
            if not attr.startswith('__') and not callable(getattr(loading, attr)):
                try:
                    f.write("  loading.%s: %r\n" % (attr, getattr(loading, attr)))
                except:
                    pass
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
