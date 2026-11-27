import sys, traceback, dis
out = open(OUT, 'w')
orig_stdout = sys.stdout
sys.stdout = out
try:
    import Athlete
    pa = Athlete.PlayerAthlete
    for name in ['showSelectCharacter', 'enterHall', 'onLogin']:
        fn = getattr(pa, name, None)
        if hasattr(fn, 'im_func'):
            fn = fn.im_func
        if hasattr(fn, 'func_closure') and fn.func_closure:
            for c in fn.func_closure:
                if hasattr(c.cell_contents, 'func_code'):
                    real = c.cell_contents
                    print('=== %s CLOSURE ===' % name)
                    dis.dis(real.func_code)
        elif hasattr(fn, 'func_code'):
            print('=== %s ===' % name)
            dis.dis(fn.func_code)
except Exception:
    traceback.print_exc()
finally:
    sys.stdout = orig_stdout
    out.close()
