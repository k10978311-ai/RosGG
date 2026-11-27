OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Athlete
    cls = Athlete.PlayerAthlete
    
    for m in ('onSetSwitches', 'onSyncSwitches'):
        fn = getattr(cls, m, None)
        f.write("%s: %r\n" % (m, fn))
        if fn:
            co = getattr(fn, 'func_code', None)
            if co:
                f.write("  names: %r\n" % (co.co_names,))
                f.write("  consts: %r\n" % (co.co_consts,))
                f.write("  varnames: %r\n" % (co.co_varnames,))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
