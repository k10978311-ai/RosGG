# READ-ONLY introspection payload (run via frida/neox_py_eval.js). Never calls game logic.
import sys, types
f = open(OUT, 'w')
def w(s):
    f.write(s + '\n')

def code_summary(co, path, depth=0):
    if depth > 5:
        return
    strs = [c for c in co.co_consts if isinstance(c, str) and len(c) < 80]
    w('  %s%s names=%s strs=%s' % ('  ' * depth, path, list(co.co_names)[:60], strs[:30]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType):
            code_summary(c, c.co_name, depth + 1)

def dump_module(mname):
    mod = sys.modules.get(mname)
    if mod is None:
        w('## %s: NOT LOADED' % mname)
        return
    w('## %s (%s)' % (mname, getattr(mod, '__file__', '?')))
    for k, v in sorted(vars(mod).items()):
        if isinstance(v, types.FunctionType) and v.__module__ == mname:
            code_summary(v.func_code, k)
        elif isinstance(v, (type, types.ClassType)) and getattr(v, '__module__', None) == mname:
            w(' class %s bases=%s' % (k, [b.__name__ for b in v.__bases__]))
            for mk, mv in sorted(v.__dict__.items()):
                fn = getattr(mv, 'func_code', None) or getattr(getattr(mv, '__func__', None), 'func_code', None)
                if fn is not None:
                    code_summary(fn, k + '.' + mk, 1)

import BigWorld
w('player=%r' % (BigWorld.player(),))
try:
    w('entities=%r' % (dict(BigWorld.entities.items()) if hasattr(BigWorld, 'entities') else 'n/a',))
except Exception as e:
    w('entities err %r' % (e,))
w('BigWorld attrs: %s' % [a for a in dir(BigWorld) if not a.startswith('_')][:200])
w('modules w/ Proxy/Athlete/Account: %s' % sorted(m for m in sys.modules if any(x in m for x in ('Proxy', 'Athlete', 'Account'))))
for m in ('helpers.channel.channel_login', 'helpers.ConnectMonitor', 'ui.UILogin', 'iProxy', 'iProxyNoCell', 'LoginProxy'):
    dump_module(m)
f.close()
