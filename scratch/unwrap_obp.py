f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/obp_unwrap.txt", "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.onBecomePlayer
    if hasattr(fn, 'im_func'): fn = fn.im_func
    for c in fn.func_closure or []:
        if hasattr(c.cell_contents, 'func_code'):
            real_fn = c.cell_contents
            f.write("real onBecomePlayer co_names: %r\n" % (real_fn.func_code.co_names,))
            f.write("real onBecomePlayer co_consts: %r\n" % ([x for x in real_fn.func_code.co_consts if not hasattr(x, 'co_names')],))
            f.write("real onBecomePlayer co_varnames: %r\n" % (real_fn.func_code.co_varnames,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
