import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:900] + '\n')
try:
    u = sys.modules['dts_appearance_utils']
    d = u.specialAppearanceDataReverseDict
    w('special keys sample %r' % (sorted(d.keys())[:10],))
    for fn in ('getDtsWearableAppearanceGender','getDtsBodyAppearancePart','getWearableItemList'):
        fo = getattr(u, fn)
        c = getattr(fo, 'func_code', None)
        w('%s names=%r consts=%r' % (fn, c.co_names if c else None, c.co_consts[:8] if c else None))
    import inspect
    w('getBodyAppearanceData is %r' % (u.getBodyAppearanceData,))
    for k in list(sys.modules):
        if k.split('.')[-1].lower().startswith(('dts_appearance_data','appearance_data','dtsappearance_data')) or 'wearableappearance' in k.lower() or 'bodyappearance' in k.lower():
            w('mod ' + k)
    w('gender1 hall default: ' + repr(getattr(sys.modules.get('const'), 'DEFAULT_APPEARANCE', None)))
except Exception:
    w(traceback.format_exc())
f.close()
