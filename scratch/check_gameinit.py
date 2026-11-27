OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.enterHall
    real_fn = fn.func_closure[0].cell_contents
    fg = real_fn.func_globals
    
    gi = fg.get('GameInit')
    f.write("GameInit in globals: %r\n" % gi)
    if gi:
        f.write("dir(GameInit): %r\n" % dir(gi))
        f.write("hasattr updateInactivityTimeout: %r\n" % hasattr(gi, 'updateInactivityTimeout'))
        if hasattr(gi, 'updateInactivityTimeout'):
            try:
                gi.updateInactivityTimeout()
                f.write("gi.updateInactivityTimeout(): OK\n")
            except Exception as e:
                f.write("gi.updateInactivityTimeout() FAILED: %r\n" % e)
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
