import BigWorld
import traceback
import dis

with open(OUT, "w") as f:
    try:
        p = BigWorld.player()
        if hasattr(p, "prerequisites"):
            func = getattr(p, "prerequisites")
            f.write("prerequisites: %r\n" % func)
            if hasattr(func, "im_func"):
                code = func.im_func.func_code
                f.write("code consts: %r\n" % (code.co_consts,))
                f.write("code names: %r\n" % (code.co_names,))
                f.write("disassembly:\n")
                import StringIO
                s = StringIO.StringIO()
                dis.dis(code, s)
                f.write(s.getvalue())
        
        # Check prerequisiteReady setter or callers
        if hasattr(p, "onPrerequisitesReady"):
            f.write("onPrerequisitesReady: %r\n" % getattr(p, "onPrerequisitesReady"))
    except Exception:
        f.write(traceback.format_exc())
