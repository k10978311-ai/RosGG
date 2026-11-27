OUT = '/storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log'
f = open(OUT, 'w')
try:
    import Avatar
    for name in dir(Avatar):
        obj = getattr(Avatar, name)
        if hasattr(obj, 'prerequisites') or 'prerequisites' in getattr(obj, '__dict__', {}):
            f.write('%s has prerequisites in dict: %r\n' % (name, 'prerequisites' in obj.__dict__))
    import entities.Avatar as ent_av
    for name in dir(ent_av):
        obj = getattr(ent_av, name)
        if hasattr(obj, 'prerequisites') or 'prerequisites' in getattr(obj, '__dict__', {}):
            f.write('ent_av.%s has prerequisites in dict: %r\n' % (name, 'prerequisites' in obj.__dict__))
except Exception:
    import traceback
    f.write(traceback.format_exc())
f.close()
