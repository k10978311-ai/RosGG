with open(OUT, 'w') as f:
    try:
        import inspect, dis, StringIO, sys
        import ui.UISkipTutorial as ust
        f.write('UISkipTutorial members: ' + repr(dir(ust)) + '\n')
        if hasattr(ust, 'UISkipTutorial'):
            f.write('UISkipTutorial class: ' + repr(dir(ust.UISkipTutorial)) + '\n')
        # find yes_callback
        cb = getattr(ust, 'yes_callback', None)
        if not cb and hasattr(ust, 'UISkipTutorial'):
            cb = getattr(ust.UISkipTutorial, 'yes_callback', None)
        if cb:
            buf = StringIO.StringIO()
            old = sys.stdout; sys.stdout = buf
            dis.dis(cb)
            sys.stdout = old
            f.write('yes_callback dis:\n' + buf.getvalue() + '\n')
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
