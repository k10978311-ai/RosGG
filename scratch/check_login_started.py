import Globals
f = open(OUT, 'w')
um = Globals.uiMgr
vis = getattr(um, '_UIMgr____all_ui__vis', {})
f.write('vis UIs: %r\n' % ([k for k, v in vis.items() if v]))
ul = um.get_ui_by_name('UILogin')
if ul:
    f.write('loginStarted: %r\n' % getattr(ul, '_loginStarted', None))
f.close()
