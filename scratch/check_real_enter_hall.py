f = open(OUT, "w")
try:
    import Athlete
    f.write("Athlete.GameObject: %r\n" % (getattr(Athlete, "GameObject", None),))
    go = getattr(Athlete, "GameObject", None)
    if go:
        scene = go.Find("Scene")
        f.write("go.Find('Scene'): %r\n" % (scene,))
        if scene:
            ss = scene.GetComponent("SceneSystem")
            f.write("ss: %r\n" % (ss,))
            if ss:
                f.write("ss attributes: %r\n" % ([a for a in dir(ss) if not a.startswith("__")],))
                f.write("ss.isLevelResReady: %r\n" % (getattr(ss, "isLevelResReady", None),))
                f.write("ss.isLoading: %r\n" % (getattr(ss, "isLoading", None),))
                f.write("ss.curMapID: %r\n" % (getattr(ss, "curMapID", None),))
    
    # Check Globals
    import Globals
    f.write("Globals.rookieEnterHall: %r\n" % (getattr(Globals, "rookieEnterHall", "<none>"),))
    f.write("Globals.FIRST_LOAD: %r\n" % (getattr(Globals, "FIRST_LOAD", "<none>"),))
    f.write("Globals.hasLogonServer: %r\n" % (getattr(Globals, "hasLogonServer", "<none>"),))
    
    # Check BigWorld.player()
    import BigWorld
    p = BigWorld.player()
    f.write("p: %r\n" % (p,))
    if p:
        f.write("p.readGMRedhintMsg: %r\n" % (getattr(p, "readGMRedhintMsg", "<none>"),))
        f.write("p.accessRecordTimerID: %r\n" % (getattr(p, "accessRecordTimerID", "<none>"),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
