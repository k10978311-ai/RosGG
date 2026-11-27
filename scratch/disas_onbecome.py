f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import Athlete, dis, sys, StringIO
    func = Athlete.PlayerAthlete.onBecomePlayer.im_func
    f.write('co_names: %r\n' % (func.func_code.co_names,))
    f.write('co_consts: %r\n' % ([c for c in func.func_code.co_consts if not hasattr(c, 'co_names')],))
    old_stdout = sys.stdout
    sys.stdout = s = StringIO.StringIO()
    dis.dis(func)
    sys.stdout = old_stdout
    f.write('dis:\n' + s.getvalue())
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
