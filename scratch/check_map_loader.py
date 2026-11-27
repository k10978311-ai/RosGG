with open(OUT, 'w') as f:
    import helpers.MapLoader as ML
    f.write("MapLoader dir: %r\n" % dir(ML))
    import Athlete
    p_enter = getattr(Athlete.PlayerAthlete, 'enterHall', None)
    if p_enter and hasattr(p_enter, 'func_code'):
        f.write("enterHall names: %r\n" % (p_enter.func_code.co_names,))
        f.write("enterHall consts: %r\n" % (p_enter.func_code.co_consts,))
        f.write("enterHall varnames: %r\n" % (p_enter.func_code.co_varnames,))
    import ui.UISkipTutorial as ST
    f.write("UISkipTutorial dir: %r\n" % dir(ST))
    cls = getattr(ST, 'UISkipTutorial', None)
    if cls:
        f.write("UISkipTutorial methods: %r\n" % [m for m in dir(cls) if not m.startswith('__')])
        for m_name in ['onExitBtnEvent', 'tryLeaveMap']:
            m = getattr(cls, m_name, None)
            if m and hasattr(m, 'func_code'):
                f.write("%s names: %r\n" % (m_name, m.func_code.co_names))
                f.write("%s consts: %r\n" % (m_name, m.func_code.co_consts))
