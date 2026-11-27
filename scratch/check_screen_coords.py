import Globals
f = open(OUT, 'w')
try:
    ul = Globals.uiMgr.get_ui_by_name('UILogin')
    btn = getattr(ul, 'login_btn', None)
    f.write('btn: %r\n' % btn)
    if btn:
        f.write('btn dir: %r\n' % [x for x in dir(btn) if 'pos' in x.lower() or 'rect' in x.lower() or 'box' in x.lower() or 'bound' in x.lower() or 'screen' in x.lower()])
        for m in ('getWorldPosition', 'getPosition', 'getBoundingBox', 'getContentSize', 'getAnchorPoint'):
            if hasattr(btn, m):
                try:
                    f.write('%s: %r\n' % (m, getattr(btn, m)()))
                except Exception as e:
                    f.write('%s err: %r\n' % (m, e))
        # check resolution
        import cc
        f.write('visibleSize: %r\n' % (getattr(cc.Director.getInstance(), 'getVisibleSize', lambda: None)()))
        f.write('winSize: %r\n' % (getattr(cc.Director.getInstance(), 'getWinSize', lambda: None)()))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
