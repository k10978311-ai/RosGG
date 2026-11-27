f = open(OUT, "w")
try:
    import BigWorld
    p = BigWorld.player()
    f.write("hasattr(p, 'enterHall'): %r\n" % hasattr(p, 'enterHall'))
    f.write("p.enterHall: %r\n" % getattr(p, 'enterHall', None))
    fn = getattr(p, 'enterHall', None)
    if fn and hasattr(fn, 'im_func'):
        fc = fn.im_func.func_code
        f.write("enterHall co_varnames: %r\n" % (fc.co_varnames,))
        f.write("enterHall co_consts: %r\n" % (fc.co_consts,))
        f.write("enterHall co_names: %r\n" % (fc.co_names,))
    fn2 = getattr(p, 'enterHallUI', None)
    if fn2 and hasattr(fn2, 'im_func'):
        fc2 = fn2.im_func.func_code
        f.write("enterHallUI co_varnames: %r\n" % (fc2.co_varnames,))
        f.write("enterHallUI co_consts: %r\n" % (fc2.co_consts,))
        f.write("enterHallUI co_names: %r\n" % (fc2.co_names,))
    # Check if there are other methods like onEnterHall, _realEnterHall, etc.
    for m in dir(p):
        if 'hall' in m.lower():
            f.write("hall-related attr: %s = %r\n" % (m, getattr(p, m)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
