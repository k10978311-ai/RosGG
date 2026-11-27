import Athlete
import traceback

with open(OUT, "w") as f:
    try:
        GO = Athlete.GameObject
        scene_obj = GO.Find("SceneSystem")
        f.write("scene_obj: %r\n" % scene_obj)
        if scene_obj:
            comp = scene_obj.GetComponent("SceneSystem")
            f.write("comp: %r\n" % comp)
            f.write("comp loadHallScene: %r\n" % getattr(comp, "loadHallScene", None))
    except Exception:
        f.write(traceback.format_exc())
