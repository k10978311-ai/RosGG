f = open(OUT, "w")
try:
    import shared.switches as switches
    f.write("URGENT_SWITCH_ENABLE_FORCE_UPGRADE: %r\n" % (getattr(switches, "URGENT_SWITCH_ENABLE_FORCE_UPGRADE", "<none>"),))
    import elkLogging, const
    ev = elkLogging.getEngineVersion()
    f.write("engineVersion: %r\n" % (ev,))
    f.write("RC3: %r\n" % (getattr(const.EngineVersion, "RC3", "<none>"),))
    f.write("ev < RC3: %r\n" % (ev < const.EngineVersion.RC3 if hasattr(const.EngineVersion, "RC3") else "<none>",))
    f.write("isWin32: %r\n" % (getattr(switches, "isWin32", lambda: False)(),))
    f.write("isMac: %r\n" % (getattr(switches, "isMac", lambda: False)(),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
