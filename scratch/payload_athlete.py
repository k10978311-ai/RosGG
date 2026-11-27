import traceback
out = open(OUT, 'w')
try:
    import Athlete
    pa = Athlete.PlayerAthlete
    out.write('Athlete attributes:\n')
    for name in ['showSelectCharacter', 'createCharacter', 'enterHall', '_realEnterHall', 'onLogin', 'onRoleCreateSuc', 'onGetGMTable']:
        fn = getattr(pa, name, None)
        out.write('%s: %r\n' % (name, fn))
        if hasattr(fn, 'im_func'):
            fn = fn.im_func
        if hasattr(fn, 'func_closure') and fn.func_closure:
            for c in fn.func_closure:
                if hasattr(c.cell_contents, 'func_code'):
                    real = c.cell_contents
                    out.write('  closure %s:\n' % getattr(real, '__name__', 'unnamed'))
                    out.write('    co_names: %r\n' % (real.func_code.co_names,))
                    out.write('    co_varnames: %r\n' % (real.func_code.co_varnames,))
                    out.write('    co_consts: %r\n' % ([x for x in real.func_code.co_consts if not hasattr(x, 'co_names')],))
        elif hasattr(fn, 'func_code'):
            co = fn.func_code
            out.write('  co_names: %r\n' % (co.co_names,))
            out.write('  co_varnames: %r\n' % (co.co_varnames,))
            out.write('  co_consts: %r\n' % ([x for x in co.co_consts if not hasattr(x, 'co_names')],))
except Exception:
    out.write(traceback.format_exc())
out.close()
