import sys, traceback
out = open(OUT, 'w')
try:
    import Athlete
    fn = Athlete.PlayerAthlete.showSelectCharacter
    if hasattr(fn, 'im_func'): fn = fn.im_func
    if fn.func_closure:
        for i, c in enumerate(fn.func_closure):
            obj = c.cell_contents
            out.write('closure %d: %r\n' % (i, obj))
            if hasattr(obj, 'func_code'):
                out.write('  co_names: %r\n' % (obj.func_code.co_names,))
                out.write('  co_varnames: %r\n' % (obj.func_code.co_varnames,))
                out.write('  co_consts: %r\n' % ([x for x in obj.func_code.co_consts if not hasattr(x, 'co_names')],))
except Exception:
    out.write(traceback.format_exc())
out.close()
