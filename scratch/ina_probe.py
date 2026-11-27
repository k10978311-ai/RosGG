import sys, types, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    G = sys.modules['GameInit']
    for nm in ('_setInactivityTimeoutOnPause','updateInactivityTimeout','setInactivityWatchAd'):
        o = None
        for k, v in vars(G).items():
            if hasattr(v, '__dict__') and nm in getattr(v, '__dict__', {}): o = v.__dict__[nm]; break
        if o is None and hasattr(G, nm): o = getattr(G, nm)
        o = getattr(o, '__func__', o)
        co = o.func_code
        w('== %s args=%r names=%r consts=%r' % (nm, co.co_varnames[:co.co_argcount], list(co.co_names), [repr(c)[:60] for c in co.co_consts]))
    try:
        import BigWorld; w('getInactivityTimeout=%r' % (BigWorld.getInactivityTimeout(),))
    except Exception as e: w('get err %r' % e)
except Exception:
    w(traceback.format_exc())
f.close()
