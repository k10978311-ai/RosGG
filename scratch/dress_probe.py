import sys, traceback, gc
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    import BigWorld
    p = BigWorld.player()
    w('player %r' % (p,))
    for a in ('dtsShowBodyAppearanceList','dtsShowWearableAppearanceList','dtsBodyAppearanceList','dtsWearableAppearanceList','dtsAppearanceGender','dtsOutGameBag','dtsOutGameWeapon','dtsShareAppearanceSuit','useOwnAppearOverHeroAppear','baseCharacterType'):
        w('%s = %r' % (a, getattr(p, a, 'MISSING')))
    m = sys.modules.get('dts_appearance_utils') or sys.modules.get('common.dts_appearance_utils')
    w('utils module %r' % (m,))
    for k in sys.modules:
        if 'appearance' in k.lower() or 'dress' in k.lower():
            w('mod ' + k)
except Exception:
    w(traceback.format_exc())
f.close()
