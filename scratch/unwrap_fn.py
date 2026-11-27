f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import Athlete
    fn = Athlete.PlayerAthlete.showSelectCharacter
    f.write('fn: %r\n' % fn)
    if hasattr(fn, 'im_func'):
        fn = fn.im_func
    if fn.func_closure:
        f.write('closures: %d\n' % len(fn.func_closure))
        for i, c in enumerate(fn.func_closure):
            f.write('  [%d] cell_contents: %r\n' % (i, c.cell_contents))
            if hasattr(c.cell_contents, 'func_code'):
                real_fn = c.cell_contents
                f.write('  REAL FN co_names: %r\n' % (real_fn.func_code.co_names,))
                f.write('  REAL FN co_consts: %r\n' % ([x for x in real_fn.func_code.co_consts if not hasattr(x, 'co_names')],))
                f.write('  REAL FN co_varnames: %r\n' % (real_fn.func_code.co_varnames,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
