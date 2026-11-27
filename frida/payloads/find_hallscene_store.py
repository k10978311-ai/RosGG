# READ-ONLY: find code objects that do `Globals.<attr> = ...` using the remapped opcodes
# (LOAD_GLOBAL=155, STORE_ATTR=176 in this NeoX build, from hand-decoding).
import sys, types
TARGETS = ('hallScene', 'player', 'hallSceneReady')
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
seen = set()
def scan(co, path, depth=0):
    if depth > 6 or id(co) in seen: return
    seen.add(id(co))
    names = co.co_names
    code = co.co_code
    i, n = 0, len(code)
    prev = None
    while i < n:
        op = ord(code[i])
        if op >= 90:
            arg = ord(code[i + 1]) | (ord(code[i + 2]) << 8)
            if op == 176 and arg < len(names) and names[arg] in TARGETS and prev is not None:
                pop, parg = prev
                if pop == 155 and parg < len(names):
                    w('%s : %s.%s = ...' % (path, names[parg], names[arg]))
                elif pop in (124, 160):
                    w('%s : <local/self>.%s = ...' % (path, names[arg]))
            prev = (op, arg)
            i += 3
        else:
            prev = (op, None)
            i += 1
    for c in co.co_consts:
        if isinstance(c, types.CodeType): scan(c, path + '.' + c.co_name, depth + 1)
def walk(obj, path, depth=0):
    if depth > 3: return
    if isinstance(obj, types.FunctionType): scan(obj.func_code, path)
    elif isinstance(obj, (type, types.ClassType)):
        for k, v in list(obj.__dict__.items()):
            if isinstance(v, (types.FunctionType, staticmethod, classmethod)) or isinstance(v, (type, types.ClassType)):
                fn = getattr(v, '__func__', v)
                walk(fn, path + '.' + k, depth + 1)
for mname, mod in sorted(sys.modules.items()):
    if mod is None: continue
    try:
        for k, v in list(vars(mod).items()):
            if getattr(v, '__module__', None) == mname: walk(v, mname + ':' + k)
    except Exception: pass
f.close()
