# READ-ONLY: loading flags / UI state after entering the tutorial map
import sys, BigWorld
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import Globals
for a in ('inLoading', 'inLoadingStage1', 'inLoadingStage2', 'fightUILoaded', 'firstEnterMap', 'MAP_ID', 'player', 'scene'):
    w('Globals.%s = %r' % (a, getattr(Globals, a, '<missing>')))
ML = sys.modules['helpers.MapLoader'].MapLoader.getInstance()
w('MapLoader enteringWorld=%r targetPosition=%r' % (getattr(ML, 'enteringWorld', '?'), getattr(ML, 'targetPosition', '?')))
p = BigWorld.player()
w('player %s id=%s pos=%r spaceID=%r inWorld=%r' % (type(p).__name__, p.id, tuple(p.position), getattr(p, 'spaceID', '?'), getattr(p, 'inWorld', '?')))
for a in ('gameObject', 'isDead', 'hp', 'battleState', 'isInBattle'):
    w('player.%s = %r' % (a, getattr(p, a, '<missing>')))
um = getattr(Globals, 'uiMgr', None)
for a in ('opened_uis', '_opened', 'uis', 'stack', '_ui_stack', 'cur_uis'):
    if hasattr(um, a): w('uiMgr.%s = %r' % (a, getattr(um, a)))
w('uiMgr attrs: %s' % [k for k in dir(um) if not k.startswith('__')][:80])
f.close()
