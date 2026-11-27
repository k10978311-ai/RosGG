import Globals, traceback

f = open(OUT, 'w')
try:
    all_ui = getattr(Globals.uiMgr, '____all_ui__', {})
    ulang = all_ui.get('UILanguageBtn')
    if ulang:
        f.write("=== UILanguageBtn ===\n")
        for a in dir(ulang):
            if not a.startswith('__'):
                try:
                    val = getattr(ulang, a)
                    if not callable(val):
                        f.write("  %s = %r\n" % (a, str(val)[:120]))
                except:
                    pass
except Exception:
    f.write(traceback.format_exc())
f.close()
