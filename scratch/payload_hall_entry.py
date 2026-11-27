import BigWorld
import traceback

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        f.write("Player class: %s\n" % type(p).__name__)
        hall_methods = [m for m in dir(p) if any(w in m.lower() for w in ['hall', 'login', 'scene', 'main', 'enter', 'ready'])]
        f.write("Relevant player methods:\n%r\n" % hall_methods)
        
        # Check what enterHall does
        import inspect
        if hasattr(p, "enterHall"):
            f.write("enterHall doc/func: %r\n" % getattr(p, "enterHall"))
        if hasattr(p, "_realEnterHall"):
            f.write("_realEnterHall doc/func: %r\n" % getattr(p, "_realEnterHall"))
        if hasattr(p, "onHallSceneReady"):
            f.write("onHallSceneReady doc/func: %r\n" % getattr(p, "onHallSceneReady"))
        if hasattr(p, "enterHallUI"):
            f.write("enterHallUI doc/func: %r\n" % getattr(p, "enterHallUI"))

        # Check state flags on p
        flags = [a for a in dir(p) if 'flag' in a.lower() or 'state' in a.lower() or 'step' in a.lower() or 'ready' in a.lower() or 'scene' in a.lower()]
        f.write("\nState flags on player:\n")
        for fl in flags:
            try:
                f.write("  %s = %r\n" % (fl, getattr(p, fl)))
            except Exception:
                pass
    except Exception:
        f.write(traceback.format_exc())
