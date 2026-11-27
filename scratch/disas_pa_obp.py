with open(OUT, 'w') as f:
    try:
        import Avatar, dis, StringIO, sys
        fn = getattr(Avatar.PlayerAvatar, 'onBecomePlayer', None)
        f.write('fn: ' + repr(fn) + '\n')
        if fn:
            buf = StringIO.StringIO()
            old = sys.stdout; sys.stdout = buf
            dis.dis(fn)
            sys.stdout = old
            f.write(buf.getvalue())
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
