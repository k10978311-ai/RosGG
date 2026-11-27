import Globals
f = open(OUT, 'w')
um = Globals.uiMgr
ul = um.get_ui_by_name('UILogin')
if ul:
    f.write('server: %r:%r (%r)\n' % (getattr(ul, 'defaultServerIP', None), getattr(ul, 'defaultServerPort', None), getattr(ul, 'defaultServerName', None)))
f.close()
