import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    c = sys.modules['const']
    for a in sorted(dir(c)):
        if any(k in a.upper() for k in ('YUANBAO', 'COIN', 'CURRENCY', 'STAR', 'TICKET', 'DIAMOND', 'CASH', 'MONEY', 'GOLD', 'TOKEN')) and isinstance(getattr(c, a), (int, long)):
            w('const.%s = %r' % (a, getattr(c, a)))
    lp = sys.modules['dts_appearance_utils'].legacyProperties
    cnt = {}; ex = {}
    rows = []
    for pid, p in lp.iterDtsHallPropData():
        t = getattr(p, 'PROP_TYPE', None)
        tn = type(t).__name__ + ':' + str(t)
        cnt[tn] = cnt.get(tn, 0) + 1
        attrs = dict((a, getattr(p, a)) for a in dir(p) if not a.startswith('_') and isinstance(getattr(p, a, None), (int, long, str, float)))
        if tn not in ex: ex[tn] = (pid, attrs)
        rows.append((pid, tn, attrs.get('CATEGORY'), attrs.get('GENDER'), attrs.get('QUALITY')))
    w('TYPES %r' % (cnt,))
    for k, v in ex.items(): w('EX %s %r' % (k, v))
    for r in rows: w('ROW %r' % (r,))
except Exception:
    w(traceback.format_exc())
f.close()
