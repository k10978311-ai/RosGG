with open(OUT, 'w') as f:
    try:
        import Globals
        for attr in ['FIRST_LOAD', 'FIRST_LOAD_TIME', 'isWin32', 'isMac']:
            f.write(attr + ': ' + repr(getattr(Globals, attr, 'NOT_SET')) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
