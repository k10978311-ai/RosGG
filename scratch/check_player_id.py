f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/pid_out.txt", "w")
try:
    import BigWorld
    p = BigWorld.player()
    f.write("player: %r\n" % (p,))
    if p:
        f.write("p.id: %r\n" % getattr(p, 'id', None))
    f.write("BigWorld.entities: %r\n" % (list(BigWorld.entities.keys()),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
