import sys
f = open(OUT, "w")
try:
    import ClientEntity, Globals
    App = vars(ClientEntity).get("Application")
    scene = getattr(App, "scene", None)
    f.write("App.scene: %r (type %s)\n" % (scene, type(scene).__name__))
    if scene:
        for k in sorted(dir(scene)):
            if not k.startswith("__"):
                try:
                    val = getattr(scene, k)
                    f.write("  scene.%s = %r\n" % (k, val))
                except Exception as ex:
                    f.write("  scene.%s = <err %r>\n" % (k, ex))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
