import Globals
f = open(OUT, 'w')
um = Globals.uiMgr
ul = um.get_ui_by_name('UILogin')
if ul:
    for btn_name in ('login_btn', 'btn_enter', 'btn_play'):
        btn = getattr(ul, btn_name, None)
        f.write('btn %s: %r\n' % (btn_name, btn))
        if btn and hasattr(btn, 'getWorldPosition'):
            f.write('  worldPos=%r size=%r\n' % (btn.getWorldPosition(), getattr(btn, 'getContentSize', lambda: None)()))
f.close()
