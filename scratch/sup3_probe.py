import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    su = sys.modules['supplement_utils']
    d = su.getAvailableSupplementDictByTime()
    sc = [m for k, m in sys.modules.items() if m is not None and hasattr(m, 'SupplementKindEnum')][0].SupplementKindEnum
    names = dict((getattr(sc, a), a) for a in dir(sc) if not a.startswith('_') and isinstance(getattr(sc, a), (int, long)))
    for k in sorted(d.keys()):
        try: kind = su.getSupplementKind(k)
        except Exception as e: kind = 'ERR'
        v = d[k]
        w('K %d %s %s cur=%r' % (k, names.get(kind, kind), type(v).__name__, getattr(su.getSupplementData(k) if hasattr(su,'getSupplementData') else None, 'CURRENCY_TYPE', None) if False else ''))
except Exception:
    w(traceback.format_exc())
f.close()
