TARGETS = [
 ('player.logic_ctrls.PlayerAvatarController', 'PlayerAvatarController', 'setCampType', 140, 175),
 ('libclaudia.Classes.Physics', 'Physics', 'RemoveGameObject', 85, 100),
 ('entities.Avatar', 'PlayerAvatar', '_createPlayerGO', 2300, 2340),
 ('player.logic_ctrls.PlayerStatesV2', 'PlayerStatesV2', 'Start', 2405, 2420),
 ('player.appearance.iDress', 'iDress', 'initDress', 30, 42),
]
# READ-ONLY: line-mapped disassembly of selected functions (names/consts/varnames resolved per arg).
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
def unwrap(fn):
    for cell in (getattr(fn, 'func_closure', None) or ()):
        try: v = cell.cell_contents
        except ValueError: continue
        if isinstance(v, types.FunctionType): return unwrap(v)
    return fn
def lines(co):
    m = {}; addr = 0; ln = co.co_firstlineno; t = co.co_lnotab
    for k in range(0, len(t), 2):
        m.setdefault(addr, ln); addr += ord(t[k]); ln += ord(t[k+1])
    m.setdefault(addr, ln); return m
def dis(modname, clsname, meth, lo, hi):
    mod = sys.modules.get(modname)
    obj = getattr(mod, clsname, None) if (mod and clsname) else mod
    fn = obj.__dict__.get(meth) if obj is not None else None
    if fn is None: w('## %s.%s.%s not found' % (modname, clsname, meth)); return
    if isinstance(fn, (staticmethod, classmethod)): fn = fn.__func__
    co = unwrap(fn).func_code
    w('## %s.%s.%s first=%d vars=%s' % (modname, clsname, meth, co.co_firstlineno, list(co.co_varnames)))
    lm = lines(co); code = co.co_code; i = 0; cur = co.co_firstlineno
    while i < len(code):
        if i in lm: cur = lm[i]
        op = ord(code[i]); s = ''
        if op >= 90:
            arg = ord(code[i+1]) | (ord(code[i+2]) << 8)
            n = co.co_names[arg] if arg < len(co.co_names) else '-'
            c = repr(co.co_consts[arg])[:30] if arg < len(co.co_consts) else '-'
            v = co.co_varnames[arg] if arg < len(co.co_varnames) else '-'
            s = '%5d n=%s c=%s v=%s' % (arg, n, c, v); step = 3
        else: step = 1
        if lo <= cur <= hi: w('L%-5d %4d op%-3d %s' % (cur, i, op, s))
        i += step
for spec in TARGETS:
    try: dis(*spec)
    except Exception as e: w('ERR %r %r' % (spec, e))
f.close()
