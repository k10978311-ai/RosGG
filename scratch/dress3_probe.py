import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:600] + '\n')
try:
    u = sys.modules['dts_appearance_utils']
    for nm in ('bodyAppearanceData','wearableAppearanceData'):
        d = getattr(u, nm, None)
        w('%s %r len=%r' % (nm, type(d), len(d) if d is not None else None))
    b = u.bodyAppearanceData
    keys = sorted(b.keys())[:6] if hasattr(b,'keys') else []
    for k in keys: w('body %r -> %r' % (k, b[k]))
    w('BodyCat %r' % ([ (a, getattr(u.BodyAppearanceCategoryEnum, a)) for a in dir(u.BodyAppearanceCategoryEnum) if not a.startswith('_')],))
    w('WearCat %r' % ([ (a, getattr(u.WearableAppearanceCategoryEnum, a)) for a in dir(u.WearableAppearanceCategoryEnum) if not a.startswith('_')],))
    wd = getattr(u, 'wearableAppearanceData', None)
    if wd:
        for k in sorted(wd.keys())[:4]: w('wear %r -> %r' % (k, wd[k]))
    # default-flag scan
    for nm, d in (('body', b), ('wear', wd or {})):
        c = 0
        for k, v in d.items():
            s = repr(v).lower()
            if 'default' in s or 'born' in s:
                w('%s default? %r -> %r' % (nm, k, v)); c += 1
                if c >= 6: break
except Exception:
    w(traceback.format_exc())
f.close()
