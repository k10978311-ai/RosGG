f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/obp_def.txt', 'w')
try:
    import Athlete
    pa = Athlete.PlayerAthlete
    for c in pa.__mro__:
        if 'onBecomePlayer' in c.__dict__:
            f.write('Found onBecomePlayer in %s\n' % c.__name__)
            fn = c.__dict__['onBecomePlayer']
            if hasattr(fn, 'im_func'): fn = fn.im_func
            f.write('co_names: %r\n' % (fn.func_code.co_names,))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
