with open(OUT, 'w') as f:
    try:
        import sys
        found = []
        def check_code(co, name):
            try:
                if not hasattr(co, 'co_names'): return
                if 'enterSelectModeFinished' in co.co_names or 'rookieEnterHall' in co.co_names:
                    found.append((name, getattr(co, 'co_name', '?'), [n for n in co.co_names if 'enter' in n.lower() or 'mode' in n.lower() or 'rookie' in n.lower()]))
                for c in co.co_consts:
                    if hasattr(c, 'co_names'):
                        check_code(c, name + '.' + getattr(c, 'co_name', '?'))
            except Exception:
                pass
        
        for mod_name, mod in sys.modules.items():
            if not mod: continue
            try:
                md = getattr(mod, '__dict__', None)
                if not md or not isinstance(md, dict): continue
                for k, v in md.items():
                    try:
                        co = getattr(v, 'func_code', None)
                        if co: check_code(co, mod_name + '.' + k)
                        vd = getattr(v, '__dict__', None)
                        if vd and isinstance(vd, dict):
                            for k2, v2 in vd.items():
                                try:
                                    co2 = getattr(v2, 'func_code', None)
                                    if co2: check_code(co2, mod_name + '.' + k + '.' + k2)
                                except Exception: pass
                    except Exception: pass
            except Exception: pass
        f.write('found (' + str(len(found)) + '): ' + repr(found) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
