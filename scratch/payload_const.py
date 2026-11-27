import sys, traceback
out = open(OUT, 'w')
try:
    import const
    out.write('SelectCharacterScene: %r\n' % getattr(const, 'SelectCharacterScene', None))
    out.write('SelectCharacterScenePostProcess: %r\n' % getattr(const, 'SelectCharacterScenePostProcess', None))
    for k in dir(const):
        if 'scene' in k.lower() or 'hall' in k.lower() or 'char' in k.lower():
            out.write('  %s = %r\n' % (k, getattr(const, k)))
except Exception:
    out.write(traceback.format_exc())
out.close()
