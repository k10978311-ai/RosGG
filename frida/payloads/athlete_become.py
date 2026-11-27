# READ-ONLY: full names of PlayerAthlete.onBecomePlayer and Globals.setInHall / related setters.
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
def cs(co, path, depth=0):
    if depth > 3: return
    w('%s%s(%s) names=%s consts=%r' % ('  ' * depth, path, ','.join(co.co_varnames[:co.co_argcount]), list(co.co_names), [c for c in co.co_consts if isinstance(c, (str, int, float)) and not isinstance(c, bool)][:20]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): cs(c, c.co_name, depth + 1)
import Athlete, Globals
cs(Athlete.PlayerAthlete.__dict__['onBecomePlayer'].func_code, 'PlayerAthlete.onBecomePlayer')
for k in sorted(vars(Globals)):
    v = getattr(Globals, k)
    if isinstance(v, types.FunctionType) and ('Hall' in k or 'layer' in k or k.startswith('set')):
        cs(v.func_code, 'Globals.' + k)
f.close()
