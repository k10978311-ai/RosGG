OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import BigWorld
    p = BigWorld.player()
    
    # test preloadDtsHallProp
    try:
        p.preloadDtsHallProp()
        f.write("preloadDtsHallProp: OK\n")
    except Exception as e:
        f.write("preloadDtsHallProp FAILED: %r\n" % e)
        
    # test tryPhaseDeepLinkActions
    try:
        p.tryPhaseDeepLinkActions()
        f.write("tryPhaseDeepLinkActions: OK\n")
    except Exception as e:
        f.write("tryPhaseDeepLinkActions FAILED: %r\n" % e)

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
