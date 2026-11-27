import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:1800] + '\n')
try:
    cu = sys.modules['currency_utils']
    w('cu names: %r' % ([a for a in dir(cu) if not a.startswith('__')],))
    w('cu.YUANBAO=%r' % (getattr(cu, 'YUANBAO', 'NA'),))
    import types as T
    for a in dir(cu):
        v = getattr(cu, a)
        if isinstance(v, type) or (hasattr(v, '__dict__') and not callable(v)):
            w('cls %s: %r' % (a, dict((k, x) for k, x in vars(v).items() if not k.startswith('_') and isinstance(x, (int, long)))))
    lp = sys.modules['dts_appearance_utils'].legacyProperties
    i = 0
    for d in lp.iterDtsHallPropData():
        w('item %d: %r' % (i, d)); i += 1
        if i >= 3: break
    w('getDtsHallPropData doc/example: %r' % (lp.getDtsHallPropData,))
except Exception:
    w(traceback.format_exc())
f.close()
