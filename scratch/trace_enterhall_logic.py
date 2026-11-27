import sys
f = open(OUT, "w")
try:
    import Globals, shared.switches as switches, ros2_common
    f.write("Globals.enterSelectModeFinished: %r\n" % getattr(Globals, "enterSelectModeFinished", "<missing>"))
    f.write("switches.PCEnableMode: %r\n" % getattr(switches, "PCEnableMode", "<missing>"))
    f.write("isRos2Package: %r\n" % ros2_common.RosVersionController.isRos2Package())
    f.write("Globals.enterFirstFlag: %r\n" % getattr(Globals, "enterFirstFlag", "<missing>"))
    import BigWorld
    p = BigWorld.player()
    f.write("p.getValentineTShirt: %r\n" % getattr(p, "getValentineTShirt", "<missing>"))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
