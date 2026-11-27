# READ-ONLY: ui.UILoading structure + who references it
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
m = sys.modules['ui.UILoading']
for k, v in sorted(m.__dict__.items()):
    if isinstance(v, (type, types.ClassType)) and v.__module__ == m.__name__:
        w('class %s bases=%s' % (k, [b.__name__ for b in v.__bases__]))
        for a, x in sorted(v.__dict__.items()):
            fn = getattr(x, '__func__', x)
            if isinstance(fn, types.FunctionType):
                co = fn.func_code
                w('  %s L%d names=%s' % (a, co.co_firstlineno, list(co.co_names)[:18]))
    elif not k.startswith('__'):
        w('global %s = %s' % (k, repr(v)[:80]))
seen = set()
def scan(co, path, depth=0):
    if depth > 6 or id(co) in seen: return
    seen.add(id(co))
    if 'UILoading' in co.co_names: w('REF %s L%d %s' % (path, co.co_firstlineno, [n for n in co.co_names if n[0].isupper() or 'oad' in n][:14]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): scan(c, path + '.' + c.co_name, depth + 1)
for mname, mod in sorted(sys.modules.items()):
    if mod is None or mname == 'ui.UILoading': continue
    for k, v in list(getattr(mod, '__dict__', {}).items()):
        if isinstance(v, (type, types.ClassType)) and getattr(v, '__module__', '') == mname:
            for a, x in list(v.__dict__.items()):
                fn = getattr(x, '__func__', x)
                while isinstance(fn, types.FunctionType) and fn.func_closure:
                    nxt = [c.cell_contents for c in fn.func_closure if isinstance(getattr(c, 'cell_contents', None), types.FunctionType)]
                    if not nxt: break
                    fn = nxt[0]
                if isinstance(fn, types.FunctionType): scan(fn.func_code, '%s.%s.%s' % (mname, k, a))
        elif isinstance(v, types.FunctionType) and getattr(v, '__module__', '') == mname:
            scan(v.func_code, '%s.%s' % (mname, k))
f.close()
