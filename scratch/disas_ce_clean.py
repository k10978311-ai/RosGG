with open(OUT, 'w') as f:
    try:
        import ClientEntity, dis, StringIO, sys
        fn = ClientEntity.ClientEntity.prerequisites
        buf = StringIO.StringIO()
        old = sys.stdout; sys.stdout = buf
        dis.dis(fn)
        sys.stdout = old
        f.write(buf.getvalue())
    except Exception as e:
        import traceback
        f.write('ERR: ' + traceback.format_exc() + '\n')
