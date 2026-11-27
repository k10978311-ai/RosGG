OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import sys, BigWorld
    p = BigWorld.player()
    
    trace_log = []
    
    def tracer(frame, event, arg):
        co = frame.f_code
        if 'enterHall' in co.co_name or 'EnterHall' in co.co_name:
            trace_log.append("%s: %s:%d (event=%s, arg=%r)" % (co.co_name, co.co_filename, frame.f_lineno, event, arg))
            if event == 'exception':
                trace_log.append("  EXCEPTION in %s: %r" % (co.co_name, arg))
        return tracer
        
    sys.settrace(tracer)
    try:
        f.write("Calling p.enterHall(True)...\n")
        p.enterHall(True)
        f.write("enterHall completed normally.\n")
    except Exception as e:
        import traceback
        f.write("enterHall raised EXCEPTION:\n" + traceback.format_exc() + "\n")
    finally:
        sys.settrace(None)
        
    f.write("\nTrace log (%d events):\n" % len(trace_log))
    for l in trace_log[:200]:
        f.write("  " + l + "\n")

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
