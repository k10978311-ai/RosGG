import traceback, BigWorld, const
f = open(OUT, 'w')
try:
    const.CLIENT_INACTIVE_DEFAULT_TIME = 300.0
    const.CLIENT_INACTIVE_HALL_TIME = 300.0
    BigWorld.setInactivityTimeout(300.0)
    f.write('SUCCESS: set inactivityTimeout to %r, const.CLIENT_INACTIVE_DEFAULT_TIME=%r\n' % (
        BigWorld.getInactivityTimeout(), const.CLIENT_INACTIVE_DEFAULT_TIME))
except Exception:
    f.write(traceback.format_exc())
f.close()
