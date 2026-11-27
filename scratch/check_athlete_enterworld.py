import sys
f = open(OUT, "w")
try:
    import Athlete
    cls = Athlete.PlayerAthlete
    for c in cls.__mro__:
        if "enterWorld" in c.__dict__:
            f.write("enterWorld defined in %s.%s: %r\n" % (c.__module__, c.__name__, c.__dict__["enterWorld"]))
        if "onEnterWorld" in c.__dict__:
            f.write("onEnterWorld defined in %s.%s: %r\n" % (c.__module__, c.__name__, c.__dict__["onEnterWorld"]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
