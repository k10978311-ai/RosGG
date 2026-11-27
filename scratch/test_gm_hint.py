OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import BigWorld
    p = BigWorld.player()
    f.write("p.updateReadGMRedhintMsg: %r\n" % getattr(p, 'updateReadGMRedhintMsg', 'NO_ATTR'))
    f.write("p.readGMRedhintMsg: %r\n" % getattr(p, 'readGMRedhintMsg', 'NO_ATTR'))
    
    # Try calling it
    try:
        p.updateReadGMRedhintMsg(p.readGMRedhintMsg)
        f.write("call updateReadGMRedhintMsg: OK\n")
    except Exception as e:
        f.write("call updateReadGMRedhintMsg FAILED: %r\n" % e)

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
