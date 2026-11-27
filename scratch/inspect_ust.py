with open(OUT, 'w') as f:
    try:
        import sys, types, dis, StringIO
        mod = sys.modules.get('ui.UISkipTutorial')
        f.write('mod dict keys: ' + repr(dir(mod)) + '\n')
        cls = getattr(mod, 'UISkipTutorial', None)
        # Search all functions in mod
        for k, v in mod.__dict__.items():
            if isinstance(v, (types.FunctionType, types.MethodType)):
                f.write('fn: ' + k + '\n')
        # Check instance if active
        import Globals
        ui = Globals.uiMgr.get_ui('UISkipTutorial') if hasattr(Globals, 'uiMgr') else None
        f.write('ui instance: ' + repr(ui) + '\n')
        if ui:
            for k in dir(ui):
                v = getattr(ui, k, None)
                if 'yes' in k.lower() or 'callback' in k.lower() or 'skip' in k.lower() or 'touch' in k.lower():
                    f.write('ui member: %s = %r\n' % (k, v))
        # Let's inspect class methods and codes
        for k in dir(cls):
            v = getattr(cls, k, None)
            if callable(v):
                code = getattr(v, 'func_code', None) or getattr(getattr(v, 'im_func', None), 'func_code', None)
                if code:
                    f.write('method %s has code: consts=%r, names=%r\n' % (k, code.co_consts, code.co_names))
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
