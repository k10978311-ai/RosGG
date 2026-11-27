f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/dis_hall.txt', 'w')
try:
    import Athlete
    fn = Athlete.PlayerAthlete.enterHall
    if hasattr(fn, 'im_func'): fn = fn.im_func
    for c in fn.func_closure or []:
        if hasattr(c.cell_contents, 'func_code'):
            for const_val in c.cell_contents.func_code.co_consts:
                if hasattr(const_val, 'co_names'):
                    f.write('nested code object: %r co_names: %r\n' % (const_val.co_name, const_val.co_names))
                    f.write('  co_consts: %r\n' % ([x for x in const_val.co_consts if not hasattr(x, 'co_names')],))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
