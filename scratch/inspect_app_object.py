f = open(OUT, "w")
try:
    import Athlete
    go = Athlete.GameObject
    scene = go.Find("Scene")
    ss = scene.GetComponent("SceneSystem")
    pfn = ss.__class__.__dict__.get("_preloadLevelResCoro")
    globs = pfn.func_globals
    f.write("Application in func_globals: %r\n" % (globs.get("Application"),))
    app = globs.get("Application")
    if app:
        f.write("app dir: %r\n" % ([a for a in dir(app) if not a.startswith("__")],))
        for m in ["PreloadLevel", "is_loading", "isLoading", "get_loading_progress", "LoadLevelAtFinish"]:
            f.write("app.%s: %r\n" % (m, getattr(app, m, "<none>")))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
