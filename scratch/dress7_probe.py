import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:500] + '\n')
try:
    u = sys.modules['dts_appearance_utils']
    for i in (1110375, 1110409):
        for fn in ('getWearableAppearanceData','getBodyAppearanceData','getDtsWearableAppearanceCategory','getDtsWearableAppearanceGender','getDtsBodyAppearanceGender'):
            try: w('%s(%d) = %r' % (fn, i, getattr(u, fn)(i)))
            except Exception as e: w('%s(%d) ERR %r' % (fn, i, e))
    # body ids: scan likely ranges
    found = []
    for i in list(range(1000000, 1000300)) + list(range(2000000, 2000100)) + list(range(1100000,1100100)):
        try:
            d = u.getBodyAppearanceData(i)
            if d: found.append((i, d))
        except Exception: pass
    w('body found %d' % len(found))
    for i, d in found[:6]: w('  %r %r' % (i, d))
except Exception:
    w(traceback.format_exc())
f.close()
