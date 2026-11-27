with open(OUT, 'w') as f:
    try:
        import Globals
        f.write('MAP_ID: ' + repr(getattr(Globals, 'MAP_ID', 'None')) + '\n')
        f.write('PREV_MAP_ID: ' + repr(getattr(Globals, 'PREV_MAP_ID', 'None')) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
