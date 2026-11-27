OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Globals
    esm = getattr(Globals, 'enterSelectModeFinished', None)
    f.write("Globals.enterSelectModeFinished: %r\n" % esm)
    
    import Athlete
    real_fn = Athlete.PlayerAthlete.enterHall.func_closure[0].cell_contents
    switches = real_fn.func_globals.get('switches')
    f.write("switches: %r\n" % switches)
    pc_mode = getattr(switches, 'PCEnableMode', None)
    f.write("switches.PCEnableMode: %r\n" % pc_mode)
    
    ros2_common = real_fn.func_globals.get('ros2_common')
    f.write("ros2_common: %r\n" % ros2_common)
    is_ros2 = ros2_common.RosVersionController.isRos2Package()
    f.write("isRos2Package(): %r\n" % is_ros2)
    
    cond = esm and pc_mode and not is_ros2
    f.write("Condition (esm and pc_mode and not is_ros2): %r\n" % cond)

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
