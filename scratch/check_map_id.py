f = open(OUT, "w")
try:
    import Globals, Athlete
    f.write("Globals.MAP_ID: %r\n" % (getattr(Globals, "MAP_ID", "<none>"),))
    f.write("Globals.PREV_MAP_ID: %r\n" % (getattr(Globals, "PREV_MAP_ID", "<none>"),))
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem") if scene else None
    if ss:
        f.write("ss.curMapID: %r\n" % (getattr(ss, "curMapID", "<none>"),))
        f.write("ss.isLevelResReady: %r\n" % (getattr(ss, "isLevelResReady", "<none>"),))
        f.write("ss.isLoading: %r\n" % (getattr(ss, "isLoading", "<none>"),))
        f.write("ss.mapID: %r\n" % (getattr(ss, "mapID", "<none>"),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
