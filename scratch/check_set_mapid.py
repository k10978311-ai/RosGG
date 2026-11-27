f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/set_mapid.txt', 'w')
try:
    import sys
    for mod_name, mod in sys.modules.items():
        if not mod: continue
        for attr in dir(mod):
            try:
                obj = getattr(mod, attr)
                fns = []
                if hasattr(obj, 'im_func'): fns.append((attr, obj.im_func))
                elif callable(obj) and hasattr(obj, 'func_code'): fns.append((attr, obj))
                elif isinstance(obj, type):
                    for k, v in obj.__dict__.items():
                        if hasattr(v, 'im_func'): fns.append(('%s.%s' % (attr, k), v.im_func))
                        elif hasattr(v, 'func_code'): fns.append(('%s.%s' % (attr, k), v))
                for name, fn in fns:
                    if 'MAP_ID' in fn.func_code.co_names:
                        f.write('%s.%s uses MAP_ID\n' % (mod_name, name))
            except Exception:
                pass
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
