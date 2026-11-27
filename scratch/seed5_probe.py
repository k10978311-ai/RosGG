import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    c = sys.modules['const']
    for a in dir(c):
        if any(k in a.upper() for k in ('YUANBAO', 'COIN', 'CURRENCY', 'TICKET', 'DIAMOND', 'CASH', 'MONEY', 'GOLD')):
            v = getattr(c, a)
            if isinstance(v, (int, long)): w('const.%s = %r' % (a, v))
    lp = sys.modules['dts_appearance_utils'].legacyProperties
    cnt = {}; shown = 0
    rows = []
    for pid, p in lp.iterDtsHallPropData():
        t = getattr(p, 'PROP_TYPE', None)
        tn = type(t).__name__
        cnt[tn] = cnt.get(tn, 0) + 1
        if shown < 2:
            shown += 1
            w('EX %r %r' % (pid, [a for a in dir(p) if not a.startswith('_')][:60]))
        rows.append('%s,%s,%s,%s' % (pid, tn, getattr(p, 'CATEGORY', ''), getattr(p, 'GENDER', '')))
    w('TYPES %r' % (cnt,))
    f.write('\n'.join('ROW ' + r for r in rows) + '\n')
except Exception:
    w(traceback.format_exc())
f.close()
