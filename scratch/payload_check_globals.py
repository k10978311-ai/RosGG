import Globals
import traceback

with open(OUT, "w") as f:
    try:
        f.write("Globals dir:\n%r\n" % dir(Globals))
        for attr in ["ui", "ui_mgr", "scene", "cur_scene", "player"]:
            if hasattr(Globals, attr):
                f.write("Globals.%s = %r\n" % (attr, getattr(Globals, attr)))
    except Exception:
        f.write(traceback.format_exc())
