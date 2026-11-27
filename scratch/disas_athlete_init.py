f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/dis_init.txt', 'w')
try:
    import Athlete
    fn = Athlete.Athlete.__init__
    if hasattr(fn, 'im_func'): fn = fn.im_func
    f.write('Athlete.__init__ co_names: %r\n' % (fn.func_code.co_names,))
    f.write('Athlete.__init__ co_consts: %r\n' % ([x for x in fn.func_code.co_consts if not hasattr(x, 'co_names')],))
    fn2 = Athlete.PlayerAthlete.__init__
    if hasattr(fn2, 'im_func'): fn2 = fn2.im_func
    f.write('PlayerAthlete.__init__ co_names: %r\n' % (fn2.func_code.co_names,))
    f.write('PlayerAthlete.__init__ co_consts: %r\n' % ([x for x in fn2.func_code.co_consts if not hasattr(x, 'co_names')],))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
