with open(OUT, 'w') as f:
    import ui.UISkipTutorial as ST
    cls = getattr(ST, 'UISkipTutorial', None)
    m = getattr(cls, 'tryLeaveMap', None)
    for c in m.func_code.co_consts:
        if hasattr(c, 'co_name') and c.co_name == 'yes_callback':
            f.write("yes_callback names: %r\n" % (c.co_names,))
            f.write("yes_callback consts: %r\n" % (c.co_consts,))
            f.write("yes_callback varnames: %r\n" % (c.co_varnames,))
            # disassemble opcode
            import opcode
            code = bytearray(c.co_code)
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
            f.write("yes_callback ops: %r\n" % (lines,))
