# READ-ONLY: names/consts used by <module>.<class>.onCreate for selected interfaces + player state.
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
MODS = ['iDtsLevelSystem']
for m in MODS:
    mod = sys.modules.get(m)
    if mod is None:
        w('%s not loaded' % m); continue
    cls = getattr(mod, m, None)
    fn = cls.__dict__.get('onCreate') if cls else None
    if fn is None:
        w('%s.onCreate missing' % m); continue
    co = fn.func_code
    w('%s.onCreate names=%s consts=%r' % (m, list(co.co_names), [c for c in co.co_consts if not isinstance(c, types.CodeType)]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType):
            w('   inner %s names=%s' % (c.co_name, list(c.co_names)))
import BigWorld
p = BigWorld.player()
w('player=%r' % (p,))
for k in ('dtsLevel', 'dtsExp', 'dtsRos2ExpSeasonData', 'specialAwardState', 'dtsLevelAwardState'):
    w('  %s=%r' % (k, getattr(p, k, '<missing>')))
f.close()
