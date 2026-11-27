import traceback

with open(OUT, "w") as f:
    try:
        import offlineClient.SceneSystem as OSS
        f.write("offlineClient.SceneSystem dir: %r\n" % dir(OSS))
        for attr in dir(OSS):
            if not attr.startswith("__"):
                val = getattr(OSS, attr)
                f.write("  %s = %r\n" % (attr, val))
    except Exception:
        f.write(traceback.format_exc())
