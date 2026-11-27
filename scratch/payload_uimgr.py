import sys, traceback
out = open(OUT, 'w')
try:
    import Globals
    uiMgr = getattr(Globals, 'uiMgr', None)
    out.write('uiMgr: %r\n' % uiMgr)
    if uiMgr:
        for k in dir(uiMgr):
            if 'ui' in k.lower():
                val = getattr(uiMgr, k)
                out.write('  %s: %r\n' % (k, val))
except Exception:
    out.write(traceback.format_exc())
out.close()
