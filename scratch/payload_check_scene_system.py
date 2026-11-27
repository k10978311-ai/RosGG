import libclaudia.Classes.SceneSystem as SceneSystem
import traceback

with open(OUT, "w") as f:
    try:
        f.write("SceneSystem dir: %r\n" % dir(SceneSystem))
        for attr in ["currentMapId", "curSceneName", "is_loading", "isLoading", "_loading", "currentScene", "scene"]:
            if hasattr(SceneSystem, attr):
                f.write("SceneSystem.%s: %r\n" % (attr, getattr(SceneSystem, attr)))
    except Exception:
        f.write(traceback.format_exc())
