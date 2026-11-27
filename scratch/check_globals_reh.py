OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Globals
    f.write("Globals.rookieEnterHall: %r\n" % getattr(Globals, 'rookieEnterHall', 'NO_ATTR'))
    f.write("Globals.hasLogonServer: %r\n" % getattr(Globals, 'hasLogonServer', 'NO_ATTR'))
    f.write("Globals.patchNpkCheckResult: %r\n" % getattr(Globals, 'patchNpkCheckResult', 'NO_ATTR'))
    f.write("Globals.timerRefreshMSToken: %r\n" % getattr(Globals, 'timerRefreshMSToken', 'NO_ATTR'))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
