
import sys
with open(OUT, 'w') as f:
    try:
        import entities.Athlete as ath
        import dis, StringIO
        for name in ['onSyncSwitches', 'onSetSwitches']:
            fn = getattr(ath.PlayerAthlete, name, None)
            f.write('=== ' + name + ' ===\n')
            if fn:
                co = fn.im_func.func_code if hasattr(fn, 'im_func') else fn.func_code
                f.write('names: ' + repr(co.co_names) + '\n')
                f.write('consts: ' + repr(co.co_consts) + '\n')
                f.write('varnames: ' + repr(co.co_varnames) + '\n')
                sio = StringIO.StringIO()
                old_out = sys.stdout
                sys.stdout = sio
                dis.dis(co)
                sys.stdout = old_out
                f.write(sio.getvalue() + '\n')
            else:
                f.write('NOT FOUND on PlayerAthlete\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
