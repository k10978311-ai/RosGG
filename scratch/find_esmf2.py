with open(OUT, 'w') as f:
    try:
        import sys, types
        found = []
        for mod_name, mod in sys.modules.items():
            if not mod: continue
            for k, v in getattr(mod, '__dict__', {}).items():
                if isinstance(v, (types.FunctionType, types.MethodType)):
                    co = getattr(v, 'func_code', None)
                    if co and 'enterSelectModeFinished' in co.co_names:
                        found.append(mod_name + '.' + k)
                elif isinstance(v, (type, types.ClassType)):
                    for k2, v2 in getattr(v, '__dict__', {}).items():
                        if isinstance(v2, (types.FunctionType, types.MethodType)):
                            co = getattr(v2, 'func_code', None)
                            if co and 'enterSelectModeFinished' in co.co_names:
                                found.append(mod_name + '.' + k + '.' + k2)
        f.write('found: ' + repr(found) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
