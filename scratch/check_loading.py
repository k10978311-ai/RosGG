import Globals
f = open(OUT, 'w')
um = Globals.uiMgr
ul = um.get_ui_by_name('UILoading')
f.write('UILoading: %r\n' % (ul,))
if ul:
    for a in ('percent', 'progress', 'cur_progress', '_progress', 'loading_bar', 'tip_text', 'tips', '_is_loading', 'loading_res'):
        f.write('  %s = %r\n' % (a, getattr(ul, a, '<missing>')))
f.close()
