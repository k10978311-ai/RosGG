# READ-ONLY: hall-entry state after Athlete creation.
import sys
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import BigWorld, Globals, ClientEntity
p = BigWorld.player()
w('player=%r class=%s' % (p, p.__class__.__name__ if p else None))
App = vars(ClientEntity).get('Application')
w('Application.scene=%r' % (getattr(App, 'scene', '?'),))
for k in ('player', 'isInHall', 'hallSceneReady', 'isInGame', 'MAP_ID', 'inLoading', 'loginResReady', 'serverSauthInfo'):
    w('Globals.%s=%r' % (k, getattr(Globals, k, '<missing>')))
w('prereq=%r cached=%r entities=%r' % (BigWorld.prereqEntities(), BigWorld.cachedEntities(), dict(BigWorld.entities.items())))
um = getattr(Globals, 'uiMgr', None)
for attr in ('_UIMgr____all_ui__vis', '_UIMgr____all_ui_enter_times'):
    v = getattr(um, attr, None)
    if isinstance(v, dict):
        w('uiMgr.%s=%r' % (attr, dict((k, x) for k, x in v.items() if x)))
f.close()
