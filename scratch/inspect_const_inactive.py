import traceback
f = open(OUT, 'w')
try:
    import const, BigWorld
    for name in dir(const):
        if 'inactive' in name.lower():
            f.write('%s = %r\n' % (name, getattr(const, name)))
    f.write('current inactivityTimeout = %r\n' % (BigWorld.getInactivityTimeout(),))
except Exception:
    f.write(traceback.format_exc())
f.close()
