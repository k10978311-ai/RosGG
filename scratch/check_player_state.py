OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import BigWorld
    p = BigWorld.player()
    f.write("player: %r\n" % p)
    for attr in ('gameObject', 'entityBehaviour', 'behaviour', 'loadCompFinished', 'inHall', 'isPlayer'):
        f.write("  p.%s: %r\n" % (attr, getattr(p, attr, 'NO_ATTR')))
    
    # check Globals.inHall or Globals.setInHall
    import Globals
    for attr in ('inHall', 'is_in_hall', 'hallSceneReady'):
        f.write("  Globals.%s: %r\n" % (attr, getattr(Globals, attr, 'NO_ATTR')))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
