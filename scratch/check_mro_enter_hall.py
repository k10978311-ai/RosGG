OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete
    cls = Athlete.PlayerAthlete
    f.write("MRO: %r\n" % ([c.__name__ for c in cls.__mro__],))
    for c in cls.__mro__:
        if 'enterHall' in c.__dict__:
            f.write("enterHall in %s: %r\n" % (c.__name__, c.__dict__['enterHall']))
            
    # Also check globals of real_fn
    fn = cls.enterHall
    real_fn = fn.func_closure[0].cell_contents
    f.write("real_fn globals switches: %r\n" % real_fn.func_globals.get('switches'))
    f.write("real_fn globals safesuper: %r\n" % real_fn.func_globals.get('safesuper'))
    f.write("real_fn globals ros2_common: %r\n" % real_fn.func_globals.get('ros2_common'))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
