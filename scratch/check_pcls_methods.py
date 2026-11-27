f = open(OUT, "w")
try:
    import Athlete
    pcls = Athlete.PlayerAthlete
    
    f.write("bases: %r\n" % (pcls.__mro__,))
    for k in dir(pcls):
        v = getattr(pcls, k)
        if callable(v) and hasattr(v, 'im_func'):
            co = v.im_func.func_code
            if 'loadHallScene' in co.co_names:
                f.write("Found loadHallScene in %s (names=%r)\n" % (k, co.co_names))
            if 'enterHall' in k.lower():
                f.write("enterHall method %s: names=%r\n" % (k, co.co_names))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
