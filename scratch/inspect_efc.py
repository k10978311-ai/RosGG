f = open(OUT, "w")
try:
    import Globals, dis
    efc = getattr(Globals, "entityFlowControl", None)
    if efc:
        cls = type(efc)
        for name in ('Update', 'appendEntity', 'popEntity'):
            fn = getattr(cls, name, None)
            if fn:
                co = fn.im_func.func_code if hasattr(fn, 'im_func') else fn.func_code
                f.write("=== %s ===\n" % name)
                f.write("co_names: %r\n" % (co.co_names,))
                f.write("co_consts: %r\n" % (co.co_consts,))
                bc = bytearray(co.co_code)
                for i in range(0, min(len(bc), 60), 3):
                    f.write("%d: op=%d\n" % (i, bc[i]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
