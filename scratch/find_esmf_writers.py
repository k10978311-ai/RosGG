with open(OUT, 'w') as f:
    try:
        import sys
        found = []
        for mod_name, mod in sorted(sys.modules.items()):
            if not mod: continue
            for k, v in getattr(mod, '__dict__', {}).items():
                co = getattr(v, 'func_code', None)
                if co and 'enterSelectModeFinished' in co.co_names:
                    # check if it stores into it
                    code_bytes = bytearray(co.co_code)
                    names = co.co_names
                    for i in range(len(code_bytes)-2):
                        op = code_bytes[i]
                        arg = code_bytes[i+1] | (code_bytes[i+2] << 8)
                        # op 156 is STORE_ATTR or STORE_GLOBAL
                        if op in (95, 97, 156) and arg < len(names) and names[arg] == 'enterSelectModeFinished':
                            found.append((mod_name + '.' + k, op))
        f.write('found stores to enterSelectModeFinished: ' + repr(found) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
