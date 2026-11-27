f = open(OUT, "w")
try:
    import Athlete
    fn = Athlete.PlayerAthlete.enterHall.im_func
    inner_fn = fn.func_closure[0].cell_contents
    code = inner_fn.func_code
    
    f.write("inner enterHall names: %r\n" % (code.co_names,))
    f.write("inner enterHall consts: %r\n" % (code.co_consts,))
    f.write("inner enterHall varnames: %r\n" % (code.co_varnames,))
    
    # Let's inspect the sub code object _realEnterHall
    for c in code.co_consts:
        if hasattr(c, 'co_name') and c.co_name == '_realEnterHall':
            f.write("\n_realEnterHall names: %r\n" % (c.co_names,))
            f.write("_realEnterHall consts: %r\n" % (c.co_consts,))
            f.write("_realEnterHall varnames: %r\n" % (c.co_varnames,))
            # Let's check sub code objects of _realEnterHall too
            for sc in c.co_consts:
                if hasattr(sc, 'co_name'):
                    f.write("  sub code in _realEnterHall: %s (names=%r, consts=%r)\n" % (sc.co_name, sc.co_names, sc.co_consts))

    # Check player values
    import BigWorld
    p = BigWorld.player()
    f.write("\np.enterFirstFlag: %r\n" % (getattr(p, 'enterFirstFlag', '<no>'),))
    f.write("p.enterSelectModeFinished: %r\n" % (getattr(p, 'enterSelectModeFinished', '<no>'),))
    
    import switches
    f.write("switches.PCEnableMode: %r\n" % (getattr(switches, 'PCEnableMode', '<no>'),))
    
    import ros2_common
    f.write("isRos2Package: %r\n" % (ros2_common.RosVersionController.isRos2Package(),))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
