import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:600] + '\n')
try:
    u = sys.modules['dts_appearance_utils']
    try:
        wd = u.getWearableAppearanceData()
        w('wear ok len %r' % len(wd))
    except Exception:
        w('WEAR ERR ' + traceback.format_exc()); wd = {}
    try:
        b = u.getBodyAppearanceData()
    except Exception:
        w('BODY ERR ' + traceback.format_exc()); b = {}
    w('body %r len %r; wear %r len %r' % (type(b), len(b), type(wd), len(wd)))
    for k in sorted(b)[:5]: w('body %r -> %r' % (k, b[k]))
    for k in sorted(wd)[:3]: w('wear %r -> %r' % (k, wd[k]))
    # males: body ids by category 1 FACE 2 HAIR 3 GENDER
    for cat in (1, 2, 3):
        ids = [k for k in sorted(b) if u.getDtsBodyAppearanceCategory(k) == cat and u.getDtsBodyAppearanceGender(k) == 1]
        w('body cat %d male ids: %r' % (cat, ids[:10]))
    for cat in (1, 2, 3, 4, 5, 6):
        ids = [k for k in sorted(wd) if u.getDtsWearableAppearanceCategory(k) == cat and u.getDtsWearableAppearanceGender(k) in (1, 0)]
        w('wear cat %d male ids: %r' % (cat, ids[:10]))
except Exception:
    w(traceback.format_exc())
f.close()
