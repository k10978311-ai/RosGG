f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import Athlete
    func = Athlete.PlayerAthlete.showSelectCharacter.im_func
    f.write('co_names: %r\n' % (func.func_code.co_names,))
    f.write('co_consts: %r\n' % ([c for c in func.func_code.co_consts if not hasattr(c, 'co_names')],))
    f.write('co_varnames: %r\n' % (func.func_code.co_varnames,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
