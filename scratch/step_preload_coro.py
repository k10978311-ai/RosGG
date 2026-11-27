f = open(OUT, "w")
try:
    import Athlete, const
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem")
    coro = ss._preloadLevelResCoro(const.HALL_MAP_ID, None)
    
    val1 = coro.next()
    f.write("yield 1: %r\n" % (val1,))
    val2 = coro.next()
    f.write("yield 2: %r\n" % (val2,))
    val3 = coro.next()
    f.write("yield 3: %r\n" % (val3,))
except StopIteration:
    f.write("StopIteration!\n")
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
