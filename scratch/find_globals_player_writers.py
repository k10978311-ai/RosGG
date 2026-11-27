with open(OUT, 'w') as f:
    try:
        import sys, types, dis
        for modname, mod in sys.modules.items():
            if not mod: continue
            for k, v in mod.__dict__.items():
                if isinstance(v, types.FunctionType):
                    co = v.func_code
                    if 'player' in co.co_names and 'Globals' in co.co_names:
                        # check if STORE_ATTR or STORE_GLOBAL sets player
                        code = co.co_code
                        # search for STORE_ATTR with index of player
                        p_idx = co.co_names.index('player')
                        for i in range(len(code)-2):
                            op = ord(code[i])
                            # op 96 is STORE_ATTR or similar in NeoX? Let's check dis
                            # in standard Python STORE_ATTR is 95
                            # let's just record the function
                        f.write('Func: %s.%s\n' % (modname, k))
                elif isinstance(v, (type, types.ClassType)):
                    for k2, v2 in v.__dict__.items():
                        if isinstance(v2, (types.FunctionType, types.MethodType)):
                            fn = getattr(v2, 'im_func', v2)
                            co = getattr(fn, 'func_code', None)
                            if co and 'player' in co.co_names and 'Globals' in co.co_names:
                                f.write('Method: %s.%s.%s\n' % (modname, k, k2))
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
