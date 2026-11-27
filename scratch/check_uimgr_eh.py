with open(OUT, 'w') as f:
    import Globals
    uiMgr = getattr(Globals, 'uiMgr', None)
    f.write("uiMgr: %r\n" % uiMgr)
    if uiMgr:
        f.write("enterHallUI: %r\n" % getattr(uiMgr, 'enterHallUI', None))
        fn = getattr(uiMgr, 'enterHallUI', None)
        if fn and hasattr(fn, 'func_code'):
            f.write("enterHallUI names: %r\n" % (fn.func_code.co_names,))
            f.write("enterHallUI consts: %r\n" % (fn.func_code.co_consts,))
