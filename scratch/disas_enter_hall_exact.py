
import sys, StringIO, dis
with open(OUT, 'w') as f:
    try:
        import entities.Athlete as ath
        fn = ath.PlayerAthlete.enterHall
        co = fn.im_func.func_code if hasattr(fn, 'im_func') else fn.func_code
        f.write('enterHall co_names: ' + repr(co.co_names) + '\n')
        f.write('enterHall co_consts: ' + repr(co.co_consts) + '\n')
        f.write('enterHall co_varnames: ' + repr(co.co_varnames) + '\n')
        sio = StringIO.StringIO()
        old_out = sys.stdout
        sys.stdout = sio
        dis.dis(co)
        sys.stdout = old_out
        f.write('enterHall disassembly:\n' + sio.getvalue() + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
