with open(OUT, 'w') as f:
    try:
        import Athlete, dis, StringIO, sys
        fn = Athlete.PlayerAthlete.enterHall
        real_fn = fn.func_closure[0].cell_contents
        co = real_fn.func_code
        f.write('real_fn co_names: ' + repr(co.co_names) + '\n')
        f.write('real_fn co_consts: ' + repr([c.co_name if hasattr(c, 'co_name') else repr(c) for c in co.co_consts]) + '\n')
        f.write('real_fn co_varnames: ' + repr(co.co_varnames) + '\n')
        sio = StringIO.StringIO()
        old_out = sys.stdout
        sys.stdout = sio
        dis.dis(co)
        sys.stdout = old_out
        f.write('disassembly:\n' + sio.getvalue() + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
