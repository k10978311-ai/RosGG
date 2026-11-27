# READ-ONLY: inspect channel_login.onLoginByServerSauth and ChannelLoginRetEnum.
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
def cs(co, path, depth=0):
    if depth > 4: return
    consts = [c for c in co.co_consts if isinstance(c, (str, int, long)) and not isinstance(c, bool)][:40]
    w('%s%s(%s) names=%s consts=%s' % ('  ' * depth, path, ','.join(co.co_varnames[:co.co_argcount]), list(co.co_names), consts))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): cs(c, c.co_name, depth + 1)
def unwrap(fn, path, depth=0):
    if depth > 3 or not isinstance(fn, types.FunctionType): return
    cs(fn.func_code, path, depth)
    for cell in (fn.func_closure or ()):
        try: v = cell.cell_contents
        except ValueError: continue
        if isinstance(v, types.FunctionType): unwrap(v, path + '>' + v.__name__, depth + 1)
cl = sys.modules.get('helpers.channel.channel_login')
for name in ('onLoginByServerSauth', 'login_callback'):
    fn = getattr(cl, name, None) if cl else None
    w('--- %s found=%s' % (name, fn is not None))
    if fn is not None: unwrap(fn, name)
for mname, mod in sys.modules.items():
    e = getattr(mod, 'ChannelLoginRetEnum', None) if mod else None
    if e is not None:
        w('ChannelLoginRetEnum@%s = %r' % (mname, dict((k, v) for k, v in vars(e).items() if not k.startswith('_'))))
        break
f.close()
