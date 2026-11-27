with open(OUT, 'w') as f:
    try:
        import sys
        mod = sys.modules['Avatar']
        for k, v in mod.__dict__.items():
            fn = getattr(v, 'im_func', v)
            co = getattr(fn, 'func_code', None)
            if co and 'player' in co.co_names:
                f.write('Avatar member %s has player in co_names\n' % k)
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
