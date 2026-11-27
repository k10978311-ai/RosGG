import sys
f = open(OUT, "w")
try:
    import Globals
    efc = getattr(Globals, "entityFlowControl", None)
    if efc:
        cls = type(efc)
        for name in ('Update', 'appendEntity', 'popEntity', 'Init', 'Start'):
            fn = getattr(cls, name, None)
            if fn and hasattr(fn, 'func_code'):
                co = fn.func_code
                f.write("%s names: %r\n" % (name, co.co_names))
                f.write("%s consts: %r\n" % (name, [c for c in co.co_consts if not hasattr(c, 'co_names')]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
