with open(OUT, 'w') as f:
    import Avatar
    pa = getattr(Avatar, 'PlayerAvatar', None)
    if pa:
        f.write("PlayerAvatar dir: %r\n" % dir(pa))
        fn = getattr(pa, 'prerequisites', None)
        if fn and hasattr(fn, 'func_code'):
            f.write("PlayerAvatar.prerequisites co_names: %r\n" % (fn.func_code.co_names,))
            f.write("PlayerAvatar.prerequisites co_consts: %r\n" % (fn.func_code.co_consts,))
            f.write("PlayerAvatar.prerequisites co_varnames: %r\n" % (fn.func_code.co_varnames,))
            # dump code
            import dis, StringIO, sys
            buf = StringIO.StringIO()
            sys.stdout = buf
            dis.dis(fn)
            sys.stdout = sys.__stdout__
            f.write("dis:\n" + buf.getvalue())
