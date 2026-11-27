with open(OUT, 'w') as f:
    try:
        import ClientEntity, dis, StringIO, sys
        fn = getattr(ClientEntity.ClientEntity, 'enterWorld', None)
        f.write('ClientEntity.enterWorld: ' + repr(fn) + '\n')
        if fn:
            buf = StringIO.StringIO()
            old = sys.stdout; sys.stdout = buf
            dis.dis(fn)
            sys.stdout = old
            f.write(buf.getvalue())
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
