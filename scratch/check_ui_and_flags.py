OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Globals
    f.write("enterSelectModeFinished: %r\n" % getattr(Globals, 'enterSelectModeFinished', 'NO_ATTR'))
    f.write("enterFirstFlag: %r\n" % getattr(Globals, 'enterFirstFlag', 'NO_ATTR'))
    f.write("channel: %r\n" % getattr(Globals, 'channel', 'NO_ATTR'))
    
    import switches
    f.write("switches.PCEnableMode: %r\n" % getattr(switches, 'PCEnableMode', 'NO_ATTR'))
    
    import ros2_common
    f.write("RosVersionController.isRos2Package: %r\n" % ros2_common.RosVersionController.isRos2Package())
    
    # Check what UI is currently active/open
    uiMgr = Globals.uiMgr
    f.write("uiMgr: %r\n" % uiMgr)
    f.write("uiMgr.all_ui_names: %r\n" % dir(uiMgr))
    for attr in ('_ui_dict', '_uis', '_all_ui', 'ui_dict', 'dict_ui', '_cur_ui'):
        if hasattr(uiMgr, attr):
            f.write("uiMgr.%s = %r\n" % (attr, getattr(uiMgr, attr)))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
