OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import elkLogging, const
    ev = elkLogging.getEngineVersion()
    rc3 = const.EngineVersion.RC3
    f.write("getEngineVersion(): %r\n" % ev)
    f.write("const.EngineVersion.RC3: %r\n" % rc3)
    f.write("ev < rc3: %r\n" % (ev < rc3))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
