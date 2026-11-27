# READ-ONLY deep code scan over all loaded modules, unwrapping decorator closures
# (entity methods are wrapped, e.g. by elkLogging, so the real code lives in func_closure).
# Reports code objects that use any NEEDLE as a name or string constant, and fused
# `self.<attr> = ...` stores (remapped opcode 176) to any STORE_NEEDLE.
import sys, types
NEEDLES = ()
STORE_NEEDLES = ('player',)
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
seen_code = set(); seen_fn = set()
def walk_code(co, path, depth=0):
    if depth > 8 or id(co) in seen_code: return
    seen_code.add(id(co))
    used = set(co.co_names) | set(c for c in co.co_consts if isinstance(c, str))
    hit = [n for n in NEEDLES if n in used]
    code = co.co_code; i = 0; stores = []; prev = None
    while i < len(code):
        op = ord(code[i])
        if op >= 90:
            arg = ord(code[i + 1]) | (ord(code[i + 2]) << 8)
            if prev is not None and prev[0] == 155 and prev[1] < len(co.co_names) and co.co_names[prev[1]] == 'Globals'                     and arg < len(co.co_names) and co.co_names[arg] in STORE_NEEDLES and op != 96:
                stores.append('op%d %s' % (op, co.co_names[arg]))
            prev = (op, arg)
            i += 3
        else:
            prev = (op, None); i += 1
    if hit or stores:
        w('%s uses=%s stores=%s names=%s' % (path, hit, stores, list(co.co_names)[:25]))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): walk_code(c, path + '.' + c.co_name, depth + 1)
def walk_fn(fn, path, depth=0):
    if depth > 4 or id(fn) in seen_fn: return
    seen_fn.add(id(fn))
    walk_code(fn.func_code, path)
    for cell in (fn.func_closure or ()):
        try: v = cell.cell_contents
        except ValueError: continue
        if isinstance(v, types.FunctionType): walk_fn(v, path + '>' + v.__name__, depth + 1)
def walk_obj(v, path, depth=0):
    if depth > 3: return
    if isinstance(v, types.FunctionType): walk_fn(v, path)
    elif isinstance(v, (staticmethod, classmethod)): walk_obj(v.__func__, path, depth)
    elif isinstance(v, property):
        for g in (v.fget, v.fset):
            if g: walk_obj(g, path, depth)
    elif isinstance(v, (type, types.ClassType)):
        for k, x in list(v.__dict__.items()):
            walk_obj(x, path + '.' + k, depth + 1)
for mname, mod in sorted(sys.modules.items()):
    if mod is None: continue
    try:
        for k, v in list(vars(mod).items()):
            if getattr(v, '__module__', mname) == mname: walk_obj(v, mname + ':' + k)
    except Exception: pass
w('scanned code objects: %d' % len(seen_code))
f.close()
