f = open(OUT, 'w')
try:
    import Athlete, dis, sys, StringIO
    func = Athlete.PlayerAthlete.showSelectCharacter
    if hasattr(func, 'im_func'):
        func = func.im_func
    f.write('func: %r\n' % func)
    buf = StringIO.StringIO()
    old = sys.stdout; sys.stdout = buf
    dis.dis(func)
    sys.stdout = old
    f.write('=== showSelectCharacter ===\n' + buf.getvalue() + '\n')
    
    # Also check sub-code objects
    for c in func.func_code.co_consts:
        if hasattr(c, 'co_name'):
            f.write('--- subcode %s ---\n' % c.co_name)
            buf = StringIO.StringIO()
            old = sys.stdout; sys.stdout = buf
            dis.dis(c)
            sys.stdout = old
            f.write(buf.getvalue() + '\n')
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
