with open(OUT, 'w') as f:
    import Avatar
    pa = Avatar.PlayerAvatar
    for m in ['enterHall', 'kickOutToHall', 'onRequestLeaveDynamicSpace', 'leaveMap']:
        fn = getattr(pa, m, None)
        if hasattr(fn, 'im_func'): fn = fn.im_func
        if fn and hasattr(fn, 'func_code'):
            f.write("=== %s ===\n" % m)
            f.write("co_names: %r\n" % (fn.func_code.co_names,))
            f.write("co_consts: %r\n" % ([c for c in fn.func_code.co_consts if not hasattr(c, 'co_names')],))
            f.write("co_varnames: %r\n" % (fn.func_code.co_varnames,))
