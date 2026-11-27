import sys, traceback
f = open(OUT, 'w')
def w(s): f.write(s + '\n')
try:
    A = sys.modules['libclaudia.Classes.Application'].Application
    for k in ('____scene_object__','____current_level__','____next_level__','____loaded_level__','____next_level_callback__','____initialized__'):
        v = getattr(A, k, 'MISSING'); w('%s = %r' % (k, v))
    so = getattr(A, '____scene_object__', None)
    if so is not None:
        w('scene_object attrs: %r' % [a for a in dir(so) if not a.startswith('__')][:50])
        w('_scene = %r' % getattr(so, '_scene', 'MISSING'))
    cl = getattr(A, '____current_level__', None)
    if cl is not None:
        w('level attrs: %r' % [a for a in dir(cl) if not a.startswith('__')][:60])
    w('Application.scene = %r' % (A.scene,))
    import Globals
    w('Globals.inLoading=%r inLoadingStage1=%r' % (Globals.inLoading, Globals.inLoadingStage1))
except Exception:
    w(traceback.format_exc())
f.close()
