# READ-ONLY: where is characterInfo defined/used? (properties + code objects naming it)
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
seen = set()
def scan(co, path, depth=0):
    if depth > 6 or id(co) in seen: return
    seen.add(id(co))
    if 'characterInfo' in co.co_names: w('code %s line=%d names=%s' % (path, co.co_firstlineno, [n for n in co.co_names][:25]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): scan(c, path + '.' + c.co_name, depth + 1)
for mname, mod in sorted(sys.modules.items()):
    if mod is None or not (mname.startswith('player') or mname.startswith('entities') or mname.startswith('helpers') or mname.startswith('data')): continue
    for k, v in list(getattr(mod, '__dict__', {}).items()):
        if isinstance(v, (type, types.ClassType)) and getattr(v, '__module__', '') == mname:
            for a, x in list(v.__dict__.items()):
                if a == 'characterInfo': w('CLASS ATTR %s.%s = %r' % (mname, k, x))
                if isinstance(x, property):
                    for g in (x.fget, x.fset):
                        if g: scan(g.func_code, '%s.%s.%s(prop)' % (mname, k, a))
                fn = getattr(x, '__func__', x)
                if isinstance(fn, types.FunctionType):
                    while fn.func_closure:
                        nxt = [c.cell_contents for c in fn.func_closure if isinstance(getattr(c, 'cell_contents', None), types.FunctionType)]
                        if not nxt: break
                        fn = nxt[0]
                    scan(fn.func_code, '%s.%s.%s' % (mname, k, a))
        elif isinstance(v, types.FunctionType) and getattr(v, '__module__', '') == mname:
            scan(v.func_code, '%s.%s' % (mname, k))
f.close()
