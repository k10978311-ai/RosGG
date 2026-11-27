f = open(OUT, "w")
try:
    import Athlete
    cls = Athlete.PlayerAthlete
    f.write("PlayerAthlete methods:\n")
    for k in sorted(cls.__dict__.keys()):
        v = cls.__dict__[k]
        if hasattr(v, 'func_code'):
            f.write("  %s\n" % k)
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
