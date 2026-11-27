import traceback, opcode
f = open(OUT, 'w')
try:
    import GameInit
    fn = GameInit.updateInactivityTimeout
    co = fn.func_code
    code = bytearray(co.co_code)
    i = 0
    while i < len(code):
        offset = i
        op = code[i]
        i += 1
        arg_val = None
        if op >= opcode.HAVE_ARGUMENT:
            arg = code[i] | (code[i+1] << 8)
            i += 2
            arg_val = arg
        f.write('%4d %s (%d) %r\n' % (offset, opcode.opname[op], op, arg_val))
    f.write('co_names: %r\n' % (co.co_names,))
    f.write('co_consts: %r\n' % (co.co_consts,))
except Exception:
    f.write(traceback.format_exc())
f.close()
