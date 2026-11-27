with open(OUT, 'w') as f:
    try:
        import sys
        found = []
        for mod_name, mod in sys.modules.items():
            if not mod: continue
            for k, v in getattr(mod, '__dict__', {}).items():
                if hasattr(v, 'func_code'):
                    co = v.func_code
                    if 'enterSelectModeFinished' in co.co_names:
                        found.append(mod_name + '.' + k)
                elif hasattr(v, '__dict__'):
                    for k2, v2 in v.__dict__.items():
                        if hasattr(v2, 'func_code') and 'enterSelectModeFinished' in v2.func_code.co_names:
                            found.append(mod_name + '.' + k + '.' + k2)
        f.write('found: ' + repr(found) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
