import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s[:700] + '\n')
try:
    import BigWorld
    p = BigWorld.player()
    for a in dir(p):
        if a.startswith('iLuckyCarnival'): w('player.%s = %r' % (a, getattr(p, a)))
    c = sys.modules['const'].LuckyCarnivalConst
    for a in dir(c):
        if not a.startswith('_'): w('%s = %r' % (a, getattr(c, a)))
except Exception:
    w(traceback.format_exc())
f.close()
