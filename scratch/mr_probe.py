import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:500] + '\n')
try:
    lp = sys.modules['dts_appearance_utils'].legacyProperties
    d = lp.getMonthPayRebateSpecialAwardData()
    al = d.AWARD_LIST
    w('AWARD_LIST len=%d sample=%r' % (len(al), al[0] if len(al) else None))
    sc = sys.modules.get('shared_const')
    e = sc.MonthPayRebateSpecialAwardStatusEnum
    w('enum %r' % ([(a, getattr(e, a)) for a in dir(e) if not a.startswith('_')],))
    import BigWorld
    p = BigWorld.player()
    w('info now %r' % (getattr(p, 'monthPayRebateSpecialAwardInfo', 'MISSING'),))
    w('status now %r' % (getattr(p, 'monthPayRebateSpecialAwardStatus', 'MISSING'),))
except Exception:
    w(traceback.format_exc())
f.close()
