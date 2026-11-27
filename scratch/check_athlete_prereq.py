with open(OUT, 'w') as f:
    import Athlete
    cls = Athlete.PlayerAthlete
    f.write("mro: %r\n" % ([c.__name__ for c in cls.__mro__]))
    f.write("prerequisites: %r\n" % (getattr(cls, 'prerequisites', None)))
    if hasattr(cls, 'prerequisites'):
        prereq = getattr(cls, 'prerequisites')
        if hasattr(prereq, 'func_code'):
            f.write("prereq code names: %r\n" % (prereq.func_code.co_names,))
            f.write("prereq consts: %r\n" % (prereq.func_code.co_consts,))
            f.write("prereq varnames: %r\n" % (prereq.func_code.co_varnames,))
            # disassemble opcode
            import opcode
            code = bytearray(prereq.func_code.co_code)
            i = 0
            lines = []
            while i < len(code):
                op = code[i]
                opname = opcode.opname[op] if op < len(opcode.opname) else str(op)
                i += 1
                arg = None
                if op >= opcode.HAVE_ARGUMENT:
                    arg = code[i] + (code[i+1] << 8)
                    i += 2
                lines.append((opname, arg))
            f.write("prereq ops: %r\n" % (lines,))
