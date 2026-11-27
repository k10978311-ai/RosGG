OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    try:
        import GameInit
        f.write("import GameInit: OK -> %r\n" % GameInit)
        if hasattr(GameInit, 'updateInactivityTimeout'):
            f.write("has updateInactivityTimeout: True\n")
            GameInit.updateInactivityTimeout()
            f.write("updateInactivityTimeout() OK\n")
    except Exception as e:
        import traceback
        f.write("import GameInit FAILED:\n" + traceback.format_exc())

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
