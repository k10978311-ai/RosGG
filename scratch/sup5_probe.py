import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:1500] + '\n')
try:
    su = sys.modules['supplement_utils']
    d = su.getAvailableSupplementDictByTime()
    for sid in (1, 2, 5, 9728, 9100):
        o = d[sid]
        attrs = {}
        for a in dir(o):
            if a.startswith('_'): continue
            try: v = getattr(o, a)
            except Exception: continue
            if callable(v): continue
            attrs[a] = v if isinstance(v, (int, long, float, str, unicode, bool, type(None))) else (type(v).__name__ + ':' + repr(v)[:60])
        w('%d %s %r' % (sid, type(o).__name__, attrs))
except Exception:
    w(traceback.format_exc())
f.close()
