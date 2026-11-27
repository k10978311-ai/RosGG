# READ-ONLY: PlayerAthlete set_<prop> callbacks that touch scene/hall/map/UI loading.
import types
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
import Athlete
KEYS = ('hallScene', 'LoadLevel', 'MapLoader', 'enterHall', 'preloadMap', 'setHallSceneReady', 'loadMap', 'SceneSystem', 'enter_ui', 'UISelectMode', 'loadDefaultScene')
seen = set(); n = 0
for cls in Athlete.PlayerAthlete.__mro__:
    for k, v in cls.__dict__.items():
        if not k.startswith('set_') or k in seen or not isinstance(v, types.FunctionType): continue
        seen.add(k); n += 1
        co = v.func_code
        hits = [x for x in KEYS if x in co.co_names or any(x in str(c) for c in co.co_consts if isinstance(c, str))]
        if hits: w('%s.%s -> %s' % (cls.__name__, k, hits))
w('total set_ callbacks: %d' % n)
f.close()
