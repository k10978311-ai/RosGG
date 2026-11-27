# READ-ONLY: ui.UILoading structure + who references it
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
seen = set()
def scan(co, path, depth=0):
    if depth > 6 or id(co) in seen: return
    seen.add(id(co))
    if 'preload_resource' in co.co_names and ('model_path' in co.co_names or 'dts_model_path' in co.co_names or 'characterType' in co.co_names or 'getCharactersData' in co.co_names): w('REF %s L%d %s' % (path, co.co_firstlineno, list(co.co_names)[:40]))
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
