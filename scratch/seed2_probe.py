import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:1200] + '\n')
try:
    cu = sys.modules['currency_utils']
    for a in sorted(dir(cu)):
        if a.startswith('_'): continue
        v = getattr(cu, a)
        if not callable(v) and not hasattr(v, '__dict__') or isinstance(v, (int, long, str)):
            w('cu.%s = %r' % (a, v))
    lp = sys.modules['dts_appearance_utils'].legacyProperties
    n = 0; types = {}
    first = []
    for d in lp.iterDtsHallPropData():
        n += 1
        t = getattr(d, 'PROP_TYPE', None)
        tn = t.__class__.__name__ if t is not None else None
        types[tn] = types.get(tn, 0) + 1
        if len(first) < 3: first.append(d)
    w('total %d types %r' % (n, types))
    for d in first:
        w('sample attrs: %r' % ([a for a in dir(d) if not a.startswith('_')][:40],))
        w('sample vals: %r' % (dict((a, getattr(d, a)) for a in dir(d) if not a.startswith('_') and not callable(getattr(d, a)))))
except Exception:
    w(traceback.format_exc())
f.close()
