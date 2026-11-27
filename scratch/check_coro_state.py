f = open(OUT, "w")
try:
    import Athlete
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem")
    
    f.write("ss.isCoroutineRunning('_preloadLevelResCoro'): %r\n" % (ss.isCoroutineRunning("_preloadLevelResCoro"),))
    f.write("ss.isCoroutineRunning('loadHallScene'): %r\n" % (ss.isCoroutineRunning("loadHallScene"),))
    
    import Application
    f.write("Application.is_loading(): %r\n" % (getattr(Application, "is_loading", lambda: "<none>")(),))
    f.write("Application.get_loading_progress(): %r\n" % (getattr(Application, "get_loading_progress", lambda: "<none>")(),))
    
    # Check what UILoading has
    import Globals
    uiMgr = Globals.uiMgr
    loadingUi = uiMgr.get_ui("UILoading")
    f.write("loadingUi: %r\n" % (loadingUi,))
    if loadingUi:
        f.write("loadingUi.progress: %r\n" % (getattr(loadingUi, "progress", None),))
        f.write("loadingUi._progress: %r\n" % (getattr(loadingUi, "_progress", None),))
        f.write("loadingUi attrs: %r\n" % ([a for a in dir(loadingUi) if not a.startswith("__")],))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
