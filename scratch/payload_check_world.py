import world
import traceback

with open(OUT, "w") as f:
    try:
        f.write("world dir: %r\n" % dir(world))
        for attr in ["current_scene", "scene", "get_scene", "get_world", "camera", "active_scene"]:
            if hasattr(world, attr):
                val = getattr(world, attr)
                if callable(val):
                    try:
                        val = val()
                    except Exception as e:
                        val = "error: %s" % e
                f.write("world.%s: %r\n" % (attr, val))
    except Exception:
        f.write(traceback.format_exc())
