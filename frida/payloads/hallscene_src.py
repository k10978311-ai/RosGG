# READ-ONLY: SceneSystem.loadHallScene / DoLoadNeoxScene names, and how Application.scene is defined.
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
SS = sys.modules['libclaudia.Classes.SceneSystem'].SceneSystem
for n in ('loadHallScene', 'DoLoadNeoxScene', 'onSceneLoaded', 'LoadLevel'):
    fn = SS.__dict__.get(n)
    if isinstance(fn, types.FunctionType):
        co = fn.func_code
        w('%s(%s) names=%s consts=%r' % (n, ','.join(co.co_varnames[:co.co_argcount]), list(co.co_names), [c for c in co.co_consts if isinstance(c, (str, int))][:20]))
        for c in co.co_consts:
            if isinstance(c, types.CodeType): w('   inner %s names=%s' % (c.co_name, list(c.co_names)[:40]))
import ClientEntity
App = vars(ClientEntity).get('Application')
d = type(App).__dict__.get('scene')
w('Application.scene descriptor=%r doc=%r' % (d, getattr(d, '__doc__', None)))
f.close()
