with open(OUT, 'w') as f:
    import sys
    for mod_name in ['entities.Athlete', 'Athlete']:
        if mod_name in sys.modules:
            mod = sys.modules[mod_name]
            f.write("mod: %s\n" % mod)
            for name, obj in mod.__dict__.items():
                if hasattr(obj, '__dict__'):
                    for subname, subobj in obj.__dict__.items():
                        if 'hall' in subname.lower() or 'ready' in subname.lower():
                            f.write("  %s.%s = %r\n" % (name, subname, subobj))
