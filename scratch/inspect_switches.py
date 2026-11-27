OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete
    real_fn = Athlete.PlayerAthlete.enterHall.func_closure[0].cell_contents
    switches = real_fn.func_globals.get('switches')
    f.write("switches.__file__: %r\n" % getattr(switches, '__file__', None))
    f.write("switches dir: %r\n" % dir(switches))
    for k in sorted(dir(switches)):
        if not k.startswith('__'):
            f.write("  switches.%s: %r\n" % (k, getattr(switches, k)))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
