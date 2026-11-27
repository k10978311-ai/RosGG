f = open(OUT, "w")
try:
    import BigWorld, Globals, world
    p = BigWorld.player()
    f.write("BigWorld.player(): %r (class=%s)\n" % (p, p.__class__.__name__ if p else None))
    if p:
        f.write("  id: %d\n" % p.id)
        f.write("  hallScene: %r\n" % getattr(p, "hallScene", None))
    
    f.write("Globals.isInHall: %r\n" % getattr(Globals, "isInHall", None))
    f.write("Globals.isHallSceneReady: %r\n" % (getattr(Globals, "isHallSceneReady", lambda: None)()))
    f.write("Globals.enterSelectModeFinished: %r\n" % getattr(Globals, "enterSelectModeFinished", None))
    f.write("Globals.enterFirstFlag: %r\n" % getattr(Globals, "enterFirstFlag", None))
    
    try:
        from libclaudia import GameObject, Application
        f.write("Application.scene: %r\n" % getattr(Application, "scene", None))
        s = GameObject.Find("Scene")
        f.write("GameObject.Find('Scene'): %r\n" % (s,))
        if s:
            ss = s.GetComponent("SceneSystem")
            f.write("SceneSystem: %r\n" % (ss,))
            if ss:
                for a in dir(ss):
                    if not a.startswith('__'):
                        try:
                            f.write("  ss.%s: %r\n" % (a, getattr(ss, a)))
                        except Exception as e:
                            f.write("  ss.%s: <err %s>\n" % (a, e))
    except Exception as e:
        import traceback
        f.write("libclaudia error: %s\n%s\n" % (e, traceback.format_exc()))

    try:
        f.write("world.get_active_scene(): %r\n" % (world.get_active_scene(),))
    except Exception as e:
        f.write("world err: %s\n" % (e,))

    ui = getattr(Globals, "uiMgr", None)
    if ui:
        f.write("uiMgr: %r\n" % (ui,))
        for attr in ['_loaded_ui', '_visible_ui', 'all_ui', '_ui_dict', '_active_ui']:
            if hasattr(ui, attr):
                f.write("  ui.%s: %r\n" % (attr, getattr(ui, attr)))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
