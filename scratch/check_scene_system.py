with open(OUT, 'w') as f:
    import inspect
    for name in ['SceneSystem', 'MapLoader', 'logic.gcommon.common.SceneSystem']:
        try:
            m = __import__(name, fromlist=['*'])
            f.write("module %s: %r\n" % (name, dir(m)))
        except Exception as e:
            f.write("import %s error: %r\n" % (name, e))
    try:
        import logic.gcommon.common.SceneSystem as SS
        f.write("SS dir: %r\n" % dir(SS))
    except Exception as e:
        f.write("SS err: %r\n" % e)
