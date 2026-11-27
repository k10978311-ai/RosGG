import Globals
f = open(OUT, 'w')
um = Globals.uiMgr
for name in ('UIUserAgreement', 'UILogin', 'UIFollowonFacebook', 'UIJumpTip'):
    ui = um.get_ui(name) if hasattr(um, 'get_ui') else None
    f.write('UI %s: %r\n' % (name, ui))
    if ui:
        for attr in ('_root', 'widget', '_panel', 'btn_play', 'btn_enter', 'btn_ok', 'btn_agree', 'confirm_btn'):
            v = getattr(ui, attr, None)
            if v is not None:
                f.write('  %s.%s = %r\n' % (name, attr, v))
f.close()
