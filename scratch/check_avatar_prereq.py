import sys
f = open(OUT, "w")
try:
    import Avatar
    for c in Avatar.PlayerAvatar.__mro__:
        if "prerequisites" in c.__dict__:
            f.write("PlayerAvatar.prerequisites defined in %s.%s: %r\n" % (c.__module__, c.__name__, c.__dict__["prerequisites"]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
