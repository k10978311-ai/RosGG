with open(OUT, 'w') as f:
    try:
        import sys
        cls = sys.modules['Avatar'].PlayerAvatar
        fn = getattr(cls, 'enterWorld', None)
        f.write('PlayerAvatar.enterWorld: ' + repr(fn) + '\n')
        if fn:
            import dis, StringIO
            buf = StringIO.StringIO()
            old = sys.stdout; sys.stdout = buf
            dis.dis(fn)
            sys.stdout = old
            f.write(buf.getvalue())
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
