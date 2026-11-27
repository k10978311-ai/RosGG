f = open(OUT, "w")
try:
    import libclaudia.Classes.Application as app
    f.write("app.scene: %r\n" % (app.scene,))
    if app.scene:
        f.write("app.scene.name: %r\n" % (getattr(app.scene, "name", "<none>"),))
    
    # Check if any level is preloaded
    for attr in dir(app):
        if "level" in attr.lower():
            f.write("attr %s: %r\n" % (attr, getattr(app, attr, "<none>")))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
