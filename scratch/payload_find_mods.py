import sys
import traceback

with open(OUT, "w") as f:
    try:
        f.write("Matching modules:\n")
        for m in sorted(sys.modules.keys()):
            if any(k in m.lower() for k in ["scene", "global", "ui", "hall", "athlete", "app"]):
                f.write("  %s\n" % m)
    except Exception:
        f.write(traceback.format_exc())
