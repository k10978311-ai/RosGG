# READ-ONLY: names/consts of PlayerAthlete hall-entry methods (decorators unwrapped).
import types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import Athlete
def unwrap(fn):
    for cell in (getattr(fn, 'func_closure', None) or ()):
        try: v = cell.cell_contents
        except ValueError: continue
        if isinstance(v, types.FunctionType): return unwrap(v)
    return fn
for cls in Athlete.PlayerAthlete.__mro__:
    for n in ('enterHall', 'preloadMap', 'onLogin'):
        fn = cls.__dict__.get(n)
        if isinstance(fn, types.FunctionType):
            g = unwrap(fn); co = g.func_code
            w('%s.%s(%s) names=%s consts=%r' % (cls.__name__, n, ','.join(co.co_varnames[:co.co_argcount]), list(co.co_names), [c for c in co.co_consts if not isinstance(c, types.CodeType)][:25]))
f.close()
