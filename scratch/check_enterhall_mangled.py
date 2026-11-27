f = open(OUT, "w")
try:
    import Athlete
    pcls = Athlete.PlayerAthlete
    
    for k in dir(pcls):
        if 'enterhall' in k.lower():
            f.write("method: %s -> %r\n" % (k, getattr(pcls, k)))
            fn = getattr(pcls, k)
            if hasattr(fn, 'im_func'):
                f.write("  co_names: %r\n" % (fn.im_func.func_code.co_names,))
                f.write("  co_consts: %r\n" % (fn.im_func.func_code.co_consts,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
