f = open('/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log', 'w')
try:
    import sys
    for mod_name, mod in sys.modules.items():
        if mod and ('Athlete' in mod_name or 'athlete' in mod_name):
            f.write('module: %s -> %r\n' % (mod_name, mod))
        elif mod:
            for k in dir(mod):
                if k == 'PlayerAthlete':
                    f.write('found in %s.%s = %r\n' % (mod_name, k, getattr(mod, k)))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
