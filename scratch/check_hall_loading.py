f = open(OUT, "w")
try:
    import Athlete, Globals
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem") if scene else None
    
    f.write("Scene: %r\n" % (scene,))
    f.write("SceneSystem: %r\n" % (ss,))
    if ss:
        for attr in ["_scene", "_scene_stage", "_teleporting", "_teleportCallbacks"]:
            f.write("ss.%s: %r\n" % (attr, getattr(ss, attr, "<none>")))
        for cname in ["_preloadLevelResCoro", "loadHallScene", "DoLoadNeoxScene", "waitForTerrainReady"]:
            f.write("isCoroRunning(%s): %r\n" % (cname, ss.isCoroutineRunning(cname)))
            
    import Application as app
    f.write("app.scene: %r\n" % (getattr(app, "scene", None),))
    f.write("app.____current_level__: %r\n" % (getattr(app, "____current_level__", None),))
    f.write("app.____loaded_level__: %r\n" % (getattr(app, "____loaded_level__", None),))
    f.write("app.____next_level__: %r\n" % (getattr(app, "____next_level__", None),))
    f.write("app.____next_level_callback__: %r\n" % (getattr(app, "____next_level_callback__", None),))
    
    uiMgr = Globals.uiMgr
    loadingUi = uiMgr.get_ui("UILoading")
    f.write("loadingUi: %r\n" % (loadingUi,))
    if loadingUi:
        f.write("loadingUi.progress: %r\n" % (getattr(loadingUi, "progress", None),))
        f.write("loadingUi._progress: %r\n" % (getattr(loadingUi, "_progress", None),))
        f.write("loadingUi.is_enter: %r\n" % (getattr(loadingUi, "is_enter", None),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
