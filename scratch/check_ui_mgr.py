with open(OUT, 'w') as f:
    try:
        import Globals
        uiMgr = Globals.uiMgr
        f.write('uiMgr: ' + repr(uiMgr) + '\n')
        # check ui dicts or lists on uiMgr
        for attr in ['_ui_dict', '_uis', '_cur_ui', '_all_uis', 'uis', 'all_ui']:
            if hasattr(uiMgr, attr):
                f.write(attr + ': ' + repr(getattr(uiMgr, attr)) + '\n')
        # list all attributes of uiMgr that contain ui
        f.write('uiMgr attrs: ' + repr([x for x in dir(uiMgr) if 'ui' in x.lower() or 'panel' in x.lower()]) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
