import traceback

with open(OUT, "w") as f:
    try:
        import libclaudia.Classes.SceneSystem as SS
        f.write("SceneSystem dir: %r\n" % dir(SS))
        import GameObject
        f.write("GameObject dir: %r\n" % dir(GameObject))
        scene_obj = GameObject.Find("SceneSystem")
        f.write("scene_obj: %r\n" % scene_obj)
        if scene_obj:
            comp = scene_obj.GetComponent("SceneSystem")
            f.write("comp: %r\n" % comp)
            f.write("comp dir: %r\n" % dir(comp))
    except Exception:
        f.write(traceback.format_exc())
