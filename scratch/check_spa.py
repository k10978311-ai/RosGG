OUT = '/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log'
f = open(OUT, 'w')
try:
    import Globals
    fn = getattr(Globals, 'setPlayerAvatar', None)
    if fn:
        co = fn.func_code
        f.write('setPlayerAvatar names: %r\n' % (co.co_names,))
        f.write('setPlayerAvatar consts: %r\n' % (co.co_consts,))
        f.write('setPlayerAvatar varnames: %r\n' % (co.co_varnames,))
    else:
        f.write('setPlayerAvatar NOT FOUND in Globals\n')
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
