import Globals
f = open(OUT, 'w')
um = Globals.uiMgr
ua = um.get_ui_by_name('UIUserAgreement')
if ua:
    f.write('ua panel: %r\n' % getattr(ua, 'panel', None))
    for attr in dir(ua):
        obj = getattr(ua, attr, None)
        if hasattr(obj, 'getPosition') or hasattr(obj, 'getWorldPosition') or hasattr(obj, 'getContentSize'):
            pos = getattr(obj, 'getWorldPosition', lambda: getattr(obj, 'getPosition', lambda: None)())()
            size = getattr(obj, 'getContentSize', lambda: None)()
            f.write('  %s: pos=%r size=%r\n' % (attr, pos, size))
f.close()
