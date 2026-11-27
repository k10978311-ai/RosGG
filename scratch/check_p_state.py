f = open(OUT, "w")
try:
    import BigWorld, Globals
    p = BigWorld.player()
    f.write("p: %r\n" % (p,))
    if p:
        f.write("p.hallScene: %r\n" % (getattr(p, "hallScene", None),))
        f.write("p.readGMRedhintMsg: %r\n" % (getattr(p, "readGMRedhintMsg", "<none>"),))
        f.write("Globals.isHallSceneReady(): %r\n" % (getattr(Globals, "isHallSceneReady", lambda: None)(),))
        f.write("Globals.isInHall: %r\n" % (getattr(Globals, "isInHall", None),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
