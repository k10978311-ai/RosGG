f = open(OUT, "w")
try:
    import Athlete, Globals
    from libclaudia.Classes.Application import Application as app
    
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
        f.write("loadingUi.is_visible: %r\n" % (getattr(loadingUi, "isVisible", lambda: "<none>")(),))
    
    import BigWorld
    p = BigWorld.player()
    f.write("p: %r\n" % (p,))
    if p:
        f.write("p.hallScene: %r\n" % (getattr(p, "hallScene", None),))
        f.write("isHallSceneReady: %r\n" % (getattr(Globals, "isHallSceneReady", lambda: None)(),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
