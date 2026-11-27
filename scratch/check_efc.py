import sys
f = open(OUT, "w")
try:
    import Globals
    efc = getattr(Globals, "entityFlowControl", None)
    f.write("entityFlowControl: %r\n" % efc)
    if efc:
        for k in dir(efc):
            if not k.startswith("__"):
                try:
                    f.write("  efc.%s = %r\n" % (k, getattr(efc, k)))
                except Exception as ex:
                    f.write("  efc.%s = <err %r>\n" % (k, ex))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
