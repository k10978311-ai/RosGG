with open(OUT, 'w') as f:
    try:
        import sys
        found = []
        for mod_name, mod in sorted(sys.modules.items()):
            if not mod: continue
            for k, v in getattr(mod, '__dict__', {}).items():
                co = getattr(v, 'func_code', None)
                if hasattr(co, 'co_names') and 'enterSelectModeFinished' in co.co_names:
                    code_bytes = bytearray(co.co_code)
                    names = co.co_names
                    for i in range(len(code_bytes)-2):
                        op = code_bytes[i]
                        arg = code_bytes[i+1] | (code_bytes[i+2] << 8)
                        if op in (95, 97, 156) and arg < len(names) and names[arg] == 'enterSelectModeFinished':
                            found.append((mod_name + '.' + k, op))
                for c in getattr(co, 'co_consts', ()):
                    if hasattr(c, 'co_names') and 'enterSelectModeFinished' in c.co_names:
                        names = c.co_names
                        cb = bytearray(c.co_code)
                        for i in range(len(cb)-2):
                            op = cb[i]
                            arg = cb[i+1] | (cb[i+2] << 8)
                            if op in (95, 97, 156) and arg < len(names) and names[arg] == 'enterSelectModeFinished':
                                found.append((mod_name + '.' + k + '>' + getattr(c, 'co_name', '?'), op))
        f.write('found stores: ' + repr(found) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
