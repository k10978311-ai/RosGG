with open(OUT, 'w') as f:
    import BigWorld, traceback
    p = BigWorld.player()
    
    for name in ['preloadDtsHallProp', 'tryPhaseDeepLinkActions', 'tryUploadRCVersion']:
        try:
            fn = getattr(p, name, None)
            f.write(name + ': ' + repr(fn) + '\n')
            if fn:
                # do not call mutators, just inspect
                co = fn.im_func.func_code if hasattr(fn, 'im_func') else fn.func_code
                f.write('  co_names: ' + repr(co.co_names[:10]) + '\n')
        except Exception:
            f.write(traceback.format_exc() + '\n')
