with open(OUT, 'w') as f:
    try:
        import dis
        for op, name in enumerate(dis.opname):
            if name != '<%d>' % op:
                f.write('%d: %s\n' % (op, name))
    except Exception as e:
        import traceback
        f.write('Error: ' + traceback.format_exc() + '\n')
