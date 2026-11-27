with open(OUT, 'w') as f:
    try:
        import Globals
        uiMgr = Globals.uiMgr
        all_ui = getattr(uiMgr, '____all_ui__', {})
        f.write('all_ui keys: ' + repr(all_ui.keys()) + '\n')
        f.write('all_ui: ' + repr([(k, str(v)) for k, v in all_ui.items()]) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
