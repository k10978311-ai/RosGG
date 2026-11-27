import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:500] + '\n')
try:
    import BigWorld
    p = BigWorld.player()
    for a in ('processedRedPoints','uiMainFunctionEntrance','mainTab'):
        w('%s = %r' % (a, getattr(p, a, 'MISSING')))
    for a in dir(p):
        if 'RedPoint' in a or 'redPoint' in a:
            w('%s = %r' % (a, getattr(p, a)))
except Exception:
    w(traceback.format_exc())
f.close()
