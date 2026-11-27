OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete, dis
    fn = Athlete.PlayerAthlete.enterHall
    code = fn.im_func.func_code if hasattr(fn, 'im_func') else fn.func_code
    f.write("enterHall co_names: %s\n" % str(code.co_names))
    f.write("enterHall co_consts: %s\n" % str(code.co_consts))
    f.write("enterHall co_varnames: %s\n" % str(code.co_varnames))
    
    # Also check current Globals.player
    import Globals
    f.write("Globals.player: %s\n" % repr(Globals.player))
    if Globals.player:
        f.write("Globals.player type: %s, class: %s\n" % (type(Globals.player), Globals.player.__class__.__name__))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
