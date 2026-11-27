with open(OUT, 'w') as f:
    try:
        import sys, types
        found = []
        def check_code(co, name):
            if not hasattr(co, 'co_names'): return
            if 'enterSelectModeFinished' in co.co_names:
                found.append(name)
            for c in co.co_consts:
                if hasattr(c, 'co_names'):
                    check_code(c, name + '.' + getattr(c, 'co_name', '?'))
        
        for mod_name, mod in sys.modules.items():
            if not mod: continue
            for k, v in getattr(mod, '__dict__', {}).items():
                co = getattr(v, 'func_code', getattr(v, '__code__', None))
                if co:
                    check_code(co, mod_name + '.' + k)
                for k2, v2 in getattr(v, '__dict__', {}).items():
                    co2 = getattr(v2, 'func_code', getattr(v2, '__code__', None))
                    if co2:
                        check_code(co2, mod_name + '.' + k + '.' + k2)
        f.write('found: ' + repr(found) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
