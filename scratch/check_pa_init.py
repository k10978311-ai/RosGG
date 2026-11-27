f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/pa_init.txt', 'w')
try:
    import Athlete, dis, sys
    fn = getattr(Athlete.PlayerAthlete, '__init__', None)
    if hasattr(fn, 'im_func'): fn = fn.im_func
    f.write('PlayerAthlete.__init__: %r\n' % fn)
    if fn:
        f.write('co_names: %r\n' % (fn.func_code.co_names,))
        f.write('co_consts: %r\n' % (fn.func_code.co_consts,))
        orig = sys.stdout; sys.stdout = f; dis.dis(fn); sys.stdout = orig
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
