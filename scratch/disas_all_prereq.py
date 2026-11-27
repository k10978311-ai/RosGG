f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/dis_all_prereq.txt', 'w')
try:
    import Avatar, Athlete, dis, sys
    f.write('=== Avatar.Avatar.prerequisites ===\n')
    fn = getattr(Avatar.Avatar, 'prerequisites', None)
    if hasattr(fn, 'im_func'): fn = fn.im_func
    if fn:
        f.write('co_names: %r\n' % (fn.func_code.co_names,))
        orig = sys.stdout; sys.stdout = f; dis.dis(fn); sys.stdout = orig
    f.write('\n=== PlayerAvatar.prerequisites ===\n')
    fn = getattr(Avatar.PlayerAvatar, 'prerequisites', None)
    if hasattr(fn, 'im_func'): fn = fn.im_func
    if fn:
        f.write('co_names: %r\n' % (fn.func_code.co_names,))
        orig = sys.stdout; sys.stdout = f; dis.dis(fn); sys.stdout = orig
    f.write('\n=== Athlete.Athlete.prerequisites ===\n')
    fn = getattr(Athlete.Athlete, 'prerequisites', None)
    if hasattr(fn, 'im_func'): fn = fn.im_func
    if fn:
        f.write('co_names: %r\n' % (fn.func_code.co_names,))
        orig = sys.stdout; sys.stdout = f; dis.dis(fn); sys.stdout = orig
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
