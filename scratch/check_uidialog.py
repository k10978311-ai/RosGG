with open(OUT, 'w') as f:
    try:
        import Globals
        dlg = Globals.uiMgr.get_ui_by_name('UIDialog')
        f.write('UIDialog: ' + repr(dlg) + '\n')
        if dlg:
            f.write('dlg dir: ' + repr(dir(dlg)) + '\n')
            for attr in ['_des', '_title', 'des', 'title', 'content', 'text']:
                if hasattr(dlg, attr):
                    f.write(attr + ': ' + repr(getattr(dlg, attr)) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
