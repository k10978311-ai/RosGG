with open(OUT, 'w') as f:
    try:
        import Athlete
        raw = Athlete.PlayerAthlete.__dict__['enterHall']
        inner = raw.func_closure[0].cell_contents
        reh = [c for c in inner.func_code.co_consts if hasattr(c, 'co_name') and c.co_name == '_realEnterHall'][0]
        code = bytearray(reh.co_code)
        ret_offsets = [i for i, b in enumerate(code) if b == 74]
        f.write('ret_offsets: ' + repr(ret_offsets) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
