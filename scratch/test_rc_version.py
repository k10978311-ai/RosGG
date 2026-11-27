OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import BigWorld
    p = BigWorld.player()
    f.write("Calling p.tryUploadRCVersion()...\n")
    p.tryUploadRCVersion()
    f.write("tryUploadRCVersion: OK\n")
except Exception as e:
    import traceback
    f.write("tryUploadRCVersion FAILED:\n" + traceback.format_exc())
f.close()
