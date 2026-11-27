# READ-ONLY: unwrap PlayerAthlete.onBecomePlayer (decorated) and dump the real body.
import types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
def cs(co, path, depth=0):
    if depth > 3: return
    w('%s%s(%s) names=%s consts=%r' % ('  ' * depth, path, ','.join(co.co_varnames[:co.co_argcount]), list(co.co_names), [c for c in co.co_consts if isinstance(c, (str, int, float)) and not isinstance(c, bool)][:30]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): cs(c, c.co_name, depth + 1)
def unwrap(fn, path, depth=0):
    if depth > 3 or not isinstance(fn, types.FunctionType): return
    if depth: cs(fn.func_code, path, 0)
    for cell in (fn.func_closure or ()):
        try: v = cell.cell_contents
        except ValueError: continue
        if isinstance(v, types.FunctionType): unwrap(v, path + '>' + v.__name__, depth + 1)
import Athlete
unwrap(Athlete.PlayerAthlete.__dict__['onBecomePlayer'], 'PlayerAthlete.onBecomePlayer')
f.close()
