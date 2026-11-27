# READ-ONLY: code objects that reference loading-screen hide/close names
import sys, types, re
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
pat = re.compile(r'(hide|close|finish|end|destroy|remove)\w*loading|loading\w*(hide|close|finish|end|done|over)', re.I)
seen = set()
def scan(co, path, depth=0):
    if depth > 6 or id(co) in seen: return
    seen.add(id(co))
    hits = [n for n in co.co_names if pat.search(n)]
    if hits: w('%s L%d %s' % (path, co.co_firstlineno, hits))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): scan(c, path + '.' + c.co_name, depth + 1)
def fnof(x):
    fn = getattr(x, '__func__', x)
    if isinstance(x, property): fn = x.fget
    while isinstance(fn, types.FunctionType) and fn.func_closure:
        nxt = [c.cell_contents for c in fn.func_closure if isinstance(getattr(c, 'cell_contents', None), types.FunctionType)]
        if not nxt: break
        fn = nxt[0]
    return fn if isinstance(fn, types.FunctionType) else None
for mname, mod in sorted(sys.modules.items()):
    if mod is None or not mname.split('.')[0] in ('entities', 'helpers', 'player', 'ui', 'UI', 'logic', 'battle', 'systems', 'common', 'libclaudia'): continue
    for k, v in list(getattr(mod, '__dict__', {}).items()):
        if isinstance(v, (type, types.ClassType)) and getattr(v, '__module__', '') == mname:
            for a, x in list(v.__dict__.items()):
                fn = fnof(x)
                if fn: scan(fn.func_code, '%s.%s.%s' % (mname, k, a))
        elif isinstance(v, types.FunctionType) and getattr(v, '__module__', '') == mname:
            scan(v.func_code, '%s.%s' % (mname, k))
f.close()
