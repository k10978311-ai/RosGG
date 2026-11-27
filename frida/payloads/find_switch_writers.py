# READ-ONLY: code objects that reference both 'switches' and 'setattr' (runtime switch writers).
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
seen = set()
def walk(co, path, depth=0):
    if depth > 6 or id(co) in seen: return
    seen.add(id(co))
    n = co.co_names
    if 'setattr' in n and ('switches' in n or 'URGENT' in ' '.join(n)):
        w('%s names=%s consts=%r' % (path, list(n)[:30], [c for c in co.co_consts if isinstance(c, str)][:12]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): walk(c, path + '.' + c.co_name, depth + 1)
def scan(obj, path, depth=0):
    if depth > 3: return
    if isinstance(obj, types.FunctionType): walk(obj.func_code, path)
    elif isinstance(obj, (type, types.ClassType)):
        for k, v in list(obj.__dict__.items()):
            fn = getattr(v, 'func_code', None)
            if fn is not None: walk(fn, path + '.' + k)
for mname, mod in sorted(sys.modules.items()):
    if mod is None: continue
    try:
        for k, v in list(vars(mod).items()):
            if getattr(v, '__module__', None) == mname: scan(v, mname + ':' + k)
    except Exception: pass
f.close()
