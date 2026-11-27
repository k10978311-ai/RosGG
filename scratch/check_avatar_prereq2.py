with open(OUT, 'w') as f:
    try:
        import Avatar
        pfn = Avatar.PlayerAvatar.prerequisites
        f.write('PlayerAvatar.prerequisites: ' + repr(pfn) + '\n')
        co = pfn.im_func.func_code if hasattr(pfn, 'im_func') else getattr(pfn, 'func_code', None)
        if co:
            f.write('names: ' + repr(co.co_names) + '\n')
            f.write('consts: ' + repr(co.co_consts) + '\n')
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
