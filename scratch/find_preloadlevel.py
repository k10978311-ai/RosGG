f = open(OUT, "w")
try:
    import sys
    for name, mod in sys.modules.items():
        if mod and hasattr(mod, "PreloadLevel"):
            f.write("Found PreloadLevel in %s: %r\n" % (name, getattr(mod, "PreloadLevel")))
        if mod and hasattr(mod, "LoadLevel"):
            f.write("Found LoadLevel in %s: %r\n" % (name, getattr(mod, "LoadLevel")))
        if mod and hasattr(mod, "load_scene"):
            f.write("Found load_scene in %s: %r\n" % (name, getattr(mod, "load_scene")))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
