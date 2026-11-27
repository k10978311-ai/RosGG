# READ-ONLY: login-scene switches/state, and the names used by UILogin._delay_on_enter.
import sys, types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import Globals
UL = sys.modules.get('ui.UILogin')
g = vars(UL) if UL else {}
sw = g.get('switches')
for k in ('URGENT_SWITCH_USE_LOGIN_SCENE', 'EnablePlayVideoOnUILogin', 'EnableLocalServerList'):
    w('switches.%s=%r' % (k, getattr(sw, k, '<missing>')))
for k in ('loginScene', 'loginResReady', 'MAP_ID', 'player', 'firstLoad'):
    w('Globals.%s=%r' % (k, getattr(Globals, k, '<missing>')))
try:
    world = g.get('world') or sys.modules.get('world')
    w('world.get_active_scene()=%r' % (world.get_active_scene(),))
except Exception as e:
    w('world err %r' % (e,))
fn = UL.UILogin.__dict__.get('_delay_on_enter') if UL else None
if fn is not None:
    co = fn.func_code
    w('_delay_on_enter names=%s' % (list(co.co_names),))
    w('_delay_on_enter consts=%r' % ([c for c in co.co_consts if not isinstance(c, types.CodeType)],))
f.close()
