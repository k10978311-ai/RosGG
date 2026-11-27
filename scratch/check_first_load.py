OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Globals
    f.write("Globals.FIRST_LOAD: %r\n" % getattr(Globals, 'FIRST_LOAD', 'NO_ATTR'))
    f.write("Globals.FIRST_LOAD_TIME: %r\n" % getattr(Globals, 'FIRST_LOAD_TIME', 'NO_ATTR'))
    
    # Also test lines 348 to 430
    import SALogging, time
    f.write("SALogging: %r\n" % SALogging)
    f.write("hasattr usKeyPoint: %r\n" % hasattr(SALogging, 'usKeyPoint'))
    f.write("hasattr drpfLogging: %r\n" % hasattr(SALogging, 'drpfLogging'))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
