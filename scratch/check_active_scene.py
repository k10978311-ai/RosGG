f = open(OUT, "w")
try:
    from libclaudia import Application, GameObject
    import BigWorld, Globals
    p = BigWorld.player()
    f.write("BigWorld.player(): %r\n" % (p,))
    f.write("Application.scene: %r\n" % (Application.scene,))
    
    # Check Application methods/properties
    for a in dir(Application):
        if 'Level' in a or 'Scene' in a:
            try:
                v = getattr(Application, a)
                f.write("Application.%s: %r\n" % (a, v() if callable(v) else v))
            except Exception as e:
                f.write("Application.%s: <err %s>\n" % (a, e))

    s = GameObject.Find("Scene")
    if s:
        ss = s.GetComponent("SceneSystem")
        f.write("SceneSystem attributes:\n")
        for a in ['_current_scene_id', '_scene', '_scene_models', '_is_loading', '_coro', '_loading_callback']:
            f.write("  ss.%s: %r\n" % (a, getattr(ss, a, '<no>')))
            
    # Check UI
    uiMgr = getattr(Globals, "uiMgr", None)
    if uiMgr:
        f.write("uiMgr._loaded_ui: %r\n" % getattr(uiMgr, "_loaded_ui", None))
        f.write("uiMgr._visible_ui: %r\n" % getattr(uiMgr, "_visible_ui", None))

    # Check why UILoading is visible
    uiloading = uiMgr.get_ui('UILoading') if uiMgr else None
    f.write("UILoading: %r\n" % (uiloading,))
    if uiloading:
        for a in dir(uiloading):
            if not a.startswith('__') and not callable(getattr(uiloading, a)):
                f.write("  uiloading.%s: %r\n" % (a, getattr(uiloading, a)))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
