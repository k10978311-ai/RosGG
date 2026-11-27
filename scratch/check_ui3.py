import Globals
f = open(OUT, 'w')
um = Globals.uiMgr
for name in ('UIUserAgreement', 'UILogin'):
    ui = um.get_ui_by_name(name)
    f.write('UI %s: %r\n' % (name, ui))
    if ui:
        f.write('  attrs: %r\n' % [a for a in dir(ui) if not a.startswith('__')])
f.close()
