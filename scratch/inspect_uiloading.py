f = open(OUT, "w")
try:
    import Globals
    uiMgr = Globals.uiMgr
    all_ui = getattr(uiMgr, '____all_ui__', getattr(uiMgr, '_UIMgr____all_ui__', {}))
    loading = all_ui.get('UILoading')
    f.write("loading: %r\n" % (loading,))
    if loading:
        cls = loading.__class__
        f.write("class: %s\n" % (cls,))
        for m in dir(cls):
            if not m.startswith('__'):
                f.write("  m: %s\n" % (m,))
        # Check close or hide methods
        for fn in ['close', 'hide', 'on_close', 'onClose', 'destroy', 'finishLoading']:
            if hasattr(loading, fn):
                f.write("  has %s\n" % fn)
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
