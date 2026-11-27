import sys
f = open(OUT, "w")
try:
    import ClientEntity, Globals, BigWorld
    p = BigWorld.player()
    f.write("before: p.prerequisites() -> %r\n" % p.prerequisites())
    Globals.player = p
    f.write("after setting Globals.player: p.prerequisites() -> %r\n" % p.prerequisites())
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
