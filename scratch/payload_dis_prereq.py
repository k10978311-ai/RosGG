import sys
import BigWorld
import traceback
import dis
import StringIO

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        func = getattr(p, "prerequisites")
        g = func.im_func.func_globals
        f.write("Application in globals: %r\n" % g.get("Application"))
        app = g.get("Application")
        if app:
            scene = getattr(app, "scene", None)
            f.write("app.scene: %r\n" % scene)
        
        s = StringIO.StringIO()
        old_out = sys.stdout
        sys.stdout = s
        try:
            dis.dis(func.im_func.func_code)
        finally:
            sys.stdout = old_out
        f.write("\nDisassembly of prerequisites:\n" + s.getvalue())

        f.write("\nCalling prerequisites()...\n")
        res = p.prerequisites()
        f.write("Returned: %r\n" % (res,))
        f.write("prerequisiteReady: %r\n" % getattr(p, "prerequisiteReady", None))
    except Exception:
        f.write(traceback.format_exc())
