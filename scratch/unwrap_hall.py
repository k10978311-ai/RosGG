f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import Athlete
    fn = Athlete.PlayerAthlete.enterHall
    if hasattr(fn, 'im_func'):
        fn = fn.im_func
    if fn.func_closure:
        for i, c in enumerate(fn.func_closure):
            if hasattr(c.cell_contents, 'func_code'):
                real_fn = c.cell_contents
                f.write('enterHall REAL FN co_names: %r\n' % (real_fn.func_code.co_names,))
                f.write('enterHall REAL FN co_consts: %r\n' % ([x for x in real_fn.func_code.co_consts if not hasattr(x, 'co_names')],))
                f.write('enterHall REAL FN co_varnames: %r\n' % (real_fn.func_code.co_varnames,))
    fn2 = getattr(Athlete.PlayerAthlete, '_realEnterHall', None)
    if fn2:
        if hasattr(fn2, 'im_func'):
            fn2 = fn2.im_func
        if fn2.func_closure:
            for i, c in enumerate(fn2.func_closure):
                if hasattr(c.cell_contents, 'func_code'):
                    real_fn = c.cell_contents
                    f.write('_realEnterHall REAL FN co_names: %r\n' % (real_fn.func_code.co_names,))
                    f.write('_realEnterHall REAL FN co_consts: %r\n' % ([x for x in real_fn.func_code.co_consts if not hasattr(x, 'co_names')],))
                    f.write('_realEnterHall REAL FN co_varnames: %r\n' % (real_fn.func_code.co_varnames,))
        else:
            f.write('_realEnterHall co_names: %r\n' % (fn2.func_code.co_names,))
            f.write('_realEnterHall co_consts: %r\n' % ([x for x in fn2.func_code.co_consts if not hasattr(x, 'co_names')],))
            f.write('_realEnterHall co_varnames: %r\n' % (fn2.func_code.co_varnames,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
