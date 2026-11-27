OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import BigWorld, Globals
    f.write("BigWorld.player(): %s\n" % repr(BigWorld.player()))
    f.write("BigWorld.entities: %s\n" % repr(list(BigWorld.entities.keys())))
    for eid, e in BigWorld.entities.items():
        f.write("  e %s: %s (%s)\n" % (eid, e, e.__class__.__name__))
    f.write("Globals.player: %s\n" % repr(Globals.player))
    f.write("Globals.cur_scene: %s\n" % repr(getattr(Globals, 'cur_scene', None)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
