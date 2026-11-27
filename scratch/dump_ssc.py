OUT = '/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log'
f = open(OUT, 'w')
try:
    import Athlete
    fn = Athlete.PlayerAthlete.showSelectCharacter
    real_fn = fn.func_closure[0].cell_contents if fn.func_closure else fn
    co = real_fn.func_code
    f.write('names: %r\n' % (co.co_names,))
    f.write('consts: %r\n' % [c if not hasattr(c, 'co_name') else c.co_name for c in co.co_consts])
    f.write('varnames: %r\n' % (co.co_varnames,))
    code = bytearray(co.co_code)
    i = 0
    while i < len(code):
        offset = i
        op = code[i]
        i += 1
        arg_str = ''
        if op >= 90:
            arg = code[i] | (code[i+1] << 8)
            i += 2
            arg_str = '%d' % arg
            if op in (101, 116, 96, 155, 156):
                if arg < len(co.co_names): arg_str += ' (name: %s)' % co.co_names[arg]
            elif op == 100:
                if arg < len(co.co_consts): arg_str += ' (const: %r)' % (co.co_consts[arg],)
        f.write('%4d: op=%d %s\n' % (offset, op, arg_str))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
