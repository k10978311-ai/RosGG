# READ-ONLY: code behind the remaining PlayerAvatar creation errors.
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
def unwrap(fn):
    for cell in (getattr(fn, 'func_closure', None) or ()):
        try: v = cell.cell_contents
        except ValueError: continue
        if isinstance(v, types.FunctionType): return unwrap(v)
    return fn
def dump(modname, clsname, meth):
    mod = sys.modules.get(modname)
    cls = getattr(mod, clsname, None) if mod else None
    fn = cls.__dict__.get(meth) if cls else None
    if fn is None:
        w('%s.%s.%s: not found' % (modname, clsname, meth)); return
    co = unwrap(fn).func_code
    w('%s.%s(%s) line0=%d names=%s consts=%r' % (clsname, meth, ','.join(co.co_varnames[:co.co_argcount]), co.co_firstlineno, list(co.co_names), [c for c in co.co_consts if isinstance(c, (str, int))][:15]))
dump('player.logic_ctrls.PlayerAvatarController', 'PlayerAvatarController', 'setCampType')
dump('libclaudia.Classes.Physics', 'Physics', 'RemoveGameObject')
dump('libclaudia.Classes.Physics', 'Physics', 'AddGameObject')
dump('player.logic_ctrls.PlayerStatesV2', 'PlayerStatesV2', 'Start')
dump('player.appearance.PlayerCommonAppear', 'PlayerCommonAppear', 'onInit')
import BigWorld
p = BigWorld.player()
for a in ('dtsBattlegroundPropAppearanceList', 'dtsShowBattlegroundPropAppearanceList', 'campType', 'mapID', 'currentMapID'):
    w('player.%s = %r' % (a, getattr(p, a, '<missing>')))
f.close()
