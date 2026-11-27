import sys, types
f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.__dict__.get("onCreate")
    f.write("PlayerAthlete.onCreate: %r\n" % fn)
    if fn:
        if hasattr(fn, "func_code"):
            co = fn.func_code
            f.write("onCreate names: %r\n" % (co.co_names,))
            f.write("onCreate consts: %r\n" % ([c for c in co.co_consts if not hasattr(c, "co_names")],))
    import Globals
    f.write("Globals.curLoginHostID: %r\n" % getattr(Globals, "curLoginHostID", "<missing>"))
    f.write("Globals.player: %r\n" % getattr(Globals, "player", "<missing>"))
    f.write("Globals.isInHall: %r\n" % getattr(Globals, "isInHall", "<missing>"))
    f.write("Globals.hallSceneReady: %r\n" % getattr(Globals, "hallSceneReady", "<missing>"))
    f.write("Globals.enterSelectModeFinished: %r\n" % getattr(Globals, "enterSelectModeFinished", "<missing>"))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
