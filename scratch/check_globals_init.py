OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Globals, inspect
    f.write("Globals.rookieEnterHall: %r\n" % getattr(Globals, 'rookieEnterHall', 'NO_ATTR'))
    # Let's inspect Globals attributes
    for k in dir(Globals):
        if 'rookie' in k.lower() or 'enter' in k.lower() or 'hall' in k.lower():
            f.write("  Globals.%s: %r\n" % (k, getattr(Globals, k)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
