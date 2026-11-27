import Globals
f = open(OUT, 'w')
um = Globals.uiMgr
vis = getattr(um, '_UIMgr____all_ui__vis', {})
f.write('vis UIs: %r\n' % ([k for k, v in vis.items() if v]))
f.close()
