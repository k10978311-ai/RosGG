# READ-ONLY: GameEntry module functions and the loadingDefaultScene body.
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
m = sys.modules.get('GameEntry')
w('GameEntry=%r file=%r' % (m, getattr(m, '__file__', None)))
if m:
    for k, v in sorted(vars(m).items()):
        if isinstance(v, types.FunctionType) and v.__module__ == 'GameEntry':
            co = v.func_code
            w('%s(%s) names=%s consts=%r' % (k, ','.join(co.co_varnames[:co.co_argcount]), list(co.co_names)[:40], [c for c in co.co_consts if isinstance(c, (str, int))][:15]))
f.close()
