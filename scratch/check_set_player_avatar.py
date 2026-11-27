f = open(OUT, "w")
try:
    import Globals
    fn = Globals.setPlayerAvatar
    co = fn.func_code
    f.write("setPlayerAvatar names: %r\n" % (co.co_names,))
    f.write("setPlayerAvatar consts: %r\n" % (co.co_consts,))
    f.write("setPlayerAvatar varnames: %r\n" % (co.co_varnames,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
