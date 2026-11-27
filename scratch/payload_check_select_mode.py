import Globals
import traceback

with open(OUT, "w") as f:
    try:
        f.write("enterSelectModeFinished: %r\n" % getattr(Globals, "enterSelectModeFinished", "NOT_SET"))
        f.write("rookieEnterHall: %r\n" % getattr(Globals, "rookieEnterHall", "NOT_SET"))
        f.write("firstLoginInGame: %r\n" % getattr(Globals, "firstLoginInGame", "NOT_SET"))
        f.write("enterFirstFlag: %r\n" % getattr(Globals, "enterFirstFlag", "NOT_SET"))
    except Exception:
        f.write(traceback.format_exc())
