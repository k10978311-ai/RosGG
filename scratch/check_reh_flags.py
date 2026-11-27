with open(OUT, 'w') as f:
    try:
        import Globals
        f.write('rookieEnterHall: ' + repr(getattr(Globals, 'rookieEnterHall', 'NOT_SET')) + '\n')
        f.write('enterFirstFlag: ' + repr(getattr(Globals, 'enterFirstFlag', 'NOT_SET')) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
