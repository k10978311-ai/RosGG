f = open("/storage/emulated/0/Android/data/com.netease.chiji/files/skip_search.txt", "w")
try:
    import sys
    for mod_name, mod in sys.modules.items():
        if not mod: continue
        for k in dir(mod):
            if 'skip' in k.lower() or 'tutorial' in k.lower():
                val = getattr(mod, k)
                if callable(val) and hasattr(val, 'im_func'):
                    co = val.im_func.func_code
                    f.write("%s.%s: co_names=%r, co_consts=%r\n" % (
                        mod_name, k, co.co_names[:10],
                        [x for x in co.co_consts if not hasattr(x, 'co_names')][:10]))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
