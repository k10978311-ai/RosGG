import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:400] + '\n')
try:
    u = sys.modules['dts_appearance_utils']
    hits = {'body': [], 'wear': []}
    for i in list(range(1, 400)) + list(range(10000, 10400)) + list(range(100000, 100200)):
        for nm, fn in (('body', u.getBodyAppearanceData), ('wear', u.getWearableAppearanceData)):
            try: d = fn(i)
            except Exception: d = None
            if d: hits[nm].append((i, d))
    for nm in hits:
        w('%s hits=%d' % (nm, len(hits[nm])))
        for i, d in hits[nm][:8]: w('  %r -> %r' % (i, d))
except Exception:
    w(traceback.format_exc())
f.close()
