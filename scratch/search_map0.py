f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/map0_search.txt", "w")
try:
    import sys
    for mod_name, mod in sys.modules.items():
        if not mod: continue
        for k in dir(mod):
            try:
                val = getattr(mod, k)
                fn = getattr(val, 'im_func', val)
                if hasattr(fn, 'func_code'):
                    co = fn.func_code
                    if 'MAP_ID' in co.co_names and 0 in co.co_consts:
                        f.write("%s.%s uses MAP_ID and 0\n" % (mod_name, k))
            except Exception:
                pass
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
