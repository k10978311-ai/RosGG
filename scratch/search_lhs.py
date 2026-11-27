f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/lhs_search.txt", "w")
try:
    import sys
    for mod_name, mod in sys.modules.items():
        if not mod: continue
        for k in dir(mod):
            try:
                val = getattr(mod, k)
                fn = getattr(val, 'im_func', val)
                if hasattr(fn, 'func_code'):
                    if 'loadHallScene' in fn.func_code.co_names:
                        f.write("CALLS loadHallScene: %s.%s\n" % (mod_name, k))
            except Exception:
                pass
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
