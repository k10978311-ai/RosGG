import sys
f = open(OUT, "w")
try:
    import BigWorld
    p = BigWorld.player()
    f.write("loadCompFinished: %r\n" % getattr(p, "loadCompFinished", "<missing>"))
    f.write("curLoginHostID: %r\n" % getattr(p, "curLoginHostID", "<missing>"))
    f.write("hallScene: %r\n" % getattr(p, "hallScene", "<missing>"))
    f.write("gameObject: %r\n" % getattr(p, "gameObject", "<missing>"))
    f.write("behaviour: %r\n" % getattr(p, "behaviour", "<missing>"))
    f.write("voiceQueue: %r\n" % getattr(p, "voiceQueue", "<missing>"))
    f.write("finger_print_info: %r\n" % getattr(p, "finger_print_info", "<missing>"))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
