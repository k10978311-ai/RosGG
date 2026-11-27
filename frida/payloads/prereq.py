# READ-ONLY: show where 'prerequisites' resolves for PlayerAccount and dump its code (no calls).
import types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
def cs(co, path, depth=0):
    if depth > 4: return
    consts = [c for c in co.co_consts if not isinstance(c, types.CodeType)][:40]
    w('%s%s(%s) names=%s consts=%r' % ('  ' * depth, path, ','.join(co.co_varnames[:co.co_argcount]), list(co.co_names), consts))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): cs(c, c.co_name, depth + 1)
def unwrap(fn, path, depth=0):
    if depth > 3 or not isinstance(fn, types.FunctionType): return
    cs(fn.func_code, path, depth)
    for cell in (fn.func_closure or ()):
        try: v = cell.cell_contents
        except ValueError: continue
        if isinstance(v, types.FunctionType): unwrap(v, path + '>' + v.__name__, depth + 1)
import Account
for cls in Account.PlayerAccount.__mro__:
    if 'prerequisites' in cls.__dict__:
        v = cls.__dict__['prerequisites']
        w('prerequisites defined in %s.%s (%s)' % (cls.__module__, cls.__name__, type(v).__name__))
        if isinstance(v, types.FunctionType): unwrap(v, cls.__name__ + '.prerequisites')
        else: w('  value=%r' % (v,))
f.close()
