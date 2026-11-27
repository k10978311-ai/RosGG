with open(OUT, 'w') as f:
    try:
        import ClientEntity
        fn = getattr(ClientEntity.ClientEntity, 'onBecomePlayer', None)
        f.write('ClientEntity.onBecomePlayer: ' + repr(fn) + '\n')
        if fn:
            co = fn.im_func.func_code if hasattr(fn, 'im_func') else fn.func_code
            f.write('names: ' + repr(co.co_names) + '\n')
            f.write('consts: ' + repr([c for c in co.co_consts if not hasattr(c, 'co_names')]) + '\n')
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
