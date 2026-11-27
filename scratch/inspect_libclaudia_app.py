f = open(OUT, "w")
try:
    import libclaudia.Classes.Application as app
    f.write("app: %r\n" % (app,))
    f.write("dir(app): %r\n" % ([a for a in dir(app) if not a.startswith("__")],))
    for m in ["PreloadLevel", "LoadLevel", "LoadLevelAsync", "is_loading", "isLoading", "get_loading_progress", "LoadLevelAtFinish"]:
        if hasattr(app, m):
            f.write("app.%s: %r\n" % (m, getattr(app, m)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
