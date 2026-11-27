# USER-APPROVED EXCEPTION to AGENTS.md rule 1 (2026-11-16): enable the login-scene switch only.
#
# switches.URGENT_SWITCH_USE_LOGIN_SCENE is False in this build and can only be flipped at
# runtime by server methods that are themselves stuck behind the scene gate
# (ClientEntity.prerequisites needs Application.scene). This turns the switch on and runs
# exactly the code path the switch gates in UILogin._delay_on_enter (Globals.loadDefaultScene),
# since UILogin has already passed that point. Nothing else is changed: no login skip, no fake
# entities, no UI dismissal.
import traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    import sys, Globals, ClientEntity
    sw = sys.modules['shared.switches']
    w('before: URGENT_SWITCH_USE_LOGIN_SCENE=%r loginScene=%r' % (sw.URGENT_SWITCH_USE_LOGIN_SCENE, Globals.loginScene))
    sw.URGENT_SWITCH_USE_LOGIN_SCENE = True
    App = vars(ClientEntity).get('Application')
    if Globals.loginScene is None and getattr(App, 'scene', None) is None:
        Globals.loadDefaultScene()
        w('called Globals.loadDefaultScene()')
    w('after: switch=%r loginScene=%r App.scene=%r' % (sw.URGENT_SWITCH_USE_LOGIN_SCENE, Globals.loginScene, getattr(App, 'scene', None)))
except Exception:
    w(traceback.format_exc())
f.close()
