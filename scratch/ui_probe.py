import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:600] + '\n')
try:
    import Globals
    m = Globals.uiMgr
    w('uiMgr %r' % (m,))
    for a in dir(m):
        if a.startswith('__'): continue
        try: v = getattr(m, a)
        except Exception: continue
        if callable(v): continue
        s = repr(v)
        if any(k in a.lower() for k in ('lock','block','loading','busy','enter','cur','stack','pending','wait','forbid','disable','touch')):
            w('%s = %s' % (a, s[:200]))
except Exception:
    w(traceback.format_exc())
f.close()
