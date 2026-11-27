with open(OUT, 'w') as f:
    try:
        import sys, types
        writers = []
        def check_code(co, name):
            if 'player' not in co.co_names:
                return
            p_idx = co.co_names.index('player')
            code = bytearray(co.co_code)
            for i in range(len(code)-2):
                # Check STORE_ATTR (95 in std python, but let's check any op with arg == p_idx)
                op = code[i]
                arg = code[i+1] | (code[i+2] << 8)
                if arg == p_idx:
                    # check if previous was LOAD_GLOBAL Globals or STORE_GLOBAL
                    writers.append((name, op, i, co.co_names))
            for c in co.co_consts:
                if hasattr(c, 'co_code'):
                    check_code(c, name + '.' + c.co_name)

        for mname, mod in sys.modules.items():
            if not mod: continue
            for k, v in mod.__dict__.items():
                if isinstance(v, types.FunctionType):
                    check_code(v.func_code, mname + '.' + k)
                elif isinstance(v, (type, types.ClassType)):
                    for k2, v2 in v.__dict__.items():
                        fn = getattr(v2, 'im_func', v2)
                        co = getattr(fn, 'func_code', None)
                        if co:
                            check_code(co, mname + '.' + k + '.' + k2)
        f.write('Found %d writers:\n' % len(writers))
        for w in writers:
            f.write('%r\n' % (w,))
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
