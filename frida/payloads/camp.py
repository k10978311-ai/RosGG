# READ-ONLY: camp_utils structures and where camp info comes from.
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import camp_utils as cu
for k, v in sorted(vars(cu).items()):
    if k.startswith('__'): continue
    if isinstance(v, types.FunctionType):
        co = v.func_code
        w('fn %s(%s) names=%s consts=%r' % (k, ','.join(co.co_varnames[:co.co_argcount]), list(co.co_names)[:25], [c for c in co.co_consts if isinstance(c, (str, int))][:10]))
    elif isinstance(v, (dict, list, tuple, int, str)) and len(repr(v)) < 600:
        w('var %s = %r' % (k, v))
    elif isinstance(v, (type, types.ClassType)) and getattr(v, '__module__', '') == cu.__name__:
        w('class %s: %s' % (k, [m for m in v.__dict__ if not m.startswith('__')][:30]))
        for mk, mv in v.__dict__.items():
            if isinstance(mv, types.FunctionType) and mk in ('isEnemy', '__ne__', '__init__', '__eq__'):
                co = mv.func_code
                w('   %s.%s names=%s consts=%r' % (k, mk, list(co.co_names), [c for c in co.co_consts if isinstance(c, (str, int))][:10]))
import BigWorld
p = BigWorld.player()
w('player=%r campType=%r camp=%r' % (p, getattr(p, 'campType', '?'), getattr(p, 'camp', '?')))
f.close()
