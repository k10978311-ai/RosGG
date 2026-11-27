f = open(OUT, "w")
try:
    import linecache
    # Check if linecache can read the lines
    filename = "libclaudia\\Classes\\SceneSystem.py"
    lines = [linecache.getline(filename, i) for i in range(440, 480)]
    f.write("lines from linecache:\n")
    for i, line in enumerate(lines, 440):
        if line.strip():
            f.write("%d: %s" % (i, line))
    
    # Check if file exists on disk
    import os
    for p in ["libclaudia/Classes/SceneSystem.py", "libclaudia\\Classes\\SceneSystem.py"]:
        f.write("os.path.exists(%s): %r\n" % (p, os.path.exists(p)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
