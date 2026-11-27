import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:300] + '\n')
try:
    import BigWorld, Globals
    p = BigWorld.player()
    for a in sorted(dir(p)):
        if a.startswith('__'): continue
        if any(k in a.lower() for k in ('match', 'teamstate', 'hallstate', 'inteam', 'isleader', 'queue')):
            try: v = getattr(p, a)
            except Exception: continue
            if not callable(v): w('%s = %r' % (a, v))
    m = Globals.uiMgr
    fn = getattr(m, 'isMatchingStateCanNotEnter', None) or getattr(m, 'checkMatchingState', None)
    w('fn %r' % (fn,))
    for a in dir(m):
        if 'match' in a.lower(): w('uiMgr.%s' % a)
except Exception:
    w(traceback.format_exc())
f.close()
