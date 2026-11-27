with open(OUT, 'w') as f:
    import sys
    for mod_name, mod in sys.modules.items():
        if 'uir2main' in mod_name.lower():
            f.write("mod: %s -> %r\n" % (mod_name, mod))
            f.write("dir: %r\n" % dir(mod))
    import UIMgr
    f.write("UIMgr has UIR2Main: %r\n" % hasattr(UIMgr, 'UIR2Main'))
