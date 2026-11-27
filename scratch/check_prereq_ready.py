with open(OUT, 'w') as f:
    import sys
    for mod_name, mod in sys.modules.items():
        if hasattr(mod, '__file__') and mod.__file__:
            pass
    # check where prerequisiteReady is used in ClientEntity or Athlete
    import ClientEntity
    f.write("ClientEntity dir: %r\n" % dir(ClientEntity.ClientEntity))
    for m in ['onPrerequisite', 'prerequisites', '__init__']:
        fn = getattr(ClientEntity.ClientEntity, m, None)
        if fn and hasattr(fn, 'func_code'):
            f.write("ClientEntity.%s co_names: %r\n" % (m, fn.func_code.co_names))
            f.write("ClientEntity.%s co_consts: %r\n" % (m, fn.func_code.co_consts))
