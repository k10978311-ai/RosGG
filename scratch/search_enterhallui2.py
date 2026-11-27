with open(OUT, 'w') as f:
    import sys
    for mod_name, mod in sys.modules.items():
        if not mod: continue
        for k, v in getattr(mod, '__dict__', {}).items():
            co = getattr(v, 'func_code', None)
            if co and 'enterHallUI' in getattr(co, 'co_names', ()):
                f.write("%s.%s calls enterHallUI\n" % (mod_name, k))
            elif hasattr(v, '__dict__'):
                for sk, sv in v.__dict__.items():
                    co = getattr(sv, 'func_code', None)
                    if co and 'enterHallUI' in getattr(co, 'co_names', ()):
                        f.write("%s.%s.%s calls enterHallUI\n" % (mod_name, k, sk))
