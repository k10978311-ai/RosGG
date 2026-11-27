OUT = "/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log"
f = open(OUT, "w")
try:
    import Globals, Athlete
    real_fn = Athlete.PlayerAthlete.enterHall.func_closure[0].cell_contents
    fg = real_fn.func_globals
    switches = fg.get('switches')
    
    f.write("switches: %r\n" % switches)
    if switches:
        f.write("  URGENT_SWITCH_ENABLE_FORCE_UPGRADE: %r\n" % getattr(switches, 'URGENT_SWITCH_ENABLE_FORCE_UPGRADE', 'NO_ATTR'))
        
    for k in ('needKickOut', 'needRealName', 'doRealnameAuthenAgain', 'realnameAuthenAgainFlag', 'forceLogout', 'isWin32', 'isMac', 'loadCompFinished'):
        f.write("Globals.%s: %r\n" % (k, getattr(Globals, k, 'NO_ATTR')))

    # Let's inspect what line _realEnterHall actually reached or if an exception happened!
    # Let's check _realEnterHall bytecode from 130 to 750
    co = real_fn.func_code
    for c in co.co_consts:
        if hasattr(c, 'co_name') and c.co_name == '_realEnterHall':
            # Check constants
            f.write("_realEnterHall consts: %r\n" % (c.co_consts,))

except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
