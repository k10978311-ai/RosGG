# READ-ONLY: unwrap decorated PlayerAccount methods (closure cells) and read LoginRetCode consts.
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
def cs(co, path, depth=0):
    if depth > 4: return
    strs = [c for c in co.co_consts if isinstance(c, (str, int, long)) and not isinstance(c, bool)][:30]
    w('%s%s(%s) names=%s consts=%s' % ('  ' * depth, path, ','.join(co.co_varnames[:co.co_argcount]), list(co.co_names), strs))
    for c in co.co_consts:
        if isinstance(c, types.CodeType): cs(c, c.co_name, depth + 1)
def unwrap(fn, path, depth=0):
    if depth > 3 or not isinstance(fn, types.FunctionType): return
    cs(fn.func_code, path, depth)
    for cell in (fn.func_closure or ()):
        try:
            v = cell.cell_contents
        except ValueError:
            continue
        if isinstance(v, types.FunctionType):
            unwrap(v, path + '>' + v.__name__, depth + 1)
import Account
PA = Account.PlayerAccount
for name in ('onBecomePlayer', 'onChannelLogin', 'onLogin', 'onLoginPCServer'):
    fn = PA.__dict__.get(name)
    if fn is not None: unwrap(fn, 'PlayerAccount.' + name)
for name in sorted(Account.Account.__dict__):
    fn = Account.Account.__dict__[name]
    if isinstance(fn, types.FunctionType): unwrap(fn, 'Account.' + name)
try:
    import const
    for cname in ('LoginRetCode', 'ChannelLoginRetCode', 'ChannelLoginRet'):
        c = getattr(const, cname, None)
        if c is not None:
            w('const.%s = %r' % (cname, dict((k, v) for k, v in vars(c).items() if not k.startswith('__'))))
except Exception as e:
    w('const err %r' % (e,))
f.close()
