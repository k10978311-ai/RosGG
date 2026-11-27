with open(OUT, 'w') as f:
    import Athlete
    fn = Athlete.PlayerAthlete._realEnterHall
    import types
    def find_code(c, target):
        if c.co_name == target:
            return c
        for const in c.co_consts:
            if hasattr(const, 'co_name'):
                res = find_code(const, target)
                if res: return res
        return None

    co = find_code(fn.im_func.func_code if hasattr(fn, 'im_func') else fn.func_code, 'onHallSceneReady')
    if co:
        f.write("found onHallSceneReady!\n")
        f.write("names: %r\n" % (co.co_names,))
        f.write("consts: %r\n" % (co.co_consts,))
        f.write("varnames: %r\n" % (co.co_varnames,))
        code = bytearray(co.co_code)
        for i in range(0, len(code), 3 if code[0] >= 90 else 1):
            pass
        f.write("code len: %d\n" % len(code))
        import dis
        f.write("disassembly:\n")
        # dump opcodes
        i = 0
        while i < len(code):
            offset = i
            op = code[i]
            i += 1
            arg_str = ''
            if op >= 90:
                arg = code[i] | (code[i+1] << 8)
                i += 2
                arg_str = str(arg)
                if arg < len(co.co_names): arg_str += ' (n: ' + str(co.co_names[arg]) + ')'
                if arg < len(co.co_consts): arg_str += ' (c: ' + repr(co.co_consts[arg]) + ')'
                if arg < len(co.co_varnames): arg_str += ' (v: ' + str(co.co_varnames[arg]) + ')'
            f.write('%4d: op=%3d %s\n' % (offset, op, arg_str))
    else:
        f.write("onHallSceneReady not found\n")
